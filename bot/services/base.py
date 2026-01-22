from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseDownloaderService(ABC):

    @abstractmethod
    async def validate(self, url: str) -> bool:
        """Проверяет, относится ли URL к этой платформе."""
        pass

    @abstractmethod
    async def get_info(self, url: str) -> Dict[str, Any]:
        """Возвращает метаданные: название, превью, длительность."""
        pass

    @abstractmethod
    async def get_formats(self, url: str) -> List[Dict[str, Any]]:
        """Возвращает список доступных форматов."""
        pass

    @abstractmethod
    async def download(self, url: str, format_id: str) -> str:
        """Скачивает файл и возвращает путь."""
        pass
