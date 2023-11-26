import pytest

from helper.youtube_api_manual import channel_id, channel
from src.channel import Channel


@pytest.fixture
def moscowpython_channel():
    return Channel('UC-OVMPlMA3-YCIeg4z5z23A')


def test_channel_attributes(moscowpython_channel):
    assert channel_id == 'UC-OVMPlMA3-YCIeg4z5z23A'


def test_print_info(moscowpython_channel):
    assert channel.is_file()
