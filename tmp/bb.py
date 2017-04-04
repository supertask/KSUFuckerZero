#! /usr/bin/python
# -*- coding: utf-8 -*-
u"""dlibによる顔画像検出."""
import cv2
import dlib

# 画像ファイルパスを指定
import sys
import os.path
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
import traceback
import numpy
import subprocess
sample_img_path = sys.argv[1]

def facedetector_dlib(image_path):
    img = io.imread(sample_img_path)
    detector = dlib.get_frontal_face_detector()
    try:
        dets, scores, idx = detector.run(img) #frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
    except:
        _, ext = os.path.splitext(image_path)
        if ext == ".gif": return None
        subprocess.call(["convert", image_path, image_path])
        img = io.imread(image_path)
        try:
            dets, scores, idx = detector.run(img) #frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        except:
            print "An error happened by dlib,", image_path
            traceback.print_exc()
            sys.exit(1)
        
    if len(dets) > 0:
        rects = []
        for rect in dets:
            rect = [rect.left(), rect.top(), rect.right()-rect.left(), rect.bottom()-rect.top()]
            rects.append(rect)
        return rects
    else:
        return None


if __name__ == '__main__':
    rect = facedetector_dlib(sample_img_path)
    print rect
