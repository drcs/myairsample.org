#!/bin/sh

if [ -f sabotage ]; then
  sleep 10; exit 1;
fi

USER_HOME=/home/gbenison;

export PATH=${USER_HOME}/software/bin:${USER_HOME}/usr/bin:${PATH}
export PYTHONPATH=${PYTHONPATH}:${USER_HOME}/usr/lib/python2.6/site-packages
export TEXINPUTS=${USER_HOME}/texmf///:${USER_HOME}/texmf/tex/latex///:${DOCUMENT_ROOT}/media//:

if [ -f newrelic.ini ]; then
    source ${USER_HOME}/python/bin/activate
    export NEW_RELIC_CONFIG_FILE=newrelic.ini
    newrelic-admin run-program python loc.py
else
    python loc.py
fi

