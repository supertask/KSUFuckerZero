#!/bin/bash
EXEC_DIR=/home/analyze
sudo docker run -v $(pwd):$EXEC_DIR -t sample python -c "import MeCab; print dir(MeCab); import dlib" #$EXEC_DIR/main.py
