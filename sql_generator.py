# coding:utf-8
# @Time     : 2020/6/22
# @Author   : fisher yu
# @File     : sql_generator.py


import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='read a dict from json file and generate insert and update sql')
    parser.add_argument('-f', '--file', help='json file path, not null', type=str)
    parser.add_argument('-o', '--out', help='file to save sql', type=str, default='')

    args = parser.parse_args()
    if not args.file:
        print('no json file to read')  # No need to check file exists on disk, throw error when read file
        sys.exit(1)
    return args.file, args.out


def read_dict(file):
    with open(file, 'r', encoding='utf-8') as f:
        template = json.load(f)

    if not isinstance(template, dict):
        print('the json file\'s content must be a dict, json file reference: sql.json')
        print('such as {"k1": "v1", "k2": "v2"}')
        sys.exit(1)

    return template


def gen_insert_sql(template: dict):
    sql_columns, sql_indicators = [], []
    for key in template.keys():
        sql_columns.append('`%s`' % key)
        sql_indicators.append('%%(%s)s' % key)
    columns = ', '.join(sql_columns)
    indicators = ', '.join(sql_indicators)
    insert_template = 'insert into `table_name`(%s) values(%s)' % (columns, indicators)
    return insert_template


def gen_update_sql(template: dict):
    set_values = []
    for key in template.keys():
        set_values.append('`%s` = %%(%s)s' % (key, key))

    updates = ', '.join(set_values)
    update_template = 'update `table_name` set %s' % updates
    return update_template


def main():
    json_file, sql_file = parse_args()
    tpl = read_dict(json_file)
    insert_sql = gen_insert_sql(tpl)
    update_sql = gen_update_sql(tpl)
    if sql_file:
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(insert_sql)
            f.write('\n')
            f.write(update_sql)
    else:
        print(insert_sql)
        print(update_sql)


if __name__ == '__main__':
    main()
