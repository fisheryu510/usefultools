# coding:utf-8
# @Time     : 2020/3/22
# @Author   : fisher yu
# @File     : GPR.py

"""
GPR = go path replace
Test file: style1.go style2.go
Please backup original go source file before testing
backup file can not endswith .go, recommend using .go.bak
"""

import argparse
import copy
import os
import pathlib
import sys


def print_error(err):
    print(err, file=sys.stderr)


def parse_arguments():
    description = """
    replace the go package import path, version 0.1
    such as: go-proj/pkg1/utils => go-proj/pkg2/utils
    python gpr.py -d dest -op go-proj/pkg1 -np go-proj/pkg2 -ap 1
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--dest", type=str, help="The project dictionary or file")
    parser.add_argument("-op", "--original-package", type=str, help="The package path need to be replaced")
    parser.add_argument("-np", "--new-package", type=str, help="The new package path")
    parser.add_argument("-ap", "--add-go-path", type=bool, default=False,
                        help="The GOPATH is need to be added automatically, default is false")

    args = parser.parse_args()
    if not args.original_package or not args.new_package or not args.dest:
        print_error("Error: op or np param is required")
        sys.exit(1)

    if args.dest == "." or args.dest == "":
        path = os.path.abspath(".")
    else:
        path = args.dest

    return path, args.original_package, args.new_package, args.add_go_path


def _get_gopath() -> (str, bool):
    go_path = os.environ.get("GOPATH")
    if not go_path:
        return None, False
    else:
        return go_path, True


def prepare_path(input_dir: str, ap: bool):
    if ap:
        path, success = _get_gopath()
        if not success:
            print("Error: GOPATH env is not configured")
            sys.exit(1)
        if path.endswith("/"):
            path = path[:-1]
        if input_dir.startswith("/"):
            input_dir = input_dir[1:]
        full_path = path + "/src/" + input_dir
    else:
        full_path = input_dir

    path_obj = pathlib.Path(full_path)
    if not path_obj.exists():
        print("Error: {full_path} is not exists".format(full_path=full_path))
        sys.exit(1)

    print("Work on:" + full_path)
    return path_obj.is_dir(), full_path


"""
if this function is poor efficiency, 
consider using subdir execute many times or rewrite by multiprocess
"""


def fetch_go_files(dir):
    def handle_error(err):
        print(err)

    go_files = []

    for root, dirs, files in os.walk(dir, onerror=handle_error):
        for name in files:
            if name.endswith(".go"):
                go_file = os.path.join(root, name)
                # print("found a go source file: {path}".format(path=go_file))
                go_files.append(go_file)
    return go_files


def change_import(go_file, origin="", new=""):
    with open(go_file, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        new_lines = copy.deepcopy(lines)
        for index, org_line in enumerate(lines):
            line = copy.deepcopy(org_line)
            line = line.strip()
            if line.startswith("func") or line.startswith("type") \
                    or line.startswith("var") or line.startswith("const"):
                break
            new_line = org_line.replace(origin, new)
            new_lines[index] = new_line
        f.seek(0)
        for line in new_lines:
            if line.endswith("\n"):
                f.write(line)
            else:
                f.write(line + "\n")


def main():
    d, op, np, ap = parse_arguments()
    # print(d, op, np, ap)
    is_dir, full_path = prepare_path(d, ap)
    if is_dir:
        go_files = fetch_go_files(full_path)
    else:
        go_files = [full_path]
    for go_file in go_files:
        print("Deal file: " + go_file)
        change_import(go_file, op, np)


if __name__ == '__main__':
    main()
