import uuid
import gametts.GameTTS.gametts

gametts.GameTTS.gametts.text2filename = lambda s: str(uuid.uuid4())
