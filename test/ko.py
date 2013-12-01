# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:07:22 2013

@author: brenden
"""
# * coding:utf-8 *

import requests
import BeautifulSoup
p ={'return_tye':'paragraph','word':'학교 종이 땡땡땡 어서 모이자. 선생님이 우리를 기다리신다.'}
#p ={'return_tye':'paragraph','word':'국가'}
r =requests.post('http://owl-nest.com/lab/kts/',data=p)
s = BeautifulSoup.BeautifulSoup(r.text)
print [ n for n in s.pre.text.split('\n')]
