import subprocess
import time
import shutil
import os

from pygrader.utils import print_color, TermColors, error

from paths import RESOURCES_PATH
from kernel_utils import remove_module_if_loaded, insert_module


class BuildFailed(Exception):
    pass


def run_lab(lab_name, student_code_path, **kwargs):
    # Run git show and run the built code
    cmd = ["git", "log", "-1", r"--format=%cd"]
    proc = subprocess.run(cmd, cwd=str(student_code_path))


def build_userspace(student_path):
    print_color(TermColors.BLUE, "Building userspace code")
    build_path = student_path / "userspace" / "build"
    build_path.mkdir(parents=True, exist_ok=True)

    if not (build_path / "Makefile").is_file():
        p = subprocess.run(["cmake", ".."], cwd=str(build_path))
        if p.returncode:
            print_color(TermColors.YELLOW, "cmake failed")
            raise BuildFailed

    p = subprocess.run(["make", "-j4"], cwd=str(build_path))
    if p.returncode:
        print_color(TermColors.YELLOW, "make failed")
        raise BuildFailed


def build_kernel_audio(student_path):
    build_path = student_path / "kernel" / "lab4_audio_codec"
    p = subprocess.run(
        [
            "make",
        ],
        cwd=str(build_path),
    )
    if p.returncode:
        print_color(TermColors.YELLOW, "make failed")
        raise BuildFailed

def build_pit(student_path):
    build_path = student_path / "kernel" / "lab6_pit"
    p = subprocess.run(
        [
            "make",
        ],
        cwd=str(build_path),
    )
    if p.returncode:
        print_color(TermColors.YELLOW, "make failed")
        raise BuildFailed


def run_exe(exe_path, exe_cwd, student_path, args=None, nonblocking=False):
    if not exe_path.is_file():
        print_color(TermColors.YELLOW, exe_path, "does not exist.")
        raise FileNotFoundError

    cmd = ["sudo", str(exe_path)]
    if args is not None:
        cmd += args

    # run the code from the student's build directory
    try:
        print_color(TermColors.BLUE, "Running", exe_path.relative_to(student_path))
        if nonblocking:
            return subprocess.Popen(cmd, cwd=str(exe_cwd))
        else:
            subprocess.run(cmd, cwd=str(exe_cwd))
            return None
    except KeyboardInterrupt:
        pass
    except PermissionError:
        pass


def run_milestone(lab_name, student_code_path, build, run, **kwargs):
    """ Run build (or other such scripts) for a given lab submission """

    # path to the build directory
    build_path = student_code_path / "userspace" / "build"

    # set the proper exe_path based on the tag given
    if lab_name == "lab1_passoff":
        if build:
            try:
                build_userspace(student_code_path)
            except BuildFailed:
                return
        if run:
            try:
                run_exe(
                    build_path / "apps" / "lab1_helloworld" / "helloworld",
                    build_path,
                    student_code_path,
                )
            except FileNotFoundError:
                return

    elif lab_name == "lab2_passoff":
        if build:
            try:
                build_userspace(student_code_path)
            except BuildFailed:
                return
        if run:
            try:
                run_exe(build_path / "apps" / "clock" / "clock", build_path, student_code_path)
            except FileNotFoundError:
                return

    elif lab_name in ("lab3_m1_passoff", "lab3_m2_passoff", "lab3_m3_passoff"):
        if build:
            try:
                build_userspace(student_code_path)
            except BuildFailed:
                return
        if run:
            try:
                run_exe(
                    build_path / "apps" / "space_invaders" / "space_invaders",
                    build_path,
                    student_code_path,
                )
            except FileNotFoundError:
                return

    elif lab_name == "lab4_m1_passoff":
        if build:
            try:
                build_userspace(student_code_path)
                build_kernel_audio(student_code_path)
            except BuildFailed:
                return

        if run:
            # Clear dmesg
            subprocess.run(["sudo", "dmesg", "-c"])

            print_color(TermColors.BLUE, "Inserting audio_codec.ko")
            try:
                remove_module_if_loaded("audio_codec")
                insert_module(student_code_path / "kernel" / "lab4_audio_codec" / "audio_codec.ko")
            except OSError:
                return

            exe_path = build_path / "apps" / "lab4_m1" / "lab4_m1"
            try:
                run_exe(exe_path, build_path, student_code_path)
            except FileNotFoundError:
                return

            print_color(TermColors.BLUE, "Re-Inserting audio_codec.ko")
            try:
                remove_module_if_loaded("audio_codec")
                insert_module(student_code_path / "kernel" / "lab4_audio_codec" / "audio_codec.ko")
            except OSError:
                return

            try:
                run_exe(exe_path, build_path, student_code_path)
            except FileNotFoundError:
                return

            subprocess.run(
                [
                    "dmesg",
                ]
            )

    elif lab_name == "lab4_m2_passoff":
        if build:
            try:
                build_userspace(student_code_path)
                build_kernel_audio(student_code_path)
            except BuildFailed:
                return

        if run:
            print_color(TermColors.BLUE, "Inserting audio_codec.ko")
            try:
                remove_module_if_loaded("audio_codec")
                insert_module(student_code_path / "kernel" / "lab4_audio_codec" / "audio_codec.ko")
            except OSError:
                return

            exe_path = build_path / "apps" / "lab4_m2" / "lab4_m2"
            wav_path = RESOURCES_PATH / "wav" / "ufo_die.wav"
            try:
                run_exe(
                    exe_path,
                    build_path,
                    student_code_path,
                    args=[
                        str(wav_path),
                    ],
                )
            except FileNotFoundError:
                return

    elif lab_name == "lab4_m3_passoff":
        if build:
            try:
                build_userspace(student_code_path)
                build_kernel_audio(student_code_path)
            except BuildFailed:
                return

        if run:
            print_color(TermColors.BLUE, "Inserting audio_codec.ko")
            try:
                remove_module_if_loaded("audio_codec")
                insert_module(student_code_path / "kernel" / "lab4_audio_codec" / "audio_codec.ko")
            except OSError:
                return

            try:
                run_exe(
                    build_path / "apps" / "space_invaders" / "space_invaders",
                    build_path,
                    student_code_path,
                )
            except FileNotFoundError:
                return

    elif lab_name == "lab6_passoff":
        if build:
        #comment above line and uncomment line below to skip build on run
        #if build and not run:
            try:
                build_userspace(student_code_path)
                build_kernel_audio(student_code_path)
                build_pit(student_code_path)
            except BuildFailed:
                return
        if run:
            boot_bin_path = student_code_path / "device_tree" / "boot" / "BOOT.bin"
            if not boot_bin_path.is_file():
                print_color(TermColors.YELLOW, boot_bin_path, "is missing.")
                return
            dtb_path = student_code_path / "device_tree" / "dtb" / "devicetree.dtb"
            if not dtb_path.is_file():
                print_color(TermColors.YELLOW, dtb_path, "is missing.")
                return
            
            # get the last commit time for the BOOT.bin and devicetree.dtb files
            # run the commands in shell and get their output

            # for BOOT.bin
            git_output = subprocess.run("git log -n 1 --pretty=format:%cd -- " + str(boot_bin_path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(student_code_path), shell=True)
            print(boot_bin_path.name, "last modified time in git: ", str(git_output.stdout))

            # for devicetree.dtb
            git_output = subprocess.run("git log -n 1 --pretty=format:%cd -- " + str(dtb_path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(student_code_path), shell=True)
            print(dtb_path.name, "last modified time in git: ", str(git_output.stdout))

            txtInput = ""
            while txtInput not in ("c", "r", "s"):
                txtInput = input("Copy (c) over boot files and reboot, run (r) space invaders, or skip (s)?")
            if txtInput == "s":
                return
            elif txtInput == "c":
                # copy the binary files into boot directory
                subprocess.run("sudo cp " + str(boot_bin_path) + " /boot/BOOT.bin", shell=True)
                subprocess.run("sudo cp " + str(dtb_path) + " /boot/devicetree.dtb", shell=True)
                # execute reboot command
                subprocess.run("sudo shutdown -r now", shell=True)
            elif txtInput == "r":
                remove_module_if_loaded("audio_codec")
                remove_module_if_loaded("pit")
                print_color(TermColors.BLUE, "Inserting audio_codec.ko")
                insert_module(student_code_path / "kernel" / "lab4_audio_codec" / "audio_codec.ko")
                print_color(TermColors.BLUE, "Inserting pit.ko")
                insert_module(student_code_path / "kernel" / "lab6_pit" / "pit.ko")

                #variable to store output from runs
                run_out = 0

                print("printing intialized values in the PIT before sending any:\n")
                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/int_en', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from int_en: ", run_out.stdout)

                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/period', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from period: ", run_out.stdout)

                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/run', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from run: ", run_out.stdout)

                # sending values and reading
                print_color(TermColors.BLUE, "sending 1 to int_en")
                subprocess.run('sudo bash -c "echo 1 > /sys/class/pit_427/pit_427/int_en"', shell=True)

                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/int_en', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from int_en: ", run_out.stdout)

                print_color(TermColors.BLUE, "sending 10000 to period")
                subprocess.run('sudo bash -c "echo 10000 > /sys/class/pit_427/pit_427/period"', shell=True)

                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/period', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from period: ", run_out.stdout)

                print_color(TermColors.BLUE, "sending 1 to run")
                subprocess.run('sudo bash -c "echo 1 > /sys/class/pit_427/pit_427/run"', shell=True)

                run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/run', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print_color(TermColors.YELLOW, "read value from run: ", run_out.stdout)
                try:
                    p = run_exe(
                        build_path / "apps" / "space_invaders" / "space_invaders",
                        build_path,
                        student_code_path,
                        nonblocking=True
                    )
                    time.sleep(2)
                    input("Press enter to change PIT period to 30000")
                    subprocess.run('sudo bash -c "echo 30000 > /sys/class/pit_427/pit_427/period"', shell=True)

                    run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/period', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                    print_color(TermColors.YELLOW, "read value from period: ", run_out.stdout)

                    input("Press enter to change PIT period back to 10000")
                    subprocess.run('sudo bash -c "echo 10000 > /sys/class/pit_427/pit_427/period"', shell=True)

                    run_out = subprocess.run('sudo cat /sys/class/pit_427/pit_427/period', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                    print_color(TermColors.YELLOW, "read value from period: ", run_out.stdout)

                    input("Press enter when you're done.")
                    subprocess.run("sudo skill space_invaders", shell=True)
                except FileNotFoundError:
                    return
    else:
        error("Unhandled tag in run_lab_cmd()")
