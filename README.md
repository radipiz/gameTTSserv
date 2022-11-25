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
| `speaker_id`   | 1       | No        | see [adapter/extractedData.py](adapter/extractedData.py) |
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

