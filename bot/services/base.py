from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseDownloaderService(ABC):

    @abstractmethod
    async def validate(self, url: str) -> bool:
        pass

    @abstractmethod
    async def get_info(self, url: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_formats(self, url: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def download(self, url: str, format_id: str) -> str:
        pass
