import subprocess

from pygrader.utils import error, print_color, TermColors


def is_module_loaded(mod_name):
    p = subprocess.run(
        [
            "lsmod",
        ],
        stdout=subprocess.PIPE,
    )

    lsmod_output = p.stdout.decode().splitlines()[1:]

    return mod_name in [line.split()[0] for line in lsmod_output]


def remove_module(mod_name):
    p = subprocess.run(["sudo", "rmmod", mod_name])
    if p.returncode:
        print_color(TermColors.YELLOW, "could not remove_module", mod_name)
        raise OSError


def remove_module_if_loaded(mod_name):
    if is_module_loaded(mod_name):
        remove_module(mod_name)


def insert_module(mod_path):
    p = subprocess.run(["sudo", "insmod", str(mod_path)])
    if p.returncode:
        print_color(TermColors.YELLOW, "could not insert_module", mod_path)
        raise OSError
