#!/usr/bin/env python3
import asyncio
import sys
from dataclasses import asdict

from sanic import Sanic
from sanic.response import HTTPResponse, json, text
from sanic.request import Request
from adapter.gameTtsAdapter import DatabaseAdapter, TtsAdapter, setup_gameTTS


async def main():
    sys.path.append('gametts')
    setup_gameTTS()
    app = Sanic("gameTTSServ")
    app.ctx.db = DatabaseAdapter()
    await app.ctx.db.connect()

    tts = TtsAdapter()

    @app.route('get_all_voices', methods=['GET'])
    async def get_all_voices(request: Request) -> HTTPResponse:
        voices = await app.ctx.db.get_all_voices()
        return json(list(map(lambda v: asdict(v), voices)))

    @app.route('synthesize', methods=['GET'])
    async def synthesize(request: Request) -> HTTPResponse:
        filepath = await tts.synthesize()
        return text(filepath)

    app.run(host='0.0.0.0', port=3000, debug=False)
    print(await tts.synthesize())


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
