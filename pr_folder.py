# coding   : utf-8
# @Time    : 2019/12/1 11:13
# @Author  : fisher
# @File    : pr_folder.py

__author__ = 'fisher yu'

import argparse
import os.path
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", help="set the pr project root folder", type=str)
    parser.add_argument("-n", "--name", help="set the pr project folder name", type=str)

    # parse args
    args = parser.parse_args()
    root_folder = args.root
    folder_name = args.name

    if not root_folder or not folder_name:
        print("root and name can not be empty string")
        sys.exit(1)

    folder_name = folder_name.strip('/')
    folder_name = folder_name.strip('\\')

    # check root exists
    if not os.path.exists(root_folder):
        print("root folder:%s not exists" % root_folder)
        sys.exit(1)

    # check folder name conflict
    project_path = os.path.join(root_folder, folder_name)
    if os.path.exists(project_path):
        print("project folder: %s already exists" % project_path)
        sys.exit(1)

    # create pr resource folder
    os.mkdir(project_path)
    print("create %s" % project_path)
    sub_folders = ['audio', 'video', 'other', 'picture', 'result']
    for item in sub_folders:
        sub_folder = os.path.join(project_path, item)
        print("create %s" % sub_folder)
        os.mkdir(sub_folder)


if __name__ == "__main__":
    parse_arguments()
