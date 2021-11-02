import json
from typing import Dict

__all__ = ['serialize_data', 'deserialize_data']


def serialize_data(data: Dict) -> bytes:
    return json.dumps(data).encode('utf-8')


def deserialize_data(data: bytes) -> Dict:
    return json.loads(data.decode('utf-8'))
