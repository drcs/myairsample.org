#!/bin/sh

HOME=/home/gbenison

export TEXINPUTS=${HOME}/texmf///:${HOME}/texmf/tex/latex///:${DOCUMENT_ROOT}/media//:
export PYTHONPATH=${HOME}/usr/lib/python2.6/site-packages

exec ${SCRIPT_FILENAME}
