import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Метод возвращающий название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Метод добавления"""
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        """Метод вычитания"""
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        """Метод сравнения (больше)"""
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        """Метод сравнения (дольше или равно)"""
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        """Метод сравнения (меньше)"""
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        """Метод сравнения (меньше или равно)"""
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        """Метод сравнения (меньше)"""
        return int(self.subscriberCount) == int(other.subscriberCount)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        from pprint import pprint
        pprint(self.channel)

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API """
        return cls.youtube

    def to_json(self, dict_to_print) -> None:
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""

        with open(dict_to_print, "w", encoding='utf-8') as write_file:
            json.dump({"title": self.title,
                       "description": self.description,
                       "url": self.url,
                       "subscriberCount": self.subscriberCount,
                       "video_count": self.video_count,
                       "viewCount": self.viewCount}, write_file, indent=2, ensure_ascii=False, separators=(',', ': '))
