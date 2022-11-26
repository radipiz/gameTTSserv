import dataclasses
import os


@dataclasses.dataclass
class Config:
    # better don't touch
    emotion_weight = 1.0
    speech_varianceA = 0.6
    speech_varianceB = 0.6
    sample_size = 10
    # language to use for espeak. Needed for pronunciation (some construction can even lead to exceptions)
    # use en-us for English
    # see https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md for more languages
    # (use values from Identifier column; may sound weird if the speech model doesn't "know" how it should sound)
    language = os.getenv("CONF_LANGUAGE", "de")

    # configurable
    # lower values = faster
    speech_speed = float(os.getenv("CONF_SPEECH_SPEED", 1.1))
    default_speaker_id = int(os.getenv("CONF_SPEAKER_ID", 1))
    default_emotion_id = int(os.getenv("CONF_EMOTION_ID", 5))
    default_style_id = int(os.getenv("CONF_STYLE_ID", 0))

    # maximum character count to synthesize
    max_text_length = int(os.getenv("CONF_MAX_TEXT_LENGTH", 1000))

    # values > 0 enable housekeeper service
    max_stored_files = int(os.getenv("CONF_MAX_FILES", 500))

    output_file_path = '/tmp'
