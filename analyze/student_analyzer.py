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
import re
import MeCab
import traceback
import os.path
import collections
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
        # Noise includes Katakana and specific Knaji called "Wara" in Japanese
        self.NOISE_RE = re.compile(r'^(?:\xE3\x82[\xA1-\xBF]|\xE3\x83[\x80-\xB6]|\xE3\x83[\xBB-\xBE]|\xE7\xAC\x91)+$')
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

    def __end_one_student(self):
        firstnames, lastnames, page_keywords = self.__rank_some_features()

        # Noise filter in Japanese
        firstnames = [fn for fn in firstnames if not self.NOISE_RE.search(fn)]
        lastnames = [ln for ln in lastnames if not self.NOISE_RE.search(ln)]

        #High frequency words priority is higher(Only five firstnames and lastnames)
        common_firstnames = collections.Counter(firstnames).most_common(10)
        common_lastnames = collections.Counter(lastnames).most_common(10)
        common_keywords = collections.Counter(page_keywords).most_common(250)
        firstnames = [cf[0] for cf in common_firstnames]
        lastnames = [cl[0] for cl in common_lastnames]
        page_keywords = [ck[0] for ck in common_keywords if len(ck[0].decode('utf-8')) >= 2]

        """
        for x in firstnames: print x,
        print 
        for x in lastnames: print x,
        print 
        for x in page_keywords: print x,
        print 
        """

        self.db_manager.register_HTML(self.back_studentID, firstnames, lastnames, page_keywords, self.page_titles, self.page_paths, self.page_size)
        self.clear_features()


    def analyze_HTML(self, path, studentID):
        if len(self.back_studentID) > 0 and self.back_studentID != studentID:
            self.__end_one_student()
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
            self.__end_one_student()

    def __rank_some_features(self):
        self.content = Constants.URL_RE.sub('', self.content)
        node = self.tagger.parseToNode(self.content)
        firstnames, lastnames = [], []
        page_keywords = []
        while node:
            features = node.feature.split(",")
            if features[0] == "名詞":
                if "人名" in features:
                    if "名" in features:
                        firstnames.append(node.surface)
                    elif "姓" in features:
                        lastnames.append(node.surface)
                elif "数" in features or "サ変接続" in features:
                    pass
                else:
                    page_keywords.append(node.surface)
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
