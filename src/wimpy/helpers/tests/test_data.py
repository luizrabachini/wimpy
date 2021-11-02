from wimpy.helpers.data import deserialize_data, serialize_data


class TestData:

    def test_deserialize_data(self):
        assert deserialize_data(b'{"a": "b"}') == {'a': 'b'}

    def test_serialize_data(self):
        assert serialize_data({'a': 'b'}) == b'{"a": "b"}'
