# coding:utf-8
# @Time     : 2022/4/8
# @Author   : fisher yu
# @File     : FileCounter.py

import sys
import os
import argparse

'''
指定路径下的文件格式统计
微软视频 ：wmv、asf、asx
Real Player ：rm、 rmvb
MPEG视频 ：mp4
手机视频 ：3gp
Apple视频 ：mov、m4v
其他常见视频：avi、dat、mkv、flv、vob等
https://baike.baidu.com/item/%E8%A7%86%E9%A2%91%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F/6641989?fr=aladdin
https://baike.baidu.com/item/%E5%9B%BE%E7%89%87%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F/1989798?fr=aladdin
'''

VIDEO_FORMAT = ('mp4', 'wmv', 'ts', 'avi', 'mkv', 'rm',
                'rmvb', 'asf', 'asx', '3gp', 'mov', 'm4v',
                'dat', 'flv', 'vob')
TEXT_FORMAT = ('txt', 'json', 'pdf', 'doc', 'docx', 'ppt',
               'pptx', 'xls', 'xlsx', 'csv', 'md')
PIC_FORMAT = ('png', 'jpg', 'jpeg', 'gif', 'webp', 'tiff', 'psd', 'svg', 'bmp')
CODE_FORMAT = ('java', 'html', 'js', 'css', 'py', 'cpp', 'cxx', 'c', 'h', 'go', 'sh')


def main():
    path, wanted_format = parse_cmd()
    file_dic = count_file(path, wanted_format)
    show_result(file_dic)


def parse_cmd():
    parser = argparse.ArgumentParser(description='File Counter Version 0.01')
    parser.add_argument('-f', '--format', help='show specified file format', type=str)
    parser.add_argument('-c', '--category', help='show specified file group',
                        choices=('video', 'text', 'pic', 'code'))
    parser.add_argument('-p', '--path', help='file path, must be specified', type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("Please ensure the file path is valid")
        sys.exit(0)

    wanted_format = args.format
    wanted_category = args.category
    if not wanted_format and not wanted_category:
        print("Please specify file format or catrgory")
        sys.exit(0)

    format_filter = None
    if wanted_category:
        if wanted_category == 'video':
            format_filter = VIDEO_FORMAT
        elif wanted_category == 'text':
            format_filter = TEXT_FORMAT + CODE_FORMAT
        elif wanted_category == 'pic':
            format_filter = PIC_FORMAT
        elif wanted_category == 'code':
            format_filter = CODE_FORMAT
    else:
        format_filter = (wanted_format,)
    return args.path, format_filter


def get_file_suffix(file):
    try:
        suffix_index = file.rindex('.')
    except ValueError:
        return None
    return file[suffix_index + 1:]


def count_file(path, wanted_format):
    file_dic = {}
    for parent, subdir, files in os.walk(path):
        for file in files:
            suffix = get_file_suffix(file)
            if suffix in wanted_format:
                full_path = os.path.join(parent.replace(path, ''), file)
                if suffix not in file_dic:
                    file_dic[suffix] = [full_path]
                else:
                    file_dic[suffix].append(full_path)
    return file_dic


def show_result(file_dic):
    total_files = 0
    for item, files in file_dic.items():
        total_files += len(files)
        print('{format} file: {number}'.format(format=item, number=len(files)))
        for file in files:
            print(file)
    print('Total: {total} files.'.format(total=total_files))


if __name__ == '__main__':
    main()
