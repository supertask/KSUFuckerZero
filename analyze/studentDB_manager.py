#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from constants import Constants
import dlconfig
from datetime import date
from tool import Tool

class EstimatedStudentDBManager(object):
    def __init__(self, DB_name):
        self.esDB = sqlite3.connect(DB_name)
        cursor = self.esDB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS cse_students(entrance_year integer, studentID text, traced_date date)')

    def register_estimated_studentID(self, studentID):
        entrance_year = int('20' + studentID[1:3])
        cursor = self.esDB.cursor()
        cursor.execute('SELECT studentID FROM cse_students WHERE studentID = "%s"' % studentID)
        if not cursor.fetchall():
            cursor.execute('INSERT INTO cse_students VALUES(?, ?, ?)', (entrance_year, studentID, None))
        self.esDB.commit()

    def register_estimated_studentIDs(self, root_dir):
        for folder_name in os.listdir(root_dir):
            matcher = Constants.STUDENT_ID_RE.search(folder_name)
            if matcher:
                self.register_estimated_studentID(matcher.group())

    def register_studentIDs_ranging(self, begin_sID, end_sID):
        for studentID in self.get_studentIDs_from(begin_sID, end_sID):
            self.register_estimated_studentID(studentID)

    def label_traced_students_ranging(self, begin_sID, end_sID, traced_date):
        cursor = self.esDB.cursor()
        studentIDs = self.get_studentIDs_from(begin_sID, end_sID)
        self.label_traced_students(studentIDs, traced_date)

    def label_traced_students(self, studentIDs, traced_date):
        cursor = self.esDB.cursor()
        for studentID in studentIDs:
            cursor.execute('UPDATE cse_students SET traced_date = ? WHERE studentID = ?', (traced_date, studentID))
        self.esDB.commit()
        

    def get_studentIDs_from(self, begin_sID, end_sID):
        studentIDs = []
        for studentID_tail in range(int(begin_sID[1:]), int(end_sID[1:])):
            studentID = "g" + str(studentID_tail).zfill(7)
            combined_number = sum([int(c) for c in studentID[2:]])
            if combined_number % 10 == 0:
                studentIDs.append(studentID)
        return studentIDs


    def get_unknown_grades(self):
        freshman_entrance_year = Constants.get_year(1) #1=freshman
        oldest_entrance_year = Constants.ENTRANCE_YEAR_OF_OLDEST_OB

        unknown_grades = []
        cursor = self.esDB.cursor()
        for entrance_year in range(oldest_entrance_year, freshman_entrance_year+1):
            cursor.execute('SELECT entrance_year FROM cse_students WHERE entrance_year = "%s"' % entrance_year)
            if not cursor.fetchall():
                unknown_grades.append(Constants.get_grade(entrance_year))
        return unknown_grades

    def get_estimated_studentIDs(self):
        cursor = self.esDB.cursor()
        cursor.execute('SELECT studentID FROM cse_students')
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]
        
    def get_estimated_studentIDs_from(self, entrance_year):
        cursor = self.esDB.cursor()
        cursor.execute('SELECT studentID FROM cse_students WHERE entrance_year = "%s"' % entrance_year)
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]


    def get_not_traced_students_yet(self):
        cursor = self.esDB.cursor()
        cursor.execute("SELECT entrance_year, studentID FROM cse_students WHERE ifnull(length(traced_date), 0) = 0")
        return [[Constants.get_grade(row_line[0]), row_line[1].encode('utf-8')] for row_line in cursor.fetchall()]

    def close(self):
        self.esDB.close()


class StudentDBManager(object):
    def __init__(self, DB_name):
        self.sDB = sqlite3.connect(DB_name)
        self.sDB.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        cursor = self.sDB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS cse_students(entrance_year integer, studentID text, firstnames text, lastnames text, page_keywords text, page_titles text, page_paths text, image_links text, faceimage_position text, coding_size integer)')


    def convert_to_string(self, attributes):
        """Convert a list of a list to a list of string.
        """
        return map(lambda x: Tool.conv_encoding(Constants.SPLIT_CHAR.join(x)), attributes)


    def register(self, studentID, firstnames, lastnames, page_keywords, page_titles, page_paths, coding_size):
        entrance_year = int('20' + studentID[1:3])
        cursor = self.sDB.cursor()
        cursor.execute('SELECT studentID FROM cse_students WHERE studentID = "%s"' % studentID)
        some_attributes = [firstnames, lastnames, page_keywords]

        if cursor.fetchall():
            cursor.execute('SELECT firstnames,lastnames,page_keywords,page_titles,page_paths,coding_size FROM cse_students WHERE studentID = "%s"' % studentID)
            updating_attributes = list(cursor.fetchall()[0])

            for i in range(len(some_attributes)):
                if updating_attributes[i]:
                    some_attributes[i] = set(map(Tool.conv_encoding, some_attributes[i]))
                    attr = set(updating_attributes[i].split(Constants.SPLIT_CHAR)) | some_attributes[i]
                    updating_attributes[i] = Constants.SPLIT_CHAR.join(attr)
                else:
                    some_attributes = self.convert_to_string(some_attributes)
                    updating_attributes[i] = some_attributes[i]

            updating_attributes[len(some_attributes):] = self.convert_to_string([page_titles, page_paths]) + [coding_size]
            cursor.execute('UPDATE cse_students SET firstnames=?,lastnames=?,page_keywords=?,page_titles=?,page_paths=?,coding_size=? WHERE studentID = ?', updating_attributes + [studentID])
        else:
            some_attributes += [page_titles, page_paths]
            some_attributes = self.convert_to_string(some_attributes)
            all_attributes = [entrance_year, studentID] + some_attributes + [None, None, coding_size]
            cursor.execute('INSERT INTO cse_students VALUES(?,?,?,?,?, ?,?,?,?,?)', all_attributes)
        self.sDB.commit()


    def register_images(self, studentID, paths, face_rects):
        cursor = self.sDB.cursor()
        updating_attributes = []
        """
        updating_attributes.append(Constants.SPLIT_CHAR.join(paths))
        face_rects = map(str,face_rects)
        updating_attributes.append(Constants.SPLIT_CHAR.join(face_rects))
        print updating_attributes
        """

        cursor.fetchall()[0]
        cursor.execute('SELECT image_links,faceimage_position FROM cse_students WHERE studentID = "%s"' % studentID)
        cursor.fetchall()
        if no_images:
            cursor.execute('UPDATE cse_students SET image_links=?,faceimage_position=? WHERE studentID = ?', updating_attributes + [studentID])
        else:
            rects = faceimage_position.split(Constants.SPLIT_CHAR)
            for rect in rects:
                rect = eval(rect)
                if rect: face_rects.append(rect)


            cursor.execute('UPDATE cse_students SET image_links=?,faceimage_position=? WHERE studentID = ?', updating_attributes + [studentID])
        self.sDB.commit()


class KeywordsDBManager(object):
    def __init__(self, DB_name):
        self.sDB = sqlite3.connect(DB_name)
        self.sDB.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        cursor = self.sDB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS cse_students(keyword text, studentIDs text')

    # Here
    def register(self, studentID, keywords):
        for keyword in keywords:
            cursor = self.sDB.cursor()
            cursor.execute('SELECT studentIDs FROM student_keywords WHERE keyword = "%s"' % keyword)

            if cursor.fetchone():
                studentIDs = cursor.fetchone().split(Constants.SPLIT_CHAR)
                #cursor.execute('UPDATE cse_students SET firstnames=?,lastnames=?,page_keywords=?,page_titles=?,page_paths=?,coding_size=? WHERE studentID = ?', updating_attributes + [studentID])
            else:
                studentIDs = []
                #cursor.execute('INSERT INTO cse_students VALUES(?,?,?,?,?, ?,?,?,?,?)', all_attributes)
            studentIDs.append(studentID)
            studentIDs_line = Constants.SPLIT_CHAR.join(studentIDs)


def test():
    manager = EstimatedStudentDBManager("DB/sample1.db")
    manager.register_estimated_studentID("g0811111")
    manager.register_estimated_studentID("g1111116")
    print manager.get_unknown_grades()
    print manager.get_estimated_studentIDs()
    print manager.get_estimated_studentIDs_from(2011)
    #manager.register_estimated_studentIDs("www.cc.kyoto-su.ac.jp")
    manager.close()


def main():
    """Run an example for a EstimatedStudentDBManager and StudentDBManager class."""
    test()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
