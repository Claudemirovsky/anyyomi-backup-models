# Anyyomi-backup-models
A python port of [tachiyomi-backup-models](https://github.com/clementd64/tachiyomi-backup-models), with the purpose of manipulating backup models from tachiyomi and its forks, directly from its sources.

Like as the original version, this program can read backup models from local files or fetch them automatically from a remote github repository, and provides a protobuf output by default.

My reason to create this, instead of just contributing to the original project, is that i wanted to run this on my android phone (via termux), and Deno does not support Linux+ARM.

# Options
```bash
$ python src/cli.py -h
usage: cli.py [-h] [-b BRANCH] [-r REPO] [-d DIR] [-o OUTPUT] [-i]

options:
  -h, --help            show this help message and exit

Github:
  -b BRANCH, --branch BRANCH
                        Remote repo branch (default: master)
  -r REPO, --repo REPO  Remote repo address (user/repo_name) (default:
                        tachiyomiorg/tachiyomi)

Local:
  -d DIR, --dir DIR     Path to tachiyomi backup models (priority over github-
                        related options)

General:
  -o OUTPUT, --output OUTPUT
                        Output file (Stdout if not provided)
  -i, --add-invalid     Adds invalid types(BrokenBackup...), for backups
                        before v0.12.2, but breaks protoc compatibility.
```

# Usage examples
## Using remote models
#### Fetching models from the original tachiyomi repo and dumping the protobuf output into `default-tachiyomi.proto`
```
$ python src/cli.py -o default-tachiyomi.proto
```
#### Fetching models from the TachiyomiSY fork repo and dumping a generated protobuf data into the stdout
```
$ python src/cli.py -r jobobby04/TachiyomiSY
```

## Using local repos and models
#### Using models from a local TachiyomiAZ fork clone and dumping the protobuf output into `tachiAZ.proto`
```
$ git clone https://github.com/az4521/TachiyomiAZ
$ python src/cli.py -d TachiyomiAZ/app/src/main/java/eu/kanade/tachiyomi/data/backup/full/models -o tachiAZ.proto
```
#### Using models from a local TachiyomiJ2K fork clone and dumping a generated protobuf data with invalid types into`tachij2k.proto`
```
$ git clone https://github.com/Jays2Kings/tachiyomiJ2K
$ python src/cli.py -i -d tachiyomiJ2K/app/src/main/java/eu/kanade/tachiyomi/data/backup/models -o tachij2k.proto
```

# TODOs
- [ ] Automatically detect ENUMs
- [ ] Support Aniyomi-related backup models (currently fails thanks to `BackupPreferences` classes)
