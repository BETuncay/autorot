import torch
from TTS.api import TTS



def test_tts():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # generate speech by cloning a voice using default settings
    tts.tts_to_file(
        text="Hello world!", 
        speaker_wav=r"Dagoth Ur\Dagoth Ur Welcome C.mp3", 
        language="en", 
        file_path="output1.wav")

    tts.tts_to_file(
        text="Hello world!",
        speaker="Craig Gutsy",
        language="en",
        file_path="output2.wav"
        )