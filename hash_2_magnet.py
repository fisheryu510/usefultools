# coding:utf-8
# @Time     : 2020/3/18
# @Author   : fisher yu
# @File     : hash_2_magnet.py

"""
磁力链接参考: https://baike.baidu.com/item/%E7%A3%81%E5%8A%9B%E9%93%BE%E6%8E%A5/5867775?fr=aladdin
"""
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description="Concat magnet hash to magnet link, version 0.0.1")
    parser.add_argument("-hs", help="the magnet hash", type=str)
    parser.add_argument("-dn", help="the display name for user", type=str)

    args = parser.parse_args()
    if not args.hs:
        print("hash must be set")
        sys.exit(1)
    if not args.dn:
        dn = None
    else:
        dn = args.dn
    return args.hs, dn


def main():
    hash, dn = parse_arguments()
    usable_magnet = "magnet:?xt=urn:btih:{hash}".format(hash=hash)
    if dn:
        dn_part = "&dn={dn}".format(dn=dn)
        full_magnet = usable_magnet + dn_part
        print(full_magnet)
    else:
        print(usable_magnet)


if __name__ == '__main__':
    main()
