# -*- coding: utf-8 -*-
import cv2
import sys

"""
    Faces
    /Users/tasuku/Project/KSUHack/analyze/www.cse.kyoto-su.ac.jp/\~g0946812/webcom/neko.jpg
    /Users/tasuku/Project/KSUHack/analyze/www.cse.kyoto-su.ac.jp/\~g1344504/g1344504.jpg
"""

def get_faces(image_path):

    #HAAR分類器の顔検出用の特徴量
    cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml" #Correct
    #cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml" #Wrong face
    #cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml" #Correct
    #cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml" #No face

    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #cv2.CASCADE_SCALE_IMAGE
    cascade = cv2.CascadeClassifier(cascade_path) #カスケード分類器の特徴量を取得する

    #物体認識（顔認識）の実行
    #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    #scaleFactor – 各画像スケールにおける縮小量を表します
    #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

    return facerect

    """
    if len(facerect) > 0:
        #検出した顔を囲む矩形の作成
        for rect in facerect:
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color=(0, 255, 0), thickness=2)
    else: return None

        #認識結果の保存
        cv2.imwrite("detected.jpg", image)
        cv2.imshow("Display window", image)
        cv2.waitKey(0)
    """

print get_faces(sys.argv[1])
