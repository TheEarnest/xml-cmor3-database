#!/bin/bash
pushd ~/software/cmor3/trunk/dreqPy/docs/
svn update
popd
cp ../docs/dreq.xml ../docs/dreq.xml.old
cp ../docs/vocab.xml ../docs/vocab.xml.old
cp ~/software/cmor3/trunk/dreqPy/docs/dreq.xml ../docs
cp ~/software/cmor3/trunk/dreqPy/docs/vocab.xml ../docs
cp ~/software/cmor3/trunk/dreqPy/packageConfig.py .

