# -*- coding: utf-8 -*-

import random

a = [1,2]
q = 0
w = 0
for i in range(100):
    b = random.choice(a)
    if b == 1:
        q += 1
    else:
        w += 1

print(q, w)