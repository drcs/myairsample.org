#!/bin/sh

HOME=/home/gbenison

export TEXINPUTS=${HOME}/texmf///:${HOME}/texmf/tex/latex///:${DOCUMENT_ROOT}/media//:
export PYTHONPATH=${HOME}/usr/lib/python2.6/site-packages

script="${DOCUMENT_ROOT}${SCRIPT_URL}";
cd `dirname $script`;
exec ./`basename $script`;
