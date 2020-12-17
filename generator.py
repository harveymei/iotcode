#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020/12/17 11:04 上午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: generator.py
# @IDE     : PyCharm
# @GitHub  ：https://github.com/harveymei/

from stdnum.iso7064 import mod_37_36
import base62
import time

print("编码规则版本：V4")
print("国家代码编号提示：（中国：2405 日本：2841 美国：3526）\n")

country_serial_number = int(input("请输入国家编号："))
administration_serial_number = int(input("请输入管理机构编号："))
company_serial_number = int(input("请输入应用企业编号："))
iot_code_start_serial_number = int(input("\n请输入待生成编码起始编号："))
iot_code_total_number = int(input("请输入待生成编码总数量："))


"""
生成C段代码
"""
segment_c_prefix_code = '0'
country_code = base62.encode(country_serial_number, charset=base62.CHARSET_INVERTED)
administration_code = base62.encode(administration_serial_number, charset=base62.CHARSET_INVERTED)
company_code = base62.encode(company_serial_number, charset=base62.CHARSET_INVERTED)

country_code_length = 2
administration_code_length = 2
company_code_length = 7
full_country_code = country_code.rjust(country_code_length, '0')
full_administration_code = administration_code.rjust(administration_code_length, '0')  # 右对齐补齐
full_company_code = company_code.rjust(company_code_length, '0')
full_c = segment_c_prefix_code + full_country_code + full_administration_code + full_company_code


"""
生成G段代码
"""
segment_g_prefix_code = '0'
user_defined_code_length = 11
user_defined_code = ''
full_user_defined_code = user_defined_code.rjust(user_defined_code_length, '0')  # 右对齐补齐
full_g = segment_g_prefix_code + full_user_defined_code


"""
生成U段代码
"""
# 生成唯一标识代码编号
serial_numbers = []
iot_code_total_number = iot_code_start_serial_number + iot_code_total_number
for i in range(iot_code_start_serial_number, iot_code_total_number):
    serial_numbers.append(i)

# 生成唯一标识代码并补齐
full_serial_numbers = []
for j in serial_numbers:
    serial_code = base62.encode(j, charset=base62.CHARSET_INVERTED)
    full_serial_number_length = 11
    full_serial_numbers.append(serial_code.rjust(full_serial_number_length, '0'))  # 右对齐补齐

# 计算校验码
alphabet = base62.CHARSET_INVERTED

check_digits = []
for k in full_serial_numbers:
    full_serial_number = mod_37_36.calc_check_digit(k, alphabet)
    check_digits.append(full_serial_number)


"""
拼接编码写入文件
"""
filename = str(int(time.time())) + ".txt"
with open(filename, 'w') as f_obj:
    for full_serial_numbers, check_digits in zip(full_serial_numbers, check_digits):
        full_codes = full_c + full_g + full_serial_numbers + check_digits + "\n"
        f_obj.write(full_codes)

print("----------------\n" + "编码生成完成！")
