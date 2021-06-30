# coding:utf-8
# @Time     : 2021/6/29
# @Author   : fisher yu
# @File     : file_hash.py

"""
file hash: v0.0.1
"""

import argparse
import hashlib
import os

chunkSize = 8 * 1024


def valid_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return True
    return False


def file_md5(file_path, block_size=chunkSize):
    if not valid_file(file_path):
        return None, None
    md5tool = hashlib.md5()
    with open(file_path, 'rb') as fn:
        while True:
            data = fn.read(block_size)
            if not data:
                break
            md5tool.update(data)
    md5value = md5tool.hexdigest()
    # md5b64 = base64.b64encode(md5tool.digest())
    return md5value


def file_sha1(file_path, block_size=chunkSize):
    if not valid_file(file_path):
        return None, None
    sha1tool = hashlib.sha1()
    with open(file_path, 'rb') as fn:
        while True:
            data = fn.read(block_size)
            if not data:
                break
            sha1tool.update(data)
    sha1value = sha1tool.hexdigest()
    # sha1b64 = base64.b64encode(sha1tool.digest())
    return sha1value


def batch_md5(files: list):
    md5dict = {}
    for file in files:
        md5value = file_md5(file)  # Thread here
        if not md5value:
            continue
        if file not in md5dict:
            md5dict[file] = {}
        # md5dict[file]['md5b64'] = md5b64
        md5dict[file]['md5value'] = md5value

    return md5dict


def batch_sha1(files: list):
    sha1dict = {}
    for file in files:
        sha1value = file_sha1(file)
        if not sha1value:
            continue
        if file not in sha1dict:
            sha1dict[file] = {}
        # sha1dict[file]['sha1b64'] = sha1b64
        sha1dict[file]['sha1value'] = sha1value
    return sha1dict


def merge_digest(sha1dict: dict, md5dict: dict):
    digest_dict = {}
    for file in sha1dict:
        if file not in digest_dict:
            digest_dict[file] = {}
        # digest_dict[file]['sha1b64'] = sha1dict[file]['sha1b64']
        digest_dict[file]['sha1value'] = sha1dict[file]['sha1value']

    for file in md5dict:
        if file not in digest_dict:
            digest_dict[file] = {}
        # digest_dict[file]['md5b64'] = md5dict[file]['md5b64']
        digest_dict[file]['md5value'] = md5dict[file]['md5value']

    return digest_dict


def main():
    parser = argparse.ArgumentParser(description='Compute the file digest.')
    parser.add_argument('paths', metavar='/path/to/file', type=str, nargs='*', help='A file path')
    parser.add_argument('--sha1', dest='sha1', action='store_true', help='Show sha1 digest')
    parser.add_argument('--md5', dest='md5', action='store_true', help='Show md5 digest')
    parser.add_argument('-dup', '--find-duplicate', dest='duplicate', action='store_true', help='Find Duplicate file')
    parser.add_argument('-i', '--input-file', dest='input', type=str, help='A file stores some file waiting hash')
    args = parser.parse_args()
    if not args.paths and not args.input:
        print('[-]Error: One file path at least.')
        exit(0)
    if args.input and not os.path.exists(args.input) and not os.path.isfile(args.input):
        print('[-]Error: input file not exists or not a file.')
        exit(0)

    paths = args.paths if args.paths else []
    if args.input:
        with open(args.input, 'r') as fn:
            for line in fn.readlines():
                formatted_line = line.strip('\r').strip('\n').strip('')
                if formatted_line:
                    paths.append(formatted_line)

    sha1dict = {}
    if args.sha1:
        sha1dict = batch_sha1(paths)
    md5dict = batch_md5(paths)
    digest_dict = merge_digest(sha1dict, md5dict)

    if args.duplicate:
        hash_dict = {}
        for file, file_hash in digest_dict.items():
            hash_key = file_hash['md5value']
            if hash_key not in hash_dict:
                hash_dict[hash_key] = {}

            length = len(hash_dict[hash_key])
            file_key = 'file{}'.format(str(length))
            hash_dict[hash_key][file_key] = file

        for hash_key in hash_dict.keys():
            if len(hash_dict[hash_key]) >= 2:
                print('file md5: {}'.format(hash_key))
                for value in hash_dict[hash_key].values():
                    print('\t{}'.format(value))

    if args.md5 and args.sha1:
        print(digest_dict)
    elif args.md5:
        print(md5dict)
    elif args.sha1:
        print(sha1dict)


if __name__ == '__main__':
    main()
