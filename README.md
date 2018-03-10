# wikidata-updater

Tool to import data to wikidata.

## Installation

run
```
$ git clone https://github.com/marisanest/wikidata-updater.git
```

## Configuration

Run
```
$ cp config.yaml.sample config.yaml
```
and fill out the config.yaml. The mail parameters only need to be set if you run the script with --mail (see below).

## Usage

The calling syntax is
```
$ python src/main.py [--mail]

```
When the --mail flag is set, an email will be send if an error occurs or the import is finished.

## License

The source code is licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3.