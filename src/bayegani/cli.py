from pathlib import Path

import click

from bayegani.descriptor_loader import FileDescriptorLoader


@click.group()
def cli():
    pass


@cli.command()
@click.argument('descriptor_path', type=click.Path(exists=True))
def worker(descriptor_path: str):
    descriptor_loader = FileDescriptorLoader(
        file_path=Path(descriptor_path),
    )

    worker_instance = descriptor_loader.get_worker()

    try:
        worker_instance.setup()
        worker_instance.start()
    finally:
        worker_instance.teardown()