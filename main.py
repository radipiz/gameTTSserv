#!/usr/bin/env python3
import asyncio
import logging
import sys
import time
from dataclasses import asdict

import adapter.extractedData
from flask import Flask, make_response, jsonify, request
from adapter.gameTtsAdapter import DatabaseAdapter, TtsAdapter, setup_gameTTS
from core.housekeeper import Housekeeper

background_tasks = set()


def schedule_housekeeping_task(housekeeper: Housekeeper):
    task = asyncio.create_task(housekeeper.sweep())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)


async def create_app():
    logging.basicConfig(level=logging.DEBUG)
    sys.path.append('gametts')
    import core.config
    config = core.config.Config
    setup_gameTTS()
    app = Flask("gameTTSServ")
    db = DatabaseAdapter()
    await db.connect()

    tts = TtsAdapter()

    # initialize Housekeeping
    housekeeper = Housekeeper()
    housekeeper.scan()
    schedule_housekeeping_task(housekeeper)

    @app.route('/get_voices', methods=['GET'])
    async def get_voices():
        voices = await db.get_all_voices()
        return jsonify(list(map(lambda v: asdict(v), voices)))

    @app.route('/get_games', methods=['GET'])
    async def get_games():
        games = await db.get_games()
        return jsonify(list(map(lambda g: asdict(g), games)))

    @app.route('/get_characters', methods=['GET'])
    async def get_characters():
        voices = await db.get_all_characters()
        return jsonify(list(map(lambda v: asdict(v), voices)))

    @app.route('/get_emotes', methods=['GET'])
    async def get_emotes():
        return jsonify(adapter.extractedData.EMOTION)

    @app.route('/get_speech_styles', methods=['GET'])
    async def get_speech_styles():
        return jsonify(adapter.extractedData.SPEECH_STYLE)

    @app.route('/synthesize', methods=['GET', 'POST'])
    async def synthesize():
        params = {
            'speaker_id': config.default_speaker_id,
            'emotion_id': config.default_emotion_id,
            'style_id': config.default_style_id,
            'text': '',
            'speech_speed': config.speech_speed
        }
        data = request.json if request.method == 'POST' else request.args
        if not isinstance(data, dict):
            return make_response(
                'Body must contain json object containing the following keys: ' + ', '.join(params.keys()))

        for key in params:
            if key in data:
                params[key] = type(params[key])(data[key])

        if len(params['text']) > config.max_text_length:
            return make_response(f'text has a maximum length of ${config.max_text_length}', 400)
        if len(params['text']) == 0:
            return make_response(f'text must not be empty', 400)
        start_time = time.process_time()
        mp3_file = await tts.synthesize(**params)
        end_time = time.process_time()
        logging.debug(f'Processed %d characters in %s seconds', len(params['text']), end_time - start_time)
        with open(mp3_file, 'rb') as audio:
            response = make_response(audio.read())

        extra_params = set(data.keys()) - set(params.keys())
        if extra_params:
            response.headers['Unprocessed-Keys'] = ','.join(extra_params)
        response.headers['Content-Type'] = 'audio/mp3'
        response.headers['Processing-Time'] = str(end_time - start_time)

        schedule_housekeeping_task(housekeeper)
        return response

    return app


def get_app():
    return asyncio.run(create_app())


if __name__ == '__main__':
    flask = asyncio.run(create_app())
    flask.run(host='0.0.0.0', port=3000)
