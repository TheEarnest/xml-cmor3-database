#!/bin/bash
pushd /software/svn/trunk/dreqPy/docs/
svn update
popd
cp ../docs/dreq.xml ../docs/dreq.xml.old
cp ../docs/vocab.xml ../docs/vocab.xml.old
cp /software/svn/trunk/dreqPy/docs/dreq.xml ../docs
cp /software/svn/trunk/dreqPy/docs/vocab.xml ../docs
cp /software/svn/trunk/dreqPy/packageConfig.py .

