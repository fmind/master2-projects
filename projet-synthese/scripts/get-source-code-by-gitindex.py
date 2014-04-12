#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Freaxmind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Récupère le code source du groupe 2 """

__author__  = 'Freaxmind'
__email__   = 'freaxmind@freaxmind.pro'
__version__ = '0.1'
__license__ = 'GPLv3'

import urllib
import re
import os

content = open('index').read()

for f in re.findall("[A-Za-z0-9.\/]+", content):
    if len(f) > 4:
        url = "http://172.24.141.119/" + f
        fres = "src/" + f.replace('/', '__')

        try:
            urllib.urlretrieve(url, fres)
            print url
        except IOError as e:
            print e
