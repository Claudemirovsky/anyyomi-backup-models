from generator import Generator

class Protobuf(Generator):
    # kotlin type mapping
    types = {
        "String": "string",
        "Int": "int32",
        "Long": "int64",
        "Boolean": "bool",
        "Float": "float",
        # TODO: better handling of enum,
        # this should be auto discovered
        "UpdateStrategy": "int32",
    }

    def build(self) -> str:
        lines = ['syntax = "proto2";', '']
        for name in self.defs:
            lines.append(f"message {name} {{")
            
            for entry in self.defs[name]:
                lines.extend([
                    f"  // {entry.match.strip()}",
                    f"  {'repeated' if entry.repeated else 'required' if entry.required else 'optional'} {self.get_type(entry)} {entry.name} = {entry.number};"
                ])
            
            lines.extend(["", "}"])  
        return '\n'.join(lines)

