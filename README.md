# wikidata-updater

Tool to update items on wikidata.

## Installation

```
$ git clone https://github.com/marisanest/wikidata-updater.git
```

## Configuration

```
$ cp config.yaml.sample config.yaml
```
Fill out the config.yaml. The mail parameters only need to be set if you run the script with --mail (see below).

## Usage

The calling syntax is
```
$ python src/main.py [--mail]
```
where when the --mail flag is set, an email will be send if an error occurs or the update is finished.

## License

The source code is licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3.