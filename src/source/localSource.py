from dataclasses import dataclass
from pathlib import Path
from source.source import Source, SourceEntry

@dataclass
class FileEntry(SourceEntry):
    name: str
    path: Path

class LocalSource(Source):
    def readDir(self) -> list[FileEntry]:
        dir: list[FileEntry] = []
        for file in Path(self.config).rglob("*"):
            if file.is_file():
                dir.append(
                    FileEntry(
                        name=file.name,
                        path=file.absolute()
                    )
                )
        return dir
    
    def readFile(self, entry: FileEntry) -> str:
        return entry.path.read_text()

