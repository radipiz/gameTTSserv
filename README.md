# GameTTSserv
A wrapper around GameTTS application to provide its functionality as a REST API.

## Requirements

* Python 3.9
* `requirements.txt`
* espeak-ng

_Tested on Linux_

## Setup

1. Create a folder `gametts` next to `main.py`
2. Retrieve application with models from [forum.worldofplayers.de](https://forum.worldofplayers.de/forum/threads/1580689-RELEASE-GameTTS-Text-To-Speech-Anwendung?s=0cd9d04f0ca07b62c10d8173406066a5&p=26797697&viewfull=1#post26797697) (Tested with Version 1.1.5)
3. Unzip/Install the application
4. Copy all contents of the application's folder into `gametts` folder
5. Run `pip install -r requirements.txt`
6. Launch server with `python main.py` (for evaluation)

## Endpoints

### /get_characters
Lists all possible characters to use as value for `speaker_id`

### /get_emotes
Lists all possible emote styles to use as value for `emote_id`

### /get_games
Lists all games from which are voices available

### /get_voices
Lists all available voices to use as value for `speaker_id`

### /synthesize
Supports the following parameters either as GET or POST request. For POST in must be supplied as JSON.

| Param          | Default | Mandatory | Notes                                                    |
|----------------|---------|-----------|----------------------------------------------------------|
| `emotion_id`   | 5       | No        | see [adapter/extractedData.py](adapter/extractedData.py) |
| `speaker_id`   | 1       | No        | Depends on data set (query with `/get_voices`)           |
| `style_id`     | 0       | No        | see [adapter/extractedData.py](adapter/extractedData.py) |
| `speech_speed` | 1.1     | No        | Lower means faster                                       |
| `text`         | None    | Yes       | Maximum length as per default is 1000 characters         |

Example body:
```JSON
{
  "speaker_id": 147,
  "text": "We're testing the text to speech system."
}
```

## Configuration
It's possible to change default settings and a few parameters via environment variables. Use full for Docker.

| Variable | Default | Notes |
| --- |--| --- |
| `CONF_LANGUAGE` | de | [core/config.py](core/config.py), see [espeak-ng](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md) for more languages |
| `CONF_SPEECH_SPEED` | 1.1 | [core/config.py](core/config.py) |
| `CONF_SPEAKER_ID` | 1 | [core/config.py](core/config.py) |
| `CONF_EMOTION_ID` | 5 | [core/config.py](core/config.py) |
| `CONF_STYLE_ID` | 0 | [core/config.py](core/config.py) |
| `CONF_MAX_TEXT_LENGTH` | 1000 | [core/config.py](core/config.py), maximum length of a text to synthesize |
| `CONF_MAX_FILES` | 500 | [core/config.py](core/config.py), maximum number of files to cache, 0 means infinite files |
| `PORT` | 8000 | [gunicornconfig.py](gunicornconfig.py) |
| `WEB_CONCURRENCY` | 1 | [gunicornconfig.py](gunicornconfig.py), concurrent worker threads. Careful with this setting as every worker loads the speech model and needs adequate memory

