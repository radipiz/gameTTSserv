import dataclasses


@dataclasses.dataclass
class Config:
    emotion_weight = 1.0
    speech_speed = 1.1
    speech_varianceA = 0.6
    speech_varianceB = 0.6
