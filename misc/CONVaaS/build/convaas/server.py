import asyncio
import logging.config
import os
import pwd
import shlex
import shutil
import sys
import tempfile
from asyncio import (
    AbstractEventLoop,
    AbstractServer,
    Event,
    StreamReader,
    StreamWriter,
    Task,
)
from asyncio.subprocess import Process
from logging import Logger, Manager  # type: ignore
from pathlib import Path
from pwd import struct_passwd
from signal import SIGHUP, SIGINT, SIGTERM, Signals
from stat import S_IRGRP, S_IRUSR, S_IWGRP, S_IWUSR, S_IXGRP, S_IXUSR
from typing import IO, Any, Callable, DefaultDict, List, Optional, Tuple, Union

import click
import yaml
from packaging.version import parse as parse_version

logger: Logger = logging.getLogger(__name__)

CONVAAS_BANNER: str = """
 ██████╗ ██████╗ ███╗   ██╗██╗   ██╗ █████╗  █████╗ ███████╗
██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔══██╗██╔══██╗██╔════╝
██║     ██║   ██║██╔██╗ ██║██║   ██║███████║███████║███████╗
██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══██║██╔══██║╚════██║
╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ██║  ██║██║  ██║███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
  __ __    ___ _  _ ___
 / /_\\ \\  |_ _| \\| |_ _|
< <___> >  | || .` || |
 \\_\\ /_/  |___|_|\\_|___|
  __ __       _ ___  ___  _  _
 / /_\\ \\   _ | / __|/ _ \\| \\| |
< <___> > | || \\__ \\ (_) | .` |
 \\_\\ /_/   \\__/|___/\\___/|_|\\_|
  __ __    _____ ___  __  __ _
 / /_\\ \\  |_   _/ _ \\|  \\/  | |
< <___> >   | || (_) | |\\/| | |__
 \\_\\ /_/    |_| \\___/|_|  |_|____|
  __ __   __   ___   __  __ _
 / /_\\ \\  \\ \\ / /_\\ |  \\/  | |
< <___> >  \\ V / _ \\| |\\/| | |__
 \\_\\ /_/    |_/_/ \\_\\_|  |_|____|

"""
CONVAAS_CONVERTER: str = "converter.py"
CONVAAS_VERSION: str = "1.0.0"
MAX_DATA_SIZE: int = 1024

convaas_host: str = os.getenv("CONVAAS_HOST", "127.0.0.1")
convaas_port: int = int(os.getenv("CONVAAS_PORT", 0xD0C0))
convaas_user: str = os.getenv("CONVAAS_USER", "convaas")
convaas_basedir: str = os.getenv("CONVAAS_BASEDIR", tempfile.gettempdir())
converter_config: Optional[dict] = None
converter_config_file: str = "convaas.yaml"
debug: bool = False
document_types: List[str] = []
verbosity_loglevel_map: DefaultDict[int, int] = DefaultDict(
    lambda: logging.DEBUG, {0: logging.WARNING, 1: logging.INFO}
)


class ContentSizeError(ValueError):
    pass


class DocumentTypeError(ValueError):
    pass


async def setup_workdir(event: Event) -> Path:
    # Create a working directory
    workdir: Path = Path(tempfile.mkdtemp(dir=convaas_basedir))
    workdir.chmod(S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP)
    shutil.chown(workdir, workdir.owner(), convaas_user)
    logger.debug(f"{workdir=}")

    # Copy the converter to the working directory
    converter: Path = Path(CONVAAS_CONVERTER)
    new_converter: Path = Path(workdir / CONVAAS_CONVERTER)
    new_converter.write_text(converter.read_text())
    new_converter.chmod(S_IRUSR | S_IWUSR | S_IRGRP)
    shutil.chown(new_converter, converter.owner(), convaas_user)

    # Copy the logging config to the working directory
    if converter_config is not None:
        new_converter_config_file = Path(workdir / converter_config_file)
        with new_converter_config_file.open("w") as fp:
            yaml.safe_dump(converter_config, fp)
        new_converter_config_file.chmod(S_IWUSR | S_IRUSR | S_IRGRP)
        shutil.chown(new_converter_config_file, convaas_user, convaas_user)

    # Reserve cleanup of the working directory
    asyncio.create_task(cleanup_workdir(event, workdir))
    return workdir


async def cleanup_workdir(event: Event, workdir: Path) -> None:
    # Delete all files in the working directory
    if await event.wait() and workdir.exists():
        shutil.rmtree(workdir)
        logger.info(f"cleaned up the working directory, '{workdir}'")


def init_converter(username: str) -> Callable[[], None]:
    def _init_converter() -> None:
        # Drop privileges
        logger.debug(f"{os.getuid()=}, {os.getgid()=}, {os.getgroups()=}")
        passwd: struct_passwd = pwd.getpwnam(username)
        os.setgroups(os.getgrouplist(passwd.pw_name, passwd.pw_gid))
        os.setresgid(passwd.pw_gid, os.getgid(), os.getgid())
        os.setresuid(passwd.pw_uid, os.getuid(), os.getuid())
        logger.debug(f"{os.getuid()=}, {os.getgid()=}, {os.getgroups()=}")

        # Set environment variables
        os.putenv("HOME", passwd.pw_dir)
        os.putenv("HISTFILE", "/dev/null")

    return _init_converter


async def execute_converter(*args, **kwargs) -> bytes:
    # Construct arguments
    program: str = sys.executable
    arguments: List[str] = [CONVAAS_CONVERTER]
    if converter_config is not None:
        arguments += ("--config", converter_config_file)
    arguments += args

    # Run the converter
    logger.info(f"executing `{shlex.join([program]+arguments)}`")
    proc: Process = await asyncio.create_subprocess_exec(
        program,
        *arguments,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
        preexec_fn=init_converter(convaas_user),
        **kwargs,
    )

    # Get an output or an error
    output: bytes
    error: bytes
    output, error = await proc.communicate()
    return output if proc.returncode == 0 else error


async def prompt(writer: StreamWriter, message: str, prompt: str = ">") -> None:
    writer.write(f"{message} {prompt} ".encode())
    await writer.drain()


async def prompt_string(
    reader: StreamReader, writer: StreamWriter, message: str
) -> str:
    await prompt(writer, message)
    return (await reader.readline()).decode().strip()


async def prompt_int(
    reader: StreamReader, writer: StreamWriter, message: str
) -> Optional[int]:
    s: str = await prompt_string(reader, writer, message)
    return int(s) if s.isdigit() else None


async def prompt_bytes(
    reader: StreamReader, writer: StreamWriter, message: str, n: int
) -> bytes:
    await prompt(writer, message)
    return await reader.readexactly(n)


async def prepare_converter(
    reader: StreamReader, writer: StreamWriter, workdir: Path
) -> Tuple[str, str]:
    # Get the file name from the client and validate it
    filename: str = os.path.basename(
        await prompt_string(
            reader, writer, f"Input filename ({'/'.join(document_types)})"
        )
    )
    logger.debug(f"{filename=}")
    path: Path = Path(workdir.absolute() / filename)
    logger.debug(f"{path=}")
    if not path.suffix[1:] in document_types:
        raise DocumentTypeError("Invalid input document type")

    # Get the size of the content supplied by the client and validate it
    size: Optional[int] = await prompt_int(
        reader, writer, f"Size of content (0, {MAX_DATA_SIZE}]"
    )
    logger.debug(f"{size=}")
    if size is None or size > MAX_DATA_SIZE or size <= 0:
        raise ContentSizeError("Empty or invalid size")

    # Get the content from the client
    content: bytes = await prompt_bytes(reader, writer, "Content", size)
    logger.debug(f"{content=}")
    path.write_bytes(content)

    # Get the output type from the client and validate it
    output_type: str = await prompt_string(
        reader, writer, f"Output type ({'/'.join(document_types)})"
    )
    logger.debug(f"{output_type=}")
    if output_type not in document_types:
        raise DocumentTypeError("Invalid output document type")

    # Perform conversion and return it.
    return path.name, output_type


async def handle_client(reader: StreamReader, writer: StreamWriter) -> None:

    event: Event = Event()
    try:
        peername: Any = writer.get_extra_info("peername")
        logger.info(f"connection from {peername!r}")

        # Start conversion
        workdir: Path = await setup_workdir(event)
        logger.info(f"set up a new working directory, '{workdir}'")

        writer.write(CONVAAS_BANNER.encode())
        await writer.drain()

        # Get arguments for the converter
        filename: str
        output_type: str
        filename, output_type = await prepare_converter(reader, writer, workdir)

        # Run the converter
        result: bytes = await execute_converter(
            "convert", "--output-type", output_type, filename, cwd=workdir
        )

        # Send the result to the client
        writer.write(b"\n")
        writer.write(b"--- CONVERSION RESULT ---\n")
        writer.write(result)
        writer.write(b"-------------------------\n")
        await writer.drain()
    except ConnectionResetError:
        logger.error("connection closed by client")
    except (DocumentTypeError, ContentSizeError) as e:
        logger.error(f"invalid data from client: {e}")
        writer.write(f"Invalid data: {e}\n".encode())
        await writer.drain()
    except (asyncio.IncompleteReadError, asyncio.LimitOverrunError, ValueError) as e:
        logger.error(f"incomplete or too large data from client: {e}")
        writer.write(f"Incomplete or too large data: {e}\n".encode())
        await writer.drain()
    except Exception as e:
        logger.exception(e)
        writer.write(b"An unexpected error occured.\n")
    finally:
        writer.close()

    event.set()


async def main(
    host: str, port: int, basedir: Optional[str] = None, user: Optional[str] = None
) -> None:
    global convaas_basedir, convaas_user

    if basedir is not None:
        convaas_basedir = basedir
    if user is not None:
        convaas_user = user

    # Create base directory for working directory with permission `rwx-wx---`
    path: Path = Path(convaas_basedir)
    try:
        path.mkdir(S_IRUSR | S_IWUSR | S_IXUSR | S_IWGRP | S_IXGRP, True, True)
        shutil.chown(path, path.owner(), convaas_user)
    except Exception as e:
        if debug:
            logging.exception(e)
        logging.warning("could not create base for working directory")

    # Set the available document types
    for doctype in (await execute_converter("list")).split():
        document_types.append(doctype.decode())
    logger.debug(f"{document_types=}")

    # Start the server
    lhp: Tuple[str, int] = (host, port)
    server: AbstractServer = await asyncio.start_server(handle_client, *lhp)
    logger.info(f"serving on {lhp!r}")
    async with server:
        await server.serve_forever()


async def shutdown(loop: AbstractEventLoop, signal: Optional[Signals] = None) -> None:
    logger.debug(f"{type(loop)=}")
    if signal is not None:
        logger.info(f"received {signal.name}")

    logger.info("shutting down...")

    # Cancel all tasks except itself
    tasks: List[Task] = [
        task for task in asyncio.all_tasks() if task is not asyncio.current_task()
    ]
    logger.info(f"cancelling {len(tasks)} tasks...")
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    # Then, stop the loop
    logger.info("stopping the event loop...")
    loop.stop()


def handle_exception(loop: AbstractEventLoop, context: dict) -> None:
    logger.debug(f"{context=}")
    message: str = context.get("exception", context["message"])
    logger.error(f"caught an exception: {message}")
    asyncio.create_task(shutdown(loop))


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
    global convaas_host, convaas_port, convaas_user, convaas_basedir, converter_config
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
        convaas_host = dedicated_config.get("host", convaas_host)
        convaas_port = dedicated_config.get("port", convaas_port)
        convaas_user = dedicated_config.get("user", convaas_user)
        convaas_basedir = dedicated_config.get("basedir", convaas_basedir)

    # Apply the config for logging
    if logging_config and set_logging(logging_config):
        debug |= logger.getEffectiveLevel() == logging.DEBUG

    if verbosity_loglevel_map_config is not None:
        for i, level in enumerate(verbosity_loglevel_map_config):
            verbosity_loglevel_map[i] = getattr(logging, level, logging.DEBUG)

    if "converter" in config:
        converter_config = dict(
            version=version, common=common_config, converter=config["converter"]
        )


@click.command(help="CONVerter as a Service")
@click.option("--host", "-H", help="Specify hostname to listen.")
@click.option("--port", "-p", type=int, help="Specify port number to listen.")
@click.option("--user", "-u", help="Specify user for running.")
@click.option("--basedir", "-b", help="Specify base of working directory.")
@click.option("--config", "-c", type=Path, help="Specify config file.")
@click.option("--verbose", "-v", count=True, help="Set verbosity level.")
def cli(
    host: Optional[str],
    port: Optional[int],
    user: Optional[str],
    basedir: Optional[str],
    config: Optional[Path],
    verbose: int,
) -> None:
    global converter_config_file, debug

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
            converter_config_file = config.name
            logger.setLevel(verbosity_loglevel_map[verbose])
            for handler in logger.handlers:
                handler.setLevel(verbosity_loglevel_map[verbose])

    # Set the handlers for general exceptions and some signals
    loop: AbstractEventLoop = asyncio.get_event_loop()
    signals: Tuple[Signals, ...] = (SIGHUP, SIGINT, SIGTERM)
    for signal in signals:
        loop.add_signal_handler(
            signal, lambda s=signal: asyncio.create_task(shutdown(loop, signal=s))
        )
    loop.set_exception_handler(handle_exception)

    # Start the event loop
    try:
        loop.create_task(
            main(host or convaas_host, port or convaas_port, basedir, user)
        )
        loop.run_forever()
    finally:
        loop.close()
        logger.info("Successfully shutdown")

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    cli()
