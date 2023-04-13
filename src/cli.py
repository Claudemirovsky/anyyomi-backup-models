#!/usr/bin/env python3
import argparse
from protobuf import Protobuf
from source.source import Source
from source.localSource import LocalSource
from source.githubSource import GithubSource

if __name__ == "__main__":
    args = argparse.ArgumentParser()

    remote = args.add_argument_group("Github")
    remote.add_argument("-b", "--branch", help="Remote repo branch (default: master)", action="store", default="master")
    remote.add_argument("-r", "--repo", help="Remote repo address (user/repo_name) (default: tachiyomiorg/tachiyomi)", action="store", default="tachiyomiorg/tachiyomi")

    local = args.add_argument_group("Local")
    local.add_argument("-d", "--dir", help="Path to tachiyomi backup models (priority over github-related options)", action="store")

    general = args.add_argument_group("General")
    general.add_argument("-o", "--output", help="Output file (Stdout if not provided)", action="store")
    general.add_argument("-i", "--add-invalid", help="Adds invalid types(BrokenBackup...), for backups before v0.12.2, but breaks protoc compatibility.", action="store_true")
    parsed = args.parse_args()

    source: Source = LocalSource(parsed.dir) if parsed.dir else GithubSource(parsed.repo, parsed.branch)
    parser = Protobuf(source, parsed.add_invalid)
    parser.loadDefinition()
    parser.process(parsed.output)
