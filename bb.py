#! /usr/bin/python
# -*- coding: utf-8 -*-
u"""dlibによる顔画像検出."""
import cv2
import dlib

# 画像ファイルパスを指定
import sys
sample_img_path = sys.argv[1]

def facedetector_dlib(image_path):
    img = cv2.imread(sample_img_path)
    try:
        detector = dlib.get_frontal_face_detector()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #RGB変換 (opencv形式からskimage形式に変換)
        dets, scores, idx = detector.run(img_rgb, 0) #frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        if len(dets) > 0:
            rects = []
            for rect in dets:
                rect = [rect.left(), rect.top(), rect.right()-rect.left(), rect.bottom()-rect.top()]
                rects.append(rect)
            return rects
        else:
            return None

    except:
        # メモリエラーの時など
        sys.exit(1)

if __name__ == '__main__':
    rect = facedetector_dlib(sample_img_path)
    print rect
