from abc import abstractmethod
from pathlib import Path
from parser import Parser, Entry

class Generator(Parser):
    types: dict[str, str] = {}

    def get_type(self, entry: Entry):
        type = entry.type
        if type in self.types:
            return self.types[type]

        if type in self.defs:
            return type

        raise Exception(f"Unknown type: {type}")

    @abstractmethod
    def build(self) -> str:
        pass

    def process(self, output: str):
        schema = self.build()
        if output is None:
            print(schema)
        else:
            Path(output).write_text(schema)
