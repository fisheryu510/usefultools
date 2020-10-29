# coding:utf-8
# @Time     : 2020/10/29
# @Author   : fisher yu
# @File     : image_2_pdf.py

"""
图形文件批量转换为PDF文件
有缺陷：文件排序规则需要在list_images()函数中自行修改，不管是os.walk()还是os.listdir()
需要安装reportlab: pip install reportlab
"""

import argparse
import os
import sys
import time

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

LEFT_SLASH = "/"
RIGHT_SLASH = "\\"
SUPPORTED_IMAGE_FORMAT = [".jpg", ".jpeg", ".png"]


def time_str():
    return time.strftime("%Y-%m-%d_%H_%M_%S")


def entry():
    parser = argparse.ArgumentParser(description="Images to PDF")
    parser.add_argument("-d", "--dir", help="The directory of picture. Can't be empty", type=str)
    parser.add_argument("-n", "--name", help="The final name of PDF file. Optional", type=str)

    args = parser.parse_args()
    root_folder = args.dir
    pdf_name = args.name

    if not root_folder:
        print("Picture directory can not be empty string")
        sys.exit(1)

    if not os.path.exists(root_folder) or not os.path.isdir(root_folder):
        print("Picture directory:%s not exists or not a valid directory" % root_folder)
        sys.exit(1)

    if not pdf_name or LEFT_SLASH in pdf_name or RIGHT_SLASH in pdf_name:
        pdf_name = "%s.pdf" % time_str()
    else:
        pdf_name = "%s.pdf" % pdf_name

    # print(root_folder, pdf_name)
    return root_folder, pdf_name


def list_images(folder: str):
    valid_images = []

    # for sub_file in os.listdir(folder): filename need be sort
    for root, dirs, files in os.walk(folder):  # filename need be sort
        for sub_file in files:
            print(sub_file)
            sub_file_suffix = os.path.splitext(sub_file)[-1]
            if sub_file_suffix in SUPPORTED_IMAGE_FORMAT:
                full_path = os.path.join(folder, sub_file)
                # print("Find image file: %s" % full_path)
                valid_images.append(full_path)
    return valid_images


def images_2_pdf(images: list, pdf_name: str, folder: str):
    pdf_path = os.path.join(folder, pdf_name)
    (w, h) = landscape(A4)
    cv = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    for image in images:
        cv.drawImage(image, 0, 0, w, h)
        cv.showPage()
    cv.save()


def main():
    root_folder, pdf_name = entry()
    valid_images = list_images(root_folder)
    images_2_pdf(valid_images, pdf_name, root_folder)


if __name__ == '__main__':
    main()
