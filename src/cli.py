import argparse
from protobuf import Protobuf
from source.source import Source
from source.localSource import LocalSource

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--dir", help="models dir", action="store", required=True)
    args.add_argument("-o", "--output", help="output file", action="store")
    parsed = args.parse_args()

    source: Source = LocalSource(parsed.dir)
    parser = Protobuf(source, True)
    parser.loadDefinition()
    parser.process(parsed.output)
