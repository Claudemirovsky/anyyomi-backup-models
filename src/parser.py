from abc import abstractmethod, ABC
from dataclasses import dataclass
from source.source import Source, SourceEntry
import re

@dataclass
class Entry:
    repeated: bool
    required: bool
    number: int
    type: str
    name: str
    match: str

class Parser(ABC):
    regex = re.compile(
        r"^\s*(?!\/\/\s*)@ProtoNumber\((?P<number>\d+)\)\s+va[rl]\s+(?P<name>\w+):\s+(?:(?:List<(?P<list>\w+)>)|(?P<type>\w+))(?P<optional>\?|(:?\s+=))?",
        re.MULTILINE
    )
    """
    The magic regex
 
    The kotlin models are build with class properties like
    - @ProtoNumber(2) var url: String
    - @ProtoNumber(3) var title: String = ""
    - @ProtoNumber(6) var description: String?
    - @ProtoNumber(7) var genre: List<String>
    
    This regex match 5 groups  
    - number: the protobuf field number (inside ProtoNumber)  
    - name: the field name ("url" in the first example)  
    - list: the type if it's a list ("String" in the fourth example)  
    - type: the type if not a list ("String" in the other example)  
    - optional: if the field if optional (match " =" in second example and "?" in third example)  
    
    some field are commented (used in 1.x, not in 0.x), so we must not match it (negative group with "//")
    """

    defsRegex = re.compile(
        r"class (?P<name>\w+)\((?P<defs>(?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*)\)",
        re.MULTILINE
    )
    """Definition regex. Matches classes and properties"""

    defs: dict[str, list[Entry]] = {}
    """Parsed definition"""

    _source: Source
    """Source models provider"""

    _addInvalid: bool = False

    def __init__(self, source: Source, addInvalid: bool = False):
        self._source = source
        self._addInvalid = addInvalid

    def loadDefinition(self):
        """
        Loads and parses all models
        """
        dir = self._source.readDir()

        for entry in dir:
            self.parseFile(entry)

        if not self._addInvalid:
            invalid = [
                name for name, entries in self.defs.items() 
                    if any([entry.number == 0 for entry in entries])
            ]
                      
            for name in self.defs:
                if name in invalid:
                    del self.defs[name]
                else:
                    self.defs[name] = [
                        entry for entry in self.defs[name]
                            if entry.type not in invalid
                    ]
 
    def parseFile(self, sourceEntry: SourceEntry):
        """
        Parses a model file
        """
        file = self._source.readFile(sourceEntry)

        for foundDefs in Parser.defsRegex.finditer(file):
            entries: list[Entry] = []

            for entry in Parser.regex.finditer(foundDefs.group("defs")):
                entries.append(
                    Entry(
                        repeated=bool(entry["list"]),
                        required=not bool(entry["optional"]),
                        number=int(entry["number"]),
                        type=entry["list"] or entry["type"],
                        name=entry["name"],
                        match=entry[0]
                    )
                )

            if len(entries) != len(self.regex.findall(foundDefs["defs"])):
                raise Exception(f"Not all @ProtoNumber matched in {foundDefs['name']}\n  matched: {', '.join(map(lambda x: x.name, entries))}")
            
            if len(entries) > 0:
                self.defs[foundDefs['name']] = entries

    @abstractmethod
    def process(self, output: str | None):
        pass
