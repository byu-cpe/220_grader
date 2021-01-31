#!/Users/nelson/opt/anaconda3/envs/pygrader/bin/python3

# Import the needed files
import argparse
import pathlib
import sys
import os

# Need to tell where to look for various imports that are to occur next
sys.path.append(str(pathlib.Path(__file__).parent / "src"))
sys.path.append(str(pathlib.Path(__file__).parent / "third_party" / "pygrader"))

# Here are the imports that need the above search path
from pygrader import CodeSource, Grader
from pygrader.utils import TermColors, error
from paths import (
    ROOT_PATH,
    GITHUB_GROUPS_CSV_PATH,
    GITHUB_INDIVIDUAL_CSV_PATH,
    LEARNING_SUITE_PATH,
)
import config

# Here is the list of the lab names
lab_names = [
    "Lab0",
    "Lab1",
    "Lab3",
    "Lab4",
    "Lab5",
    "LabSim",
    "Lab6",
    "Lab7",
    "Lab8",
    "Lab9",
    "Lab10",
    "Lab11",
]


def get_passoff_csv_header_name(tag):
    if tag == "Lab0":
        return ("Lab0",)
    elif tag == "Lab1":
        return ("Lab1",)
    elif tag == "Lab3":
        return ("Lab3",)
    elif tag == "Lab4":
        return ("Lab4",)
    elif tag == "Lab5":
        return ("Lab5",)
    elif tag == "Lab6":
        return ("Lab6",)
    elif tag == "Lab7":
        return ("Lab7",)
    elif tag == "Lab8":
        return ("Lab8",)
    elif tag == "Lab9":
        return ("Lab9",)
    elif tag == "Lab10":
        return ("Lab10",)
    elif tag == "Lab11":
        return ("Lab11",)
    error("Unhandled tag argument (" + tag + ") provided to get_passoff_csv_header_name()")













# Points per lab
def get_passoff_points(tag):
    if tag == "Lab0":
        return 20
    elif tag == "Lab1":
        return 20
    elif tag == "Lab2":
        return 20
    elif tag == "Lab3":
        return 20
    elif tag == "Lab4":
        return 20
    elif tag == "Lab5":
        return 20
    elif tag == "LabSim":
        return 20
    elif tag == "Lab6":
        return 20
    elif tag == "Lab7":
        return 20
    elif tag == "Lab8":
        return 20
    elif tag == "Lab9":
        return 20
    elif tag == "Lab10":
        return 20
    elif tag == "Lab11":
        return 20
    error("Unhandled tag argument (" + tag + ") provided to get_passoff_points()")


def get_csv_path_passoff(tag):
    if tag.startswith("lab3"):
        return LEARNING_SUITE_PATH / "lab3_passoff_grades.csv"
    elif tag.startswith("lab4"):
        return LEARNING_SUITE_PATH / "lab4_passoff_grades.csv"
    else:
        return LEARNING_SUITE_PATH / (tag + "_grades.csv")

def RunLab(lab_name, student_code_path, build, run, first_names, last_names, net_ids, modified_time=None, section=None, homework_id=None):
    print("\nRunLab called with params: {} {} {} {} {} {} {}...".format(lab_name, student_code_path, build, run, first_names, last_names, net_ids,
                                                                        modified_time, section, homework_id))

    # Add student homework_id to bottom of file in preparation for correcting
    feedback = ROOT_PATH / (lab_name + ".fdbk")
    with open(feedback, "a") as f:
        f.write("######################################\n")
        f.write("Student_name = {} {} ({})\n".format(last_names[0], first_names[0], net_ids[0]))
        f.write("Homework_id = {}\n".format(homework_id[0]))
        f.write("Feedback = \n")
        f.write("######################################\n")
    #os.system("code --wait -g {} {}:1000".format(student_code_path, feedback))
    #print("Done with callback...")

# The main routine
def main():
    # Set up command line args
    parser = argparse.ArgumentParser()
    # A lab name will be required, legal choices given by the 'lab_names' variable above
    parser.add_argument("lab_name", choices=lab_names)
    # Add an arg that will just do a build (named --build_only)
    parser.add_argument(
        "--build_only",
        action="store_true",
        help="Just clone and build the student repos, but don't run.  "
        "Use this to start it all off and walk away.  Come back later and do the grading.",
    )
    # Parse the command line given using the above arg definitions
    args = parser.parse_args()

    # Create a Grader object.  The code for it was imported from pygrader way up above (based on the paths given)
    grader = Grader(
        "passoff",
        lab_name=args.lab_name,
        points=(get_passoff_points(args.lab_name),),
        work_path=ROOT_PATH,
        code_source=CodeSource.LEARNING_SUITE,
        #grades_csv_path=get_csv_path_passoff(args.lab_name),
        grades_csv_path=ROOT_PATH / "Labs.csv",
        grades_col_names=get_passoff_csv_header_name(args.lab_name),
        github_csv_path=config.get_github_csv_path(args.lab_name),
        github_csv_col_name=config.get_github_csv_col_name(args.lab_name),
        github_tag=args.lab_name,
        build_only=args.build_only,
        run_on_lab=RunLab,
        learning_suite_submissions_zip_path=ROOT_PATH / (args.lab_name + ".zip"),
    )

    # Call the grader object's run method and that is it
    grader.run()


# This just calls the main routine when you do run the file either as ./run_passoff.py or as python3 run_passoff.py
if __name__ == "__main__":
    main()
