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
    language = 'de' if "CONF_LANGUAGE" not in os.environ else os.environ['CONF_LANGUAGE']

    # configurable
    # lower values = faster
    speech_speed = 1.1 if "CONF_SPEECH_SPEED" not in os.environ else float(os.environ["CONF_SPEECH_SPEED"])
    default_speaker_id = 1 if "CONF_SPEAKER_ID" not in os.environ else int(os.environ["CONF_SPEAKER_ID"])
    default_emotion_id = 5 if "CONF_EMOTION_ID" not in os.environ else int(os.environ["CONF_EMOTION_ID"])
    default_style_id = 0 if "CONF_STYLE_ID" not in os.environ else int(os.environ["CONF_STYLE_ID"])

    # maximum character count to synthesize
    max_text_length = 1000 if "CONF_MAX_TEXT_LENGTH" not in os.environ else int(os.environ["CONF_MAX_TEXT_LENGTH"])

    server_port = 3000 if "CONF_PORT" not in os.environ else int(os.environ["CONF_PORT"])

    # values > 0 enable housekeeper service
    max_stored_files = 500 if "CONF_MAX_FILES" not in os.environ else int(os.environ["CONF_MAX_FILES"])

    output_file_path = '/tmp'
