#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020/12/18 9:53 上午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: new_generator.py
# @IDE     : PyCharm
# @GitHub  ：https://github.com/harveymei/

from stdnum.iso7064 import mod_37_36
import base62
import time
alphabet = base62.CHARSET_INVERTED
filename = input("请输入文件名：")

with open(filename) as f_obj:
    check_lists = []
    for line in f_obj:
        check_lists.append(line.rstrip())


for i in check_lists:
    segment_u = i[-12:]

    if mod_37_36.validate(segment_u, alphabet) == segment_u:
        print(segment_u + " is Valid.")

#    for full_serial_numbers, check_digits in zip(full_serial_numbers, check_digits):
#        full_codes = full_c + full_g + full_serial_numbers + check_digits + "\n"
#        f_obj.write(full_codes)
