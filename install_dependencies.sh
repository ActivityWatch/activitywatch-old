#!/bin/bash
# TODO: Replace with requirements.txt or something

. ./virtualenv/bin/activate
pip3 install psutil --upgrade
pip3 install git+https://github.com/LiuLang/python3-xlib.git --upgrade
deactivate
