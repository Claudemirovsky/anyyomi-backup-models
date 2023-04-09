from generator import Generator
from parser import Entry

class Protobuf(Generator):
    # kotlin type mapping
    types = {
        "String": "string",
        "Char": "string",
        "Int": "int32",
        "Long": "int64",
        "Boolean": "bool",
        "Float": "float",
        # TODO: better handling of enum,
        # this should be auto discovered
        "UpdateStrategy": "int32",
    }
    """Kotlin -> Protobuf type mapping"""

    def build(self) -> str:
        lines = ['syntax = "proto2";', '']
        for name in self.defs:
            lines.append(f"message {name} {{")
            
            for entry in self.defs[name]:
                fieldType = self.get_type(entry)
                attribute = self.get_attribute(entry)
                lines.extend([
                    f"  // {entry.match.strip()}".replace("\n", ""),
                    f"  {attribute} {fieldType} {entry.name} = {entry.number};"
                ])
            
            lines.extend(["}", ""])  
        return '\n'.join(lines)

    def get_attribute(self, entry: Entry) -> str:
        if entry.repeated:
            return "repeated"
        if entry.required:
            return "required"
        return "optional"
