# coding:utf-8
# @Time     : 2020/11/1
# @Author   : fisher yu
# @File     : ts_merge.py

"""
M3U8片段中的ts文件合并工具，合并后的ts文件将会转换为MP4格式
需要系统中安装FFmpeg工具
M3U8格式快速入门：https://www.cnblogs.com/renhui/p/10351870.html
M3U8格式-demo:
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:35232
#EXT-X-TARGETDURATION:10
#EXTINF:10.000,
cctv6hd-1549272376000.ts
#EXTINF:10.000,
cctv6hd-1549272386000.ts
#EXTINF:10.000,
cctv6hd-1549272396000.ts
#EXTINF:10.000,
cctv6hd-1549272406000.ts
#EXTINF:10.000,
cctv6hd-1549272416000.ts
#EXTINF:10.000,
cctv6hd-1549272426000.ts
"""

import argparse
import os
import subprocess
import sys
from tempfile import NamedTemporaryFile


class M3U8FileParser:
    TS_PART_KEY = "#EXTINF:"

    def __init__(self, file_path):
        self.file_path = file_path
        self.is_ts_part = False
        self.all_ts_file = []

    def parse(self):
        with open(self.file_path, 'r', encoding='utf-8') as m3u8:
            for line in m3u8:
                if self.is_ts_part:
                    parsed_line = line.strip("\n")
                    self.all_ts_file.append(parsed_line)
                    self.is_ts_part = False
                if line.startswith(self.TS_PART_KEY):
                    self.is_ts_part = True

        return self.all_ts_file


def merge_ts_part(ts_files: list, output: str):
    """
    合并短小的ts片段
    ffmpeg -i "1.ts|2.ts|3.ts|4.ts|.5.ts|" -c copy output.mp4
    :param ts_files:
    :param output:
    :return:
    """
    basic_cmd = "ffmpeg -i \"{ts_files_seq}\" -c copy {output}.mp4"
    all_ts_str = "|".join(ts_files)
    cmd = basic_cmd.format(ts_files_seq=all_ts_str, output=output)
    print(cmd)
    # subprocess.Popen(cmd, shell=True)
    try:
        subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        return -1
    return 0


def merge_ts_by_file(ts_file: str, output: str):
    """
    合并数量大的ts片段
    ffmpeg -f concat -i filelist.txt -c copy output.mp4
    :param ts_file:
    :param output:
    :return:
    """

    # 出现问题  Unsafe file name, 加入 -safe 0
    cmd = "ffmpeg -f concat -safe 0 -i {ts_file} -c copy {output}.mp4".format(ts_file=ts_file,
                                                                              output=output)
    try:
        print("exec %s" % cmd)
        subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        return -1
    return 0


def cmd_entry():
    parser = argparse.ArgumentParser(description="Merge ts files to a full video")
    parser.add_argument("-r", "--root", help="The directory of M3U8 file", type=str)
    parser.add_argument("-f", "--files", help="The directory of ts files", type=str)
    parser.add_argument("-s", "--store", help="[Optional] Video store directory", type=str)
    parser.add_argument('-o', '--output', help="[Optional] The final name of video", type=str)

    args = parser.parse_args()
    m3u8_dir = args.root
    ts_dir = args.files
    store_dir = args.store
    output = args.output

    if not m3u8_dir or not ts_dir:
        print("M3U8 directory and ts files directory can not be empty")
        sys.exit(1)

    if not os.path.exists(m3u8_dir) or not os.path.isdir(m3u8_dir):
        print("M3U8 directory is not valid")
        sys.exit(1)

    if not os.path.exists(ts_dir) or not os.path.isdir(ts_dir):
        print("TS file directory is not valid")
        sys.exit(1)

    m3u8_files = []
    for file in os.listdir(m3u8_dir):
        if file.endswith(".m3u8") or file.endswith(".M3U8"):
            m3u8_files.append(file)

    if not m3u8_files:
        print("There is no any m3u8 file in directory")
        sys.exit(1)

    if store_dir:
        if not os.path.exists(store_dir) or not os.path.isdir(store_dir):
            print("Story directory not exist")
            sys.exit(1)

    return m3u8_dir, m3u8_files, ts_dir, output, store_dir


def exec_merge(m3u8_dir, m3u8_files, ts_dir, output, store_dir):
    pwd = os.getcwd()
    for m3u8 in m3u8_files:
        sub_path = os.path.join(m3u8_dir, m3u8)
        parser = M3U8FileParser(sub_path)
        ts_files = parser.parse()
        missing_flag = False
        for ts_file in ts_files:  # 确保所有的ts文件都存在
            ts_path = os.path.join(ts_dir, ts_file)
            if not os.path.exists(ts_path) or not os.path.isfile(ts_path):
                print("%s file's ts file is missing: %s" % (m3u8, ts_file))
                missing_flag = True
                break
        if missing_flag:
            continue

        temp = NamedTemporaryFile(mode='w+', dir=pwd, delete=True)
        print("generate %s in %s" % (temp.name, pwd))

        for ts_file in ts_files:
            ts_path = os.path.join(ts_dir, ts_file)
            line_template = "file '{file}'\n"
            temp.write(line_template.format(file=ts_path))
        temp.seek(0)

        # 生成文件名
        if not output:
            output_name = m3u8
        else:
            if len(m3u8_files) > 1:
                output_name = "%s_%s" % (output, m3u8)
            else:
                output_name = output

        if store_dir:
            output_name = os.path.join(store_dir, output_name)

        ret_code = merge_ts_by_file(temp.name, output_name)
        if ret_code != 0:
            print("merge %s.m3u8 failed" % m3u8)


def main():
    m3u8_dir, m3u8_files, ts_dir, output, store_dir = cmd_entry()
    exec_merge(m3u8_dir, m3u8_files, ts_dir, output, store_dir)


if __name__ == '__main__':
    main()
