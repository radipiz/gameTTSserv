from GameTTS.gametts import TTS, VoiceConversion, Enhancer
import sys

if len(sys.argv) != 2:
	print('No Text given', file=sys.stderr)
	exit(2)

model_path = 'Custom Application Data Folder/Resources/TTS'
espeakDLL = 'Custom Application Data Folder/Resources/libespeak-ng.dll'
espeakDLL = '/usr/lib/libespeak-ng.so'
tmp_file_path = '/tmp'
embeddings_path = 'Custom Application Data Folder/Resources'
tts = TTS(model_path, embeddings_path, tmp_file_path)
tts.set_espeak_library(espeakDLL)
tts.set_espeak_backend()
filepath = tts.synthesize(sys.argv[1], 1, 1, 2, 1,  {'split_sentence': True, 'sample_size': 1, 'varianz_a':1, 'varianz_b': 1, 'speech_speed':1, 'emotion_weight':1})
print(filepath)
