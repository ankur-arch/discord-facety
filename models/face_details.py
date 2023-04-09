from dataclasses import dataclass


@dataclass
class FaceDetails:
    age: str
    gender: str
    race: str
    age: int
    emotion: str
    face: bytes
    region: dict
    _emotion_map = {
        'happy': '😍',
        'angry': '🤬',
        'disgust': '🤮',
        'fear': '😨',
        'sad': '😞',
        'surprise': '😮',
        'neutral': '😐',
    }

    def emotion_emoji(self):
        if self.emotion in self._emotion_map:
            return self._emotion_map.get(self.emotion)
        return '😭'
