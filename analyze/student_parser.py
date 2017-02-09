#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import cv2
import MeCab
from HTMLParser import HTMLParser
from constants import Constants
from tool import Tool
from studentDB_manager import StudentDBManager

class StudentHTMLParser(HTMLParser):
    def __init__(self, page_path):
        HTMLParser.__init__(self)
        self.content = ""
        self.page_path = page_path.replace("‾","~")
        self.page_title = ""
        self.page_size = os.path.getsize(page_path)
        self.is_content_cnt = 0
        self.is_title = False
        self.is_spam = False
        self.htmltag_re = re.compile("html|h[1-6]|body|title|center|div|span|section|header|nav|article|section|footer|form|p|ul|ol|li|dl|dt|dd|pre|table|tr|th|td|a")
        self.spam_htmltag_re = re.compile("script|style")

    def increase_parameter(self, tag, param=[1,True,True]):
        if self.htmltag_re.match(tag):
            self.is_content_cnt+=param[0]
            if tag == "title":
                self.is_title = param[1]
        if self.spam_htmltag_re.match(tag):
            self.is_spam = param[2]
    
    def handle_starttag(self, tag, attrs):
        self.increase_parameter(tag)
    
    def handle_endtag(self, tag):
        self.increase_parameter(tag,[-1,False,False])
    
    def handle_data(self, content):
        if self.is_spam: return
        if self.is_content_cnt > 0:
            if self.is_title:
                self.page_title = content.replace('\n','').encode("utf-8")
            self.content += content + " "

    def show(self):
        print "-------------"
        print self.page_title
        print self.page_path
        print self.page_size
        print "-------------"


class StudentAnalyzer(object):
    def __init__(self):
        #
        # To analyze HTMLs
        #
        self.analyzing_folders = Constants.ANALYZING_FOLDERS
        self.db_manager = StudentDBManager(Constants.CSE_STUDENT_DB)
        self.tagger = MeCab.Tagger("-Ochasen")
        self.content = ""
        self.back_studentID = ""
        self.page_titles = []
        self.page_paths = []
        self.page_size = 0

        #
        # To analyze images
        #
        # HAAR分類器の顔検出用の特徴量
        self.cascade_paths = [
            "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml" #Correct
            #"/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml",  #Wrong face
            #"/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml", #Correct
            #"/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml" #No face
        ]
        self.image_paths = []

    def get_db_manger(self):
        return db_manager

    def clear_features(self):
        self.__init__()

    def __save_HTML_features(self):
        firstnames, lastnames, page_keywords = self.__rank_some_features()
        self.db_manager.register_HTML(self.back_studentID, firstnames, lastnames, page_keywords, self.page_titles, self.page_paths, self.page_size)
        self.clear_features()

    def analyze_HTML(self, path, studentID):
        if len(self.back_studentID) > 0 and self.back_studentID != studentID:
            self.__save_HTML_features()
        with open(path, 'r') as f:
            parser = StudentHTMLParser(path)
            content = f.read()
            parser.feed(Tool.conv_encoding(content))
            self.content += parser.content.encode("utf-8") + " "
            self.page_titles.append(parser.page_title)
            self.page_paths.append(parser.page_path)
            self.page_size += parser.page_size
            parser.close()

        self.back_studentID = studentID
    

    def analyze_n_save_HTMLs(self):
        for folder in self.analyzing_folders:
            Tool.search_HTMLs(os.path.join(folder), self.analyze_HTML)
            self.__save_HTML_features()

    def __rank_some_features(self):
        self.content = Constants.URL_RE.sub('', self.content)
        node = self.tagger.parseToNode(self.content)
        firstnames, lastnames, page_keywords = set(),set(),set()
        while node:
            features = node.feature.split(",")
            if features[0] == "名詞":
                if "人名" in features:
                    if "名" in features:
                        firstnames.add(node.surface)
                    elif "姓" in features:
                        lastnames.add(node.surface)
                elif "数" in features or "サ変接続" in features:
                    pass
                else:
                    page_keywords.add(node.surface)
            node = node.next
        return firstnames, lastnames, page_keywords


##############################################
# Images
##############################################

    def __save_image_features(self):
        face_rects = self.get_face_rects(self.image_paths)
        #print self.image_paths
        #print face_rects
        self.db_manager.register_images(self.back_studentID, self.image_paths, face_rects)
        self.clear_features()


    def analyze_image(self, image_path, studentID):
        if len(self.back_studentID) > 0 and self.back_studentID != studentID:
            self.__save_image_features()
        self.image_paths.append(image_path)
        self.back_studentID = studentID

    def analyze_n_save_images(self):
        for folder in self.analyzing_folders:
            #print folder, self.analyze_image
            Tool.search_images(os.path.join(folder), self.analyze_image)
            self.__save_image_features()


    def get_biggest_face_of(self, face_rects):
        max_face_size = 0
        max_rect = None
        for rect in face_rects:
            face_size = rect[2] * rect[3]
            if face_size > max_face_size:
                max_face_size = face_size
                max_rect = rect
        return max_rect

    def get_face(self, image_path):
        image = cv2.imread(image_path, 0)
        #image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #cv2.CASCADE_SCALE_IMAGE

        face_rects_on_all_cascades = []
        for cascade_path in self.cascade_paths:
            #物体認識（顔認識）の実行
            #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
            #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
            #scaleFactor – 各画像スケールにおける縮小量を表します
            #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
            #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
            #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
            face_rects = cv2.CascadeClassifier(cascade_path).detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(15, 15))

            # Too much features are suspicious. Return 'None' immediately.
            if len(face_rects) > 5: return None

            biggest_rect = self.get_biggest_face_of(face_rects)
            if biggest_rect is not None:
                face_rects_on_all_cascades.append(list(biggest_rect))

        biggest_face = self.get_biggest_face_of(face_rects_on_all_cascades)
        if biggest_face: return list(biggest_face)
        else: return None


    def get_face_rects(self, paths):
        face_dict = {}
        pictures = []
        for path in paths:
            face = self.get_face(path)
            if face:
                padding_px = int(((face[2] * face[3]) ** 0.5) * 0.1)
                face[0] -= padding_px
                face[1] -= padding_px
                face[2] += padding_px * 2
                face[3] += padding_px * 2
                face_dict[path] = face
            else:
                pictures.append((path, face, ))

        faces = sorted(face_dict.items(), key=lambda x:x[1][2] * x[1][3], reverse=True)
        faces_n_pictures = faces + pictures
        face_rects = [f[1] for f in faces_n_pictures]
        return face_rects


##############################################
# keywords from HTML
##############################################

    def create_index_DB(self):
        """Arrange the DB for a searching system.
        """
        keywords_db_manager = KeywordsDBManager(Constants.KEYWORDS_DB)
        #for
        #   keywords_db_manager.register(studentID, keywords)


def test():
   sa = StudentAnalyzer(analyzing_folders=["www.cse.kyoto-su.ac.jp/","www.cc.kyoto-su.ac.jp/"])
   paths = ["../images/sample_1.jpg", "../images/sample_3.jpg", "../images/sample_2.jpg"]
   print sa.get_face_rects(paths)

if __name__ == '__main__':
    sys.exit(test())
