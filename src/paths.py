import pathlib

ROOT_PATH = pathlib.Path(__file__).absolute().parent.parent
CODE_CHECKER_PATH = ROOT_PATH / "third_party" / "code_checker"
SCREENSHOTS_PATH = ROOT_PATH / "coding_standard_screenshots"
LEARNING_SUITE_PATH = ROOT_PATH / "learning_suite"
GITHUB_INDIVIDUAL_CSV_PATH = LEARNING_SUITE_PATH / "github_individual.csv"
GITHUB_GROUPS_CSV_PATH = LEARNING_SUITE_PATH / "github_groups.csv"
RESOURCES_PATH = ROOT_PATH / "resources"
