#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

 | Title:
     config.py
 | Date:
     2020-03-09
 | Author(s):
     THEODOR Rumetshofer

"""

#__________________
# import functions \__________________________________________________________

import os


#______________________________
# define config for the log-in \______________________________________________

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
