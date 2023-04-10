import argparse
from protobuf import Protobuf
from source.source import Source
from source.localSource import LocalSource
from source.githubSource import GithubSource

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-b", "--branch", help="Github repo branch", action="store", default="master")
    args.add_argument("-r", "--repo", help="Github repo (user/repo_name)", action="store", default="tachiyomiorg/tachiyomi")
    args.add_argument("-d", "--dir", help="models dir", action="store")
    args.add_argument("-o", "--output", help="output file", action="store")
    parsed = args.parse_args()

    source: Source = LocalSource(parsed.dir) if parsed.dir else GithubSource(parsed.repo, parsed.branch)
    parser = Protobuf(source, True)
    parser.loadDefinition()
    parser.process(parsed.output)
