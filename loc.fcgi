#!/bin/sh

USER_HOME=/home/gbenison;
export PATH=${PATH}:${USER_HOME}/software/bin:${USER_HOME}/usr/bin
export PYTHONPATH=${PYTHONPATH}:${USER_HOME}/usr/lib/python2.6/site-packages
export TEXINPUTS=${USER_HOME}/texmf///:${USER_HOME}/texmf/tex/latex///:${DOCUMENT_ROOT}/media//:

python /home/gbenison/gwenomatic/alpha/current/loc.py
