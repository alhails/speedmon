#!/usr/bin/env python3

import os
import sys
import subprocess
import json
import click

__author__ = "Alastair Hails"


def cmd(args, cwd=None):
    try:
        ret = subprocess.check_output(args, cwd=cwd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        print('\nCommand failed!\n%s\n%s' % (' '.join(error.cmd), error.output))
        return (False, None)
    return (True, ret)

@click.group()
def main():
    """
    CLI for running speed tests
    """
    pass

@main.command()
@click.option("--fmt", "-f", default="")
def exec(fmt):
    (ok, ret) = cmd(['speedtest', '-f', 'json']) 
    if not ok:
        sys.exit(os.EX_SOFTWARE) 
    results = json.loads(ret)
    dlBytes = results['download']['bytes']
    dlElapsed = results['download']['elapsed']
    dlRate = (dlBytes / dlElapsed) / 125 # Convert to Mbps
    ts = results['timestamp']

    if fmt == "csv":
        print("{0},{1}".format(ts,dlRate))
    else:
        print("Download:   {0:.0f} Mbps".format(dlRate))
    





if __name__ == "__main__":
    main()
