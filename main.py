#!/usr/bin/env python3
import asyncio
import sys
import time
from dataclasses import asdict

import adapter.patches
from flask import Flask, make_response, jsonify, request
from adapter.gameTtsAdapter import DatabaseAdapter, TtsAdapter, setup_gameTTS


async def main():
    sys.path.append('gametts')
    setup_gameTTS()
    app = Flask("gameTTSServ")
    db = DatabaseAdapter()
    await db.connect()

    tts = TtsAdapter()

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

    @app.route('/synthesize', methods=['GET', 'POST'])
    async def synthesize():
        params = {
            'speaker_id': 1,
            'language_id': 1,
            'emotion_id': 1,
            'style_id': 1,
            'text': ''
        }
        data = request.json
        if not isinstance(data, dict):
            return make_response('Body must contain json object containing the following keys: ' + ', '.join(params.keys()))

        for key in params:
            if key in data:
                if not isinstance(data[key], type(params[key])):
                    return make_response(f'{key} has must be {type(params[key])}', 400)
                params[key] = data[key]

        if len(params['text']) > 1000:
            return make_response(f'text has a maximum length of 1000', 400)
        if len(params['text']) == 0:
            return make_response(f'text must not be empty', 400)
        start_time = time.process_time()
        wav_file = await tts.synthesize(**params)
        mp3_file = await tts.convert_wav_to_mp3(wav_file)
        end_time = time.process_time()
        print(wav_file)
        with open(mp3_file, 'rb') as audio:
            response = make_response(audio.read())

        extra_params = set(data.keys()) - set(params.keys())
        if extra_params:
            response.headers['Unprocessed-Keys'] = ','.join(extra_params)
        response.headers['Content-Type'] = 'audio/mp3'
        response.headers['Processing-Time'] = str(end_time - start_time)

        return response

    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
