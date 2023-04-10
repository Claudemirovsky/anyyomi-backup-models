from dataclasses import dataclass
from source.source import Source, SourceEntry
import requests

@dataclass
class FileEntry(SourceEntry):
    name: str
    download_url: str

class GithubSource(Source):
    API_URL: str = "https://api.github.com/repos"
    PATH: str = "app/src/main/java/eu/kanade/tachiyomi/data/backup/models"
    branch: str = ""

    def __init__(self, config: str, branch: str = "master"):
        self.config = config
        self.branch = branch

    def _readDirRecursively(self, session: requests.Session, dir: str) -> list[FileEntry]:
        url = f"{self.API_URL}/{self.config}/contents/{dir}?ref={self.branch}"
        response = session.get(url)
        json = response.json()
        files: list[FileEntry] = []
        for item in json:
            if item["type"] == "dir":
                files.extend(self._readDirRecursively(session, item["path"]))
            elif item["type"] == "file":
                files.append(
                    FileEntry(
                        name=item["name"],
                        download_url=item["download_url"]
                    )
                )

        return files

    def readDir(self) -> list[FileEntry]:
        with requests.Session() as session:
            return self._readDirRecursively(session, self.PATH)

    def readFile(self, entry: FileEntry) -> str:
        return requests.get(entry.download_url).text

