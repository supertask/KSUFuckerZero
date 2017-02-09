#! /usr/bin/python
# -*- coding: utf-8 -*-
u"""dlibによる顔画像検出."""
import cv2
import dlib

# 画像ファイルパスを指定
import sys
sample_img_path = sys.argv[1]

def facedetector_dlib(img, image_path):
    try:
        detector = dlib.get_frontal_face_detector()
        # RGB変換 (opencv形式からskimage形式に変換)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        dets, scores, idx = detector.run(img_rgb, 0)

        # 矩形の色
        color = (0, 0, 255)
        s = ''
        if len(dets) > 0:
            # 顔画像ありと判断された場合
            for i, rect in enumerate(dets):
                # detsが矩形, scoreはスコア、idxはサブ検出器の結果(0.0がメインで数が大きい程弱い)
                # print rect, scores[i], idx[i]
                cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), color, thickness=1)
                print rect
                #s += (str(rect.left()) + ' ' + str(rect.top()) + ' ' + str(rect.right()) + ' ' + str(rect.bottom()) + ' ')
            s += image_path
        return img, s
    except:
        # メモリエラーの時など
        return img, ""

if __name__ == '__main__':
    img = cv2.imread(sample_img_path)
    img, s = facedetector_dlib(img, sample_img_path)
    cv2.imwrite('output.jpg', img)
    print s
