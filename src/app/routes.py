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
import numpy as np
from flask import render_template, flash, redirect, url_for, make_response
from app import app
from app.forms import LoginForm, IndexForm
import pandas as pd
import os
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import seaborn as sns

#__________________
# define functions \__________________________________________________________

# start 
@app.route('/')
def start():
    return render_template('start.html')


# log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if the submit button is pressend without any data (GET) it will jump to the 
    # last return line and shows the login.html again
    # if data is submitted, the data will be sended (POST) and the if is true. 
    # BUT if just one "data required" is missing, it will start from the beginning
    if form.validate_on_submit():
        # flash=show message to the user but the message will not automatically appear
        flash('Hej {}, welcome back!'.format(form.username.data))
        return redirect(url_for('index')) # redirected to index page
    # show log in again
    return render_template('login.html', form=form)

    
# index
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm()

    if form.validate_on_submit():
        
        if form.submit1.data:
            number_subj, new_df = query_csv(form)
            flash('Number of subjects due to your selection: {}'.format(number_subj), 'error') ### IN RED COLOUR!!!
            return render_template('index.html', form=form, result_pca=None, result_hcl=None)
        
        if form.submit2.data:
            number_subj, new_df = query_csv(form)
            resp = make_response(new_df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            resp.headers["Content-Type"] = "text/csv"
            return resp  
        
        if form.submit3.data:
            number_subj, new_df = query_csv(form)
            fig_pca = pca_cnsvs_ss(new_df)
            from io import BytesIO
            import base64
            figpcafile = BytesIO()
            fig_pca.savefig(figpcafile, format='png')
            figpcafile.seek(0)  # rewind to beginning of file
            figdata_png_pca = base64.b64encode(figpcafile.getvalue())
            return render_template('index.html', form=form, result_pca=figdata_png_pca.decode('utf8'), result_hcl=None)

        if form.submit4.data:
            number_subj, new_df = query_csv(form)
            fig_hcl = clustering_cnsvs_ss(new_df)
            from io import BytesIO
            import base64
            fighclfile = BytesIO()
            fig_hcl.savefig(fighclfile, format='png')
            fighclfile.seek(0)  # rewind to beginning of file
            figdata_png_hcl = base64.b64encode(fighclfile.getvalue())
            return render_template('index.html', form=form, result_pca=None, result_hcl=figdata_png_hcl.decode('utf8'))        
    
    
    return render_template('index.html', form=form, result=None)
   
    


# do the queries on the csv file
def query_csv(form):
    
    # set path
    curr_path = os.getcwd()
    path = os.path.join(curr_path, "../data/")
    
    # load csv-file
    df = pd.read_csv(path+'data.csv', index_col=0)
    
#    print(df)
    
    ## do queries
    # if TRUE => use the ids (GDPR!)
    use_pn = form.pn.data
    if use_pn == False:
        d = df.drop(columns='id')
    else: d = df.copy()
    
    
    # if TRUE => use also outliers
    incl_out = form.outliers.data 
    if incl_out == False:
        d = d.query('outlier==False')
    else: d = d.copy()    
    
    
    # AGE threshold
    age_string = form.age.data
    if age_string:
        
        # bigger
        if age_string.startswith('>'):
            age = age_string.split('>')[1]
            if age.isdigit(): # check if string contains only digits
                age = int(age)
                d = d.query('pat_age>@age')
            
        #  smaller
        elif age_string.startswith('<'):
            age = age_string.split('<')[1]
            if age.isdigit(): # check if string contains only digits
                age = int(age)
                d = d.query('pat_age<@age') 
                
        #  range
        elif '-' in age_string:
            lower = age_string.split('-')[0]
            upper = age_string.split('-')[1]
            if lower.isdigit() and upper.isdigit():
                lower = int(lower)
                upper = int(upper)
                d = d.query('@upper > pat_age > @lower')   

    else:
        d = d.copy()    

    # Qulaity of life threshold
    qol_string = form.qol.data
    if qol_string:
        
        # bigger
        if qol_string.startswith('>'):
            qol = qol_string.split('>')[1]
            try:
                qol = float(qol) # check if string is a float
                d = d.query('QoL_eq5d>@qol') 
            except:
                pass
            
            
        #  smaller
        elif qol_string.startswith('<'):
            qol = qol_string.split('<')[1]
            try:
                qol = float(qol) # check if string is a float
                d = d.query('QoL_eq5d<@qol') 
            except:
                pass
            
                
        #  range
        elif '-' in qol_string:
            lower = qol_string.split('-')[0]
            upper = qol_string.split('-')[1]
            try: 
                lower = float(lower) # check if string is a float
                upper = float(upper)
                d = d.query('@upper > QoL_eq5d > @lower')    
            except:
                pass
                

    else:
        d = d.copy() 

    
    # ....
    
    new_df = d.copy()
    new_df.index = list(range(1,new_df.shape[0]+1))
    number_subj = new_df.shape[0]

    return number_subj, new_df


# do PCA on the CNVS-standard scores
def pca_cnsvs_ss(new_df):
    
    X = new_df.filter(regex='_ss')
    pca_ncomponents = 2
    pca = PCA(n_components=pca_ncomponents,svd_solver='auto', whiten=True, random_state=0).fit(X)
    X_pca = pca.transform(X)
    
    lbl = new_df['label'].values
    lbl_uniq = np.unique(lbl)
    colors = ['g','r','b']
    pca_plot = []

    fig = plt.figure()     
    for label, color in zip(lbl_uniq,colors):
        pca_plot.append(plt.scatter(X_pca[lbl==label,0],X_pca[lbl==label,1],c=color, alpha=0.4, label=label))
    plt.legend(handles=pca_plot, frameon=True)
    
    plt.xlabel('1st principal component')
    plt.ylabel('2nd principal component')
    plt.title('PCA: variance ratio of the first 2 components: %.2f\nnumber of subjects %.0f' %(sum(pca.explained_variance_ratio_[:2]),lbl.size))

    return fig

# clustering on the CNSVS-standard scores
def clustering_cnsvs_ss(new_df):       
        
    X = new_df.filter(regex='_ss')
    X.to_csv('test.csv')
    
    # create the labels
    color_lbl = pd.DataFrame(columns=['HC','nonNPSLE', 'NPSLE', ], index=new_df.index, data='white')
    color_lbl['HC'][new_df[new_df.label=='HC'].index] = 'g'
    color_lbl['nonNPSLE'][new_df[new_df.label=='nonNPSLE'].index] = 'b'
    color_lbl['NPSLE'][new_df[new_df.label=='NPSLE'].index] = 'r'
    
    
    fig = sns.clustermap(X.T, row_cluster=None, method='ward', figsize=(7,5), cmap="mako",
                         col_colors=color_lbl,
                         xticklabels=0)
    
#    fig.cax.set_visible(False)

    for tick in fig.ax_col_colors.get_yticklabels():
        tick.set_fontsize(7)
    
    
    ax = fig.ax_heatmap
    ax.set_ylabel('CNS-VS score', fontsize=12)
    ax.set_xlabel('subjects', fontsize=12)

    return fig


















