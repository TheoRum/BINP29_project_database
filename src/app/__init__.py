#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

 | Title:
     routes.py
 | Date:
     2020-03-09
 | Author(s):
     THEODOR Rumetshofer

"""

#__________________
# import functions \__________________________________________________________

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
