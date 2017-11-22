#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KSU Fucker
# -----------------
# Author:
#     Tasuku TAKAHASHI (supertask.jp)
# Coding style:
#     Google Python Style Guide
#     https://google.github.io/styleguide/pyguide.html
#

import sys
import os
import MeCab
import traceback
import os.path
from constants import Constants
from tool import Tool
from studentDB_manager import StudentDBManager
from student_html_parser import StudentHTMLParser

# This means someone who has a secret folder can use this package ;)
from db_auth import SQLAuth

import subprocess

class StudentAnalyzer(object):
    def __init__(self, table_name=Constants.STUDENT_TABLE_NAME):
        """To analyze HTMLs
        """
        self.analyzing_folders = Constants.ANALYZING_FOLDERS
        self.db_manager = StudentDBManager(SQLAuth().connection, table_name)
        self.tagger = MeCab.Tagger("-Ochasen")
        self.clear_features()

    def get_db_manger(self):
        return db_manager

    def clear_features(self):
        self.content = ""
        self.back_studentID = ""
        self.page_titles = []
        self.page_paths = []
        self.page_size = 0
        self.image_paths = []

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
    

    def analyze_HTMLs(self):
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
        #paths,face_rects = self.get_faces(self.image_paths)
        #self.db_manager.register_images(self.back_studentID, paths, face_rects)
        self.db_manager.register_images(self.back_studentID, self.image_paths)
        self.clear_features()


    def analyze_image(self, image_path, studentID):
        if len(self.back_studentID) > 0 and self.back_studentID != studentID:
            self.__save_image_features()
        self.image_paths.append(image_path)
        self.back_studentID = studentID

    def analyze_images(self):
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


##############################################
# keywords from HTML
##############################################

    def create_index_DB(self):
        """Arrange the DB for a searching system.
        """
        self.db_manager.create_index_DB()


def check():
    analyzer = StudentAnalyzer("cse_students_example")
    analyzer.analyze_HTMLs()
    #analyzer.create_index_DB()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(check())
