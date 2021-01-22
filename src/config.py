from pygrader.utils import error

from paths import (
    GITHUB_GROUPS_CSV_PATH,
    GITHUB_INDIVIDUAL_CSV_PATH,
)


def get_github_csv_col_name(tag):
    if tag == "Lab0":
        return "Lab0"
    elif tag == "Lab1":
        return "Lab1"
    elif tag == "Lab3":
        return "Lab3"
    elif tag == "Lab4":
        return "Lab4"
    elif tag == "Lab5":
        return "Lab5"
    elif tag == "LabSim":
        return "LabSim"
    elif tag == "Lab7":
        return "Lab7"
    elif tag == "Lab8":
        return "Lab8"
    elif tag == "Lab9":
        return "Lab9"
    elif tag == "Lab10":
        return "Lab10"
    elif tag == "Lab11":
        return "Lab11"
    error("Unhandled tag", tag, "in get_github_csv_col_name()")


def get_github_csv_path(tag):
    if tag.startswith("lab3"):
        return GITHUB_GROUPS_CSV_PATH
    else:
        return GITHUB_INDIVIDUAL_CSV_PATH
