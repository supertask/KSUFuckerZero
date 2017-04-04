# -*- coding: utf-8 -*-
import cv2
import sys

"""
    Faces
    /Users/tasuku/Sites/KSUHack/analyze/www.cse.kyoto-su.ac.jp/\~g0946812/webcom/neko.jpg
    /Users/tasuku/Sites/KSUHack/analyze/www.cse.kyoto-su.ac.jp/\~g1344504/g1344504.jpg
"""

def get_bigest_face(face_rects):
    max_face_size = 0
    max_rect = None
    for rect in face_rects:
        face_size = rect[2] * rect[3]
        if face_size > max_face_size:
            max_face_size = face_size
            max_rect = rect

    return max_rect

def get_face(image_path):

    #HAAR分類器の顔検出用の特徴量
    #cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml" #Correct
    #cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml" #Wrong face
    cascade_path = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml" #Correct
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
    face_rects = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
    #return list(get_bigest_face(face_rects))
    print face_rects

    
    """
    rect = max_rect
    cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color=(0, 255, 0), thickness=2)
    cv2.imwrite("images/detected_1.jpg", image)
    #cv2.imshow("Display window", image)
    #cv2.waitKey(0)
    """

    if len(face_rects) > 0:
        #検出した顔を囲む矩形の作成
        for rect in face_rects:
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color=(0, 255, 0), thickness=2)

            #認識結果の保存
            cv2.imwrite("images/detected_1.jpg", image)
            #cv2.imshow("Display window", image)
            #cv2.waitKey(0)

get_face(sys.argv[1])
"""
faces = []
faces.append(get_face(sys.argv[1]))
faces.append(get_face(sys.argv[2]))
print get_bigest_face(faces)
"""

