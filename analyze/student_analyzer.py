#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import MeCab
import dlib
import traceback
import os.path
from skimage import io
from constants import Constants
from tool import Tool
from studentDB_manager import StudentDBManager
from student_html_parser import StudentHTMLParser

import numpy
import subprocess

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
        paths,face_rects = self.get_faces(self.image_paths)
        self.db_manager.register_images(self.back_studentID, paths, face_rects)
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

    #Here
    def get_face(self, image_path):
        """ Here
        """
        img = io.imread(image_path)
        detector = dlib.get_frontal_face_detector()
        try:
            dets, scores, idx = detector.run(img) #frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        except:
            _, ext = os.path.splitext(image_path)
            #TODO(Tasuku): create a func for animated gif images
            if ext.upper() == ".GIF": return None
            subprocess.call(["convert", image_path, image_path])
            img = io.imread(image_path)
            try:
                dets, scores, idx = detector.run(img)
            except:
                print "An error happened by dlib,", image_path
                traceback.print_exc()
                sys.exit(Constants.EXIT_FAILURE)

        if len(dets) > 0:
            face_rects = []
            for rect in dets:
                rect = [rect.left(), rect.top(), rect.right()-rect.left(), rect.bottom()-rect.top()]
                face_rects.append(rect)
            biggest_face = self.get_biggest_face_of(face_rects)
            return biggest_face
        else:
            return None


    def get_faces(self, paths):
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
                pictures.append((path, None, ))

        faces = sorted(face_dict.items(), key=lambda x:x[1][2] * x[1][3], reverse=True)
        faces_n_pictures = faces + pictures
        paths = [f[0] for f in faces_n_pictures]
        rects = [f[1] for f in faces_n_pictures]
        return paths, rects


##############################################
# keywords from HTML
##############################################

    def create_index_DB(self):
        """Arrange the DB for a searching system.
        """
        self.db_manager.create_index_DB()


def test():
   sa = StudentAnalyzer(analyzing_folders=["www.cse.kyoto-su.ac.jp/","www.cc.kyoto-su.ac.jp/"])
   paths = ["../images/sample_1.jpg", "../images/sample_3.jpg", "../images/sample_2.jpg"]
   print sa.get_face_rects(paths)

if __name__ == '__main__':
    sys.exit(test())
