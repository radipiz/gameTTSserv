import os
import pathlib
import pydub
import sys
import typing
import zipfile
from databases import Database
from .databaseModel import ExtendedSpeaker, Game
from gametts.GameTTS.gametts import TTS
from core.config import Config
import core.util


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
        query = 'SELECT `id` game_id, `Name` name FROM `main`.`Game` ORDER BY `Name`'
        result = await self.database.fetch_all(query=query)
        return list(map(lambda r: Game(**r), result))


class TtsAdapter:
    tts: TTS

    def __init__(self):
        prefix = 'gametts/'
        model_path = prefix + 'Custom Application Data Folder/Resources/TTS'
        if os.name == 'nt':
            espeak_dll = 'Custom Application Data Folder/Resources/libespeak-ng.dll'
        else:
            espeak_dll = '/usr/lib/libespeak-ng.so'
        embeddings_path = prefix + 'Custom Application Data Folder/Resources'

        self.tts = TTS(model_path, embeddings_path, Config.output_file_path)
        self.tts.set_espeak_library(espeak_dll)
        self.tts.set_espeak_backend()

    async def synthesize(self, text, speaker_id=1, emotion_id=1, style_id=0,
                         speech_speed=Config.speech_speed) -> pathlib.Path:
        file_name = core.util.generate_filename(speaker_id, emotion_id, style_id, speech_speed, text)
        cache_path = pathlib.Path(Config.output_file_path, file_name + '.mp3')
        if cache_path.is_file():
            return cache_path
        # speaker_id is only visual
        # the actual voice is the language_id (third argument)
        filepath = self.tts.synthesize(text, speaker_id, speaker_id, emotion_id, style_id, {
            'split_sentence': False,
            'sample_size': Config.sample_size,
            'varianz_a': Config.speech_varianceA,
            'varianz_b': Config.speech_varianceB,
            'speech_speed': speech_speed,
            'emotion_weight': Config.emotion_weight,
            'file_name': file_name
        })
        return await self.convert_wav_to_mp3(filepath)

    async def convert_wav_to_mp3(self, filepath: pathlib.Path, delete_original=True):
        output_path = pathlib.Path(filepath.parent, filepath.stem + '.mp3')
        pydub.AudioSegment.from_wav(filepath).export(output_path, format='mp3')
        if delete_original:
            filepath.unlink(missing_ok=True)
        return output_path


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
