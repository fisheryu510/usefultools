# coding:utf-8
# @Time     : 2019/12/29
# @Author   : fisher yu
# @File     : markdown_index.py

"""
将Markdown文件中的标题抽取出来转换为索引，供外部导航
"""
import re
import argparse
import sys
import os

H1_TAG = ('h1', "^# ", "# ")
H2_TAG = ('h2', "^## ", "## ")
H3_TAG = ('h3', "^### ", "### ")
H4_TAG = ('h4', "^#### ", "#### ")
H5_TAG = ('h5', "^##### ", "##### ")
H6_TAG = ('h6', "^###### ", "###### ")

TAG_POOL = (H1_TAG, H2_TAG, H3_TAG, H4_TAG, H5_TAG, H6_TAG)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract title tag in markdown and generate index")
    parser.add_argument("-t", "--tag", help="set the markdown title tag, from h1 to h6", type=str)
    parser.add_argument("-f", "--file", help="the markdown file path", type=str)
    parser.add_argument("-p", "--prefix", help="the prefix of generated link", type=str, default="")

    args = parser.parse_args()
    index_tag = args.tag
    md_file = args.file
    prefix = args.prefix

    if not index_tag and not md_file:
        print("tag and file is required")
        sys.exit(1)
    if not os.path.exists(md_file):
        print("file not exists, please check your file path")
        sys.exit(1)
    return index_tag, md_file, prefix


def main():
    index_tag, md_file, prefix = parse_arguments()
    markdown = MarkdownIndexExtractor(md_file, index_tag, prefix)
    try:
        markdown.bind_pattern()
        markdown.extract()
        markdown.make_index()
    except ValueError as ex:
        print(str(ex))
        sys.exit(1)


class MarkdownIndexExtractor:

    def __init__(self, md_file, index_tag, link_prefix=""):
        self.md_file = md_file
        self.index_tag = index_tag
        self.link_prefix = link_prefix
        self.remove_str = None
        self.pattern = None
        self.result = []

    def bind_pattern(self):
        for key, pattern, remove in TAG_POOL:
            if key == self.index_tag:
                self.pattern = re.compile(pattern)
                self.remove_str = remove
                return
        raise ValueError("Not matched any Markdown tag")

    def extract(self):
        with open(self.md_file, encoding='utf-8') as markdown:
            content = markdown.readlines()
        for line in content:
            if self.pattern.match(line):
                self.result.append(line.replace(self.remove_str, ""))

    def make_index(self):
        index_template = "- [{}]({}{}#{})"
        file_name = self.md_file[self.md_file.rindex("/") + 1:]

        for item in self.result:
            index = index_template.format(item.strip(), self.link_prefix, file_name, item.strip())
            print(index)


if __name__ == '__main__':
    main()
