from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class SourceEntry:
    name: str

class Source(ABC):
    config: str = ""

    def __init__(self, config: str):
        self.config = config

    @abstractmethod
    def readDir(self) -> list[SourceEntry]:
        pass
    
    @abstractmethod
    def readFile(self, entry: SourceEntry) -> str:
        pass
