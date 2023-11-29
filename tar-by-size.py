#! /usr/bin/env python3

from pathlib import Path
import os
import click
import tarfile
from itertools import count


def tarfiles_gen(prefix):
    for i in count():
        tar = tarfile.open(Path(prefix + "." + str(i) + ".tar"), mode="w")
        yield tar
        tar.close()


@click.command()
@click.option("--folder", "-f", type=click.Path(exists=True), required=True)
@click.option("--target-prefix", "-t", type=str, required=True)
@click.option("--max-size", "-s", type=int, required=True, help="Size in GB")
def main(folder, target_prefix, max_size):
    folder = Path(folder)
    max_size = max_size * 2**30
    size = 0
    tarfiles = tarfiles_gen(target_prefix)
    tar = next(tarfiles)
    for directory, _, files in os.walk(folder):
        for file in files:
            filepath = Path(directory, file)
            size += filepath.stat().st_size
            if size > max_size:
                # rotate tarball
                tar = next(tarfiles)
                size = 0
                click.echo(f"Rolled tarball. Now writing into {tar.name}")
            tar.add(filepath, filepath.relative_to(folder))
    tar.close()


if __name__ == "__main__":
    main()
