import typing
from dataclasses import dataclass


@dataclass
class ExtendedSpeaker:
    name: str
    speaker_id: int
    game_name: str
    game_id: int
    internal_speaker: typing.Optional[str]


@dataclass
class Game:
    game_id: int
    name: str


@dataclass
class Speaker:
    speaker_id: int
    _id: int
    name: str
    game_id: int
