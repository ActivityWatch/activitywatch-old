#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew install python3
else
    # Install some custom requirements on other OSs
    true
fi;

