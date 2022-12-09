# coding:utf-8
# @Time     : 2021/8/3
# @Author   : fisher yu
# @File     : sky_earth.py

import argparse
from datetime import date

SKY = "甲、乙、丙、丁、戊、已、庚、辛、壬、癸"
EARTH = "子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥"
BASE_YEAR = 2021
BASE_SEXAGENARY = "辛丑"


def build_chinese_sexagenary_cycle():
    sky = SKY.split("、")
    earth = EARTH.split("、")
    count = 0
    sexagenary_cycle = []
    while True:
        if count % len(sky) == 0 and count % len(earth) == 0 and count != 0:
            break
        sexagenary_cycle.append("{s}{e}".format(s=sky[count % len(sky)], e=earth[count % len(earth)]))
        count += 1
    return sexagenary_cycle


def calculate_year(year, sexagenary_cycle):
    base_sexagenary_index = sexagenary_cycle.index(BASE_SEXAGENARY)
    if year == BASE_YEAR:
        return BASE_SEXAGENARY
    elif year < BASE_YEAR:
        diff_year = (BASE_YEAR - year) % 60
        index = base_sexagenary_index - diff_year
        return sexagenary_cycle[index]
    else:
        diff_year = (year - BASE_YEAR) % 60
        index = base_sexagenary_index + diff_year
        return sexagenary_cycle[index]


def show_chinese_sexagenary_cycle(sexagenary_cycle, step=6):
    for x in range(0, len(sexagenary_cycle), step):
        print(sexagenary_cycle[x: x + step])


def main():
    parser = argparse.ArgumentParser(description="计算指定年份的天干地支")
    parser.add_argument("-y", "--year", type=int, default=date.today().year, help="指定年份")
    parser.add_argument("-s", "--show", action="store_true", help="是否需要展示干支纪年表")
    args = parser.parse_args()
    cycle = build_chinese_sexagenary_cycle()
    if args.show:
        show_chinese_sexagenary_cycle(cycle)
    if args.year:
        result = calculate_year(args.year, cycle)
        print(result)


if __name__ == '__main__':
    main()
