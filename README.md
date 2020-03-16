# project database
This project was part of the BINP29 course at Lund University in 2020.

## Description
This code is used to allow collaborators in the SLE project to access, filter, analyze and output data from the project dataset in a web framework using flask. The original database is a csv-file which is stored in the "data" folder.  

## Installation
It is recommended to create a new conda environment for flask and to activate:
```bash
conda create -n flaskenv flask
conda activate flaskenv
```

Control the version and the environments:
```bash
flask --version
conda info --envs
```

After cloning this repository, the following packages have to be installed:
* numpy
* flask-wtf
* pandas
* matplotlib
* seaborn

## Usage
change in the "src" folder in the repository.
```bash
FLASK_APP=flask_sle.py 
flask run
```

## Authors and acknowledgment
Theodor Rumetshofer
theodor.rumetshofer@gmail.com

## Project status
- [x] user login
- [x] filtering and apply queries
- [x] output as csv-file
- [x] PCA analysis
- [x] Cluster analysis
- [ ] user database
- [ ] relational database
- [ ] real productive environment

