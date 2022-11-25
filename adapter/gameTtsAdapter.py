import os
import sys
import typing
import zipfile
from databases import Database
from .databaseModel import ExtendedSpeaker, Game
from gametts.GameTTS.gametts import TTS


class DatabaseAdapter:
    database: Database

    def __init__(self):
        self.database = Database('sqlite+aiosqlite:///gametts/GameTTS.db')

    async def connect(self):
        await self.database.connect()

    async def get_all_characters(self) -> typing.List[ExtendedSpeaker]:
        query = '''SELECT 
                    `name` name, 
                    `speakerId` speaker_id, 
                    `GameName` game_name, 
                    `GameId` game_id,
                    `InternalSpeaker` internal_speaker 
                FROM `main`.`ExtendedSpeaker`
                ORDER BY `GameName`, `name` '''
        result = await self.database.fetch_all(query=query)
        return list(map(lambda r: ExtendedSpeaker(**r), result))

    async def get_all_voices(self) -> typing.List[ExtendedSpeaker]:
        query = '''SELECT
            DISTINCT `s`.`id` speaker_id,
            `s`.`Name` name,
            `s`.`GameId` game_id,
            `g`.`Name` game_name,
            `es`.`InternalSpeaker` internal_speaker
        FROM `Speaker` s 
        JOIN `Game` g ON `g`.`Id` = `s`.`GameId`
        JOIN `ExtendedSpeaker` es ON `es`.`SpeakerId` = `s`.`SpeakerId`
        ORDER BY `game_name`, `name`
        '''
        result = await self.database.fetch_all(query=query)
        return list(map(lambda r: ExtendedSpeaker(**r), result))

    async def get_games(self) -> typing.List[Game]:
        query = 'SELECT `id` game_id, `name` FROM `main`.`Game` ORDER BY `name`'
        result = await self.database.fetch_all(query=query)
        return list(map(lambda r: Game(**r), result))


class TtsAdapter:
    tts: TTS

    def __init__(self):
        prefix = 'gametts/'
        model_path = prefix + 'Custom Application Data Folder/Resources/TTS'
        # espeakDLL = 'Custom Application Data Folder/Resources/libespeak-ng.dll'
        espeakDLL = '/usr/lib/libespeak-ng.so'
        tmp_file_path = '/tmp'
        embeddings_path = prefix + 'Custom Application Data Folder/Resources'

        self.tts = TTS(model_path, embeddings_path, tmp_file_path)
        self.tts.set_espeak_library(espeakDLL)
        self.tts.set_espeak_backend()

    async def synthesize(self):
        print('Starting')
        filepath = self.tts.synthesize("Test", 1, 1, 2, 1,
                                       {'split_sentence': True, 'sample_size': 1, 'varianz_a': 1, 'varianz_b': 1,
                                        'speech_speed': 1, 'emotion_weight': 1})
        print(filepath)
        return filepath


def setup_gameTTS():
    base_path = 'gametts/Custom Application Data Folder/Resources'
    paths = [
        ('TTS/config.json', 'model-data.zip'),
        ('0', 'embeddings-data.zip')
    ]
    for check_file, zip_file in paths:
        check_file, zip_file = os.path.join(base_path, check_file), os.path.join(base_path, zip_file)
        if not os.path.exists(check_file):
            with zipfile.ZipFile(zip_file, 'r') as f:
                f.extractall(base_path)
            print('unzipping ' + os.path.join(base_path, zip_file), file=sys.stderr)
