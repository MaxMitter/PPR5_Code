# -*- coding: utf-8 -*-

import calendar
import string

divBy7 = [x for x in range(1001) if x % 7 == 0]
print(divBy7)

print("=============================")
contains3 = [x for x in range(1001) if '3' in str(x)]
print(contains3)

print("=============================")
doors = [x + 1 for x in range(101) if (x + 1) ** 0.5 % 1 == 0]
print(doors)

print("=============================")
months = [calendar.month_name[x + 1] for x in range(12)]
months2 = [x for x in calendar.month_names[1:]]
print(months)

print("=============================")
monthNoR = [calendar.month_name[x + 1] for x in range(12) if 'r' not in calendar.month_name[x + 1]]
print(monthNoR)

print("=============================")
cartProd = {'(' + a + ', ' + str(b) + ')' for a in {'x','y'} for b in {1, 3}}
print(cartProd)

print("=============================")
letterOrdDict = {ord(x) : x for x in string.ascii_lowercase[:26]}
print(str(letterOrdDict) + "len: " + str(len(letterOrdDict)))