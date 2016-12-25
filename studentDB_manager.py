#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from constants import Constants
import dlconfig
from datetime import date

class StudentDBManager(object):
    def __init__(self):
        self.esDB = sqlite3.connect(dlconfig.estimated_cse_student_DB)
        self.sDB = sqlite3.connect(dlconfig.cse_student_DB)
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

    def label_downloaded_students(self, begin_sID, end_sID, traced_date):
        cursor = self.esDB.cursor()
        for studentID in self.get_studentIDs_from(begin_sID, end_sID):
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
        oldest_entrance_year = dlconfig.entrance_year_of_oldestOB

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


    def get_not_traced_students(self):
        cursor = self.esDB.cursor()
        cursor.execute("SELECT entrance_year, studentID FROM cse_students WHERE ifnull(length(traced_date), 0) = 0")
        return [[Constants.get_grade(row_line[0]), row_line[1].encode('utf-8')] for row_line in cursor.fetchall()]

    def close(self):
        self.esDB.close()
        self.sDB.close()


def test():
    manager = StudentDBManager()
    manager.esDB = sqlite3.connect("DB/sample1.db")
    manager.sDB = sqlite3.connect("DB/sample2.db")
    manager.register_estimated_studentID("g0811111")
    manager.register_estimated_studentID("g1111116")
    print manager.get_unknown_grades()
    print manager.get_estimated_studentIDs()
    print manager.get_estimated_studentIDs_from(2011)
    #manager.register_estimated_studentIDs("www.cc.kyoto-su.ac.jp")
    manager.close()


def main():
    """Run an example for a StudentDBManager class."""
    test()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
