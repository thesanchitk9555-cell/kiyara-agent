import datetime
import base64
import wave
import io

def encode_audio_to_base64(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode('utf-8')

def decode_base64_audio(b64_str: str) -> bytes:
    return base64.b64decode(b64_str)

def pcm_to_wav(pcm_data: bytes, sample_rate=16000, channels=1) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)
    return buffer.getvalue()

def get_timestamp() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"