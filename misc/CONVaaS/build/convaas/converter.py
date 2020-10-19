import json
import logging.config
import os
import sys
from configparser import ConfigParser
from logging import Logger, Manager  # type: ignore
from pathlib import Path
from typing import (
    IO,
    Any,
    Callable,
    DefaultDict,
    Dict,
    List,
    NamedTuple,
    Optional,
    Union,
)

import click
import toml
import yaml
from packaging.version import parse as parse_version

logger: Logger = logging.getLogger(__name__)

CONVAAS_VERSION: str = "1.0.0"

debug: bool = False
verbosity_loglevel_map: DefaultDict[int, int] = DefaultDict(
    lambda: logging.DEBUG, {0: logging.WARNING, 1: logging.INFO}
)


class Document(NamedTuple):
    dump: Callable[[Any, IO], Any]
    load: Callable[[IO], Any]


def _ini_load(fp: IO) -> dict:
    config: ConfigParser = ConfigParser()
    config.read_file(fp)
    return {s: dict(config[s]) for s in config.sections()}


def _yaml_load(stream: Union[IO, str]) -> dict:
    return dict(yaml.safe_load(stream))


def _ini_dump(obj: Any, fp: IO) -> None:
    config: ConfigParser = ConfigParser()
    config.read_dict(obj)
    config.write(fp)


def _json_dump(obj: Any, fp: IO) -> None:
    json.dump(obj, fp, indent=2, ensure_ascii=False)
    fp.write("\n")


def _yaml_dump(obj: Any, fp: IO) -> None:
    yaml.safe_dump(obj, fp, allow_unicode=True)


documents: Dict[str, Document] = dict(
    ini=Document(load=_ini_load, dump=_ini_dump),
    json=Document(load=json.load, dump=_json_dump),
    toml=Document(load=toml.load, dump=toml.dump),
    yaml=Document(load=_yaml_load, dump=_yaml_dump),
)


def load(fp: IO, doctype: str) -> Any:
    if doctype not in documents:
        raise ValueError("not supported input format")
    return documents[doctype].load(fp)


def dump(obj: Any, fp: IO, doctype: str) -> None:
    if doctype not in documents:
        raise ValueError("not supported output format")
    documents[doctype].dump(obj, fp)


def set_logging(config: dict) -> bool:
    global logger
    try:
        logging.config.dictConfig(config)
    except Exception as e:
        logger.warning(f"could not load config for logging: {e}")
        if debug:
            logger.exception(e)
        return False
    else:
        logger = logging.getLogger(Path(__file__).stem)
        # Delete the '__name__' logger
        manager: Manager = getattr(logging.root, "manager", None)
        if manager is not None:
            del manager.loggerDict[__name__]
    return True


def parse_config(stream: Union[str, IO]) -> dict:
    if not isinstance(stream, str) and not isinstance(stream, IO):
        raise TypeError("'stream' should be str or IO")
    return dict(yaml.safe_load(stream))


def configure(config: dict) -> None:
    global debug

    # Validate config version
    version: Optional[Union[str, int]] = config.get("version", None)
    if version is None:
        raise KeyError("Version information not found")
    if not isinstance(version, int) and not isinstance(version, str):
        raise TypeError("Version information should be int or str")
    if parse_version(str(version)) > parse_version(CONVAAS_VERSION):
        raise ValueError(f"Not supported version: '{version}'")

    # Extract configs
    common_config: Optional[dict] = config.get("common", None)
    dedicated_config: Optional[dict] = config.get(Path(__file__).stem, None)

    # Put data into each dedicated data store
    verbosity_loglevel_map_config: Optional[List[str]] = None
    logging_config: dict = {}
    if common_config is not None:
        logging_config.update(common_config.get("logging", {}))
        verbosity_loglevel_map_config = common_config.get(
            "verbosity_loglevel_map", None
        )
    if dedicated_config is not None:
        logging_config.update(dedicated_config.get("logging", {}))
        verbosity_loglevel_map_config = dedicated_config.get(
            "verbosity_loglevel_map", None
        )

    # Apply the config for logging
    if logging_config and set_logging(logging_config):
        debug |= logger.getEffectiveLevel() == logging.DEBUG

    if verbosity_loglevel_map_config is not None:
        for i, level in enumerate(verbosity_loglevel_map_config):
            verbosity_loglevel_map[i] = getattr(logging, level, logging.DEBUG)


@click.group(help=f"A CLI tool to convert {'/'.join(documents)} to each other.")
@click.option("--config", "-c", type=Path, help="Specify config file.")
@click.option("--verbose", "-v", count=True, help="Set verbosity level.")
def cli(config: Optional[Path], verbose: int) -> None:
    global debug

    # Apply basic config for logging
    logging.basicConfig(level=verbosity_loglevel_map[verbose])
    debug |= verbosity_loglevel_map[verbose] == logging.DEBUG

    # Apply custom config
    if config is not None:
        try:
            configure(parse_config(config.read_text()))
        except Exception as e:
            if debug:
                logger.exception(e)
            logger.warning(f"could not apply the config: '{config}'")
        else:
            logger.setLevel(verbosity_loglevel_map[verbose])
            for handler in logger.handlers:
                handler.setLevel(verbosity_loglevel_map[verbose])


@cli.command("list", help="Show supported document types.")
def list_document_type() -> None:
    print("\n".join(documents))
    sys.exit(os.EX_OK)


@cli.command(help="Convert documents.")
@click.argument("infile", default=Path("/dev/stdin"), required=False, type=Path)
@click.argument("outfile", default=Path("/dev/stdout"), required=False, type=Path)
@click.option("--input-type", type=str)
@click.option("--output-type", type=str)
def convert(
    infile: Path,
    outfile: Path,
    input_type: Optional[str],
    output_type: Optional[str],
) -> None:
    if infile.name == "-":
        infile = Path("/dev/stdin")

    if not infile.exists():
        logger.error(f"'{infile}' not found")
        sys.exit(os.EX_NOINPUT)

    if infile.suffix[1:] not in documents and input_type is None:
        logger.error("could not determine input type")
        sys.exit(os.EX_SOFTWARE)

    if outfile.suffix[1:] not in documents and output_type is None:
        logger.error("could not determine output type")
        sys.exit(os.EX_SOFTWARE)

    try:
        with infile.open() as fp:
            obj: Any = load(fp, input_type or infile.suffix[1:])
    except Exception as e:
        if debug:
            logger.exception(e)
        logger.error(f"could not load content from '{infile}'")
        sys.exit(os.EX_DATAERR)

    try:
        with outfile.open("w") as fp:
            dump(obj, fp, output_type or outfile.suffix[1:])
    except Exception as e:
        if debug:
            logger.exception(e)
        logger.error(f"could not dump content to '{outfile}'")
        sys.exit(os.EX_CANTCREAT)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    cli(obj={})
