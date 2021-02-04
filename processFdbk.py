import argparse

def readFdbkRecord(f):
    ret = ""
    looping = True
    while looping:
        s = f.readline()
        if s == "":
            return None
        if s.startswith("######################################"):
            looping = False
    # Skip student name
    f.readline()
    # Read homework id line
    s = f.readline().strip()
    hwid = s.split(' ')[2]
    ret += (s + "\n")
    # Read "Feedback = " line
    ret += f.readline()
    # Read feedback
    looping = True
    while looping:
        s = f.readline()
        if s.startswith("######################################\n"):
            looping = False
        else:
            ret += s
    return (hwid, ret)

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

# The main routine
def main():
    # Set up command line args
    parser = argparse.ArgumentParser()
    # A lab name will be required, legal choices given by the 'lab_names' variable above
    parser.add_argument("lab_name", choices=lab_names)

    # Parse the command line given using the above arg definitions
    args = parser.parse_args()

    fdbk = dict()

    # Read the feedback records from the file and put into dictionary
    # If a hwid shows up twice, the last feedback will be kept
    with open(args.lab_name + ".fdbk", 'r') as f:
        while True:
            tmp = readFdbkRecord(f)
            if tmp is None:
                break;
            fdbk[tmp[0]] = tmp[1]

    # Write out the records
    with open(args.lab_name + ".feedback", 'w') as f:
        for hwid, rec in fdbk.items():
            f.write("################################\n")
            f.write(rec)
            f.write("################################\n")

# This just calls the main routine when you do run the file either as ./run_passoff.py or as python3 run_passoff.py
if __name__ == "__main__":
    main()
