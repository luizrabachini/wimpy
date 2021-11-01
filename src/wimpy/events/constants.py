__all__ = ['get_default_event_data_schema']


DEFAULT_EVENT_DATA_SCHEMA = {
    'type': 'object',
    'properties': {
        'host': {
            'type': 'string'
        },
        'path': {
            'type': 'string'
        },
    },
    'required': ['host', 'path']
}


def get_default_event_data_schema():
    return DEFAULT_EVENT_DATA_SCHEMA
