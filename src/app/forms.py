#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

 | Title:
     forms.py
 | Date:
     2020-03-09
 | Author(s):
     THEODOR Rumetshofer

"""

#__________________
# import functions \__________________________________________________________

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


#_____________________
# define form classes \_______________________________________________________

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
  
class IndexForm(FlaskForm):
    pn = BooleanField('include personnummer OBS! GDPR')
    outliers = BooleanField('include outliers')
    age = StringField("Specify subject age (eg, '<40', '>50' or range '30-40')")
    qol = StringField("Quality of life score (eg, '<.5', '>.9' or range '.7-.9')")
    submit1 = SubmitField('query') 
    submit2 = SubmitField('download')        
    submit3 = SubmitField('show pca')   
    submit4 = SubmitField('show clustering')  
