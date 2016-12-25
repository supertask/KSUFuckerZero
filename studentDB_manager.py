#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from constants import Constants
import dlconfig
from datetime import date
from studentID_downloader import StudentIDDownloader

class StudentDBManager(object):
    def __init__(self):
        self.esDB = sqlite3.connect(dlconfig.estimated_cse_student_DB)
        self.sDB = sqlite3.connect(dlconfig.cse_student_DB)
        self.esDB_cursor = self.esDB.cursor()

    def register_studentID(self, studentID):
        entrance_year = int('20' + studentID[1:3])
        DB_ID = int(studentID[1:])
        self.esDB_cursor.execute('CREATE TABLE IF NOT EXISTS cse_students(entrance_year integer, studentID text)')
        self.esDB_cursor.execute('SELECT studentID FROM cse_students WHERE studentID = "%s"' % studentID)
        if not self.esDB_cursor.fetchall():
            self.esDB_cursor.execute('INSERT INTO cse_students VALUES(%s, "%s")' % (entrance_year, studentID))
        self.esDB.commit()


    def register_studentIDs(self, root_dir):
        for folder_name in os.listdir(root_dir):
            matcher = Constants.STUDENT_ID_RE.search(folder_name)
            if matcher:
                #print matcher.group()
                self.register_studentID(matcher.group())


    def get_unknown_students(self):
        freshman_entrance_year = StudentIDDownloader.get_year(1, date.today()) #1=freshman
        oldest_entrance_year = dlconfig.entrance_year_of_oldestOB

        unknown_entrance_years = []
        for entrance_year in range(oldest_entrance_year, freshman_entrance_year+1):
            self.esDB_cursor.execute('SELECT entrance_year FROM cse_students WHERE entrance_year = "%s"' % entrance_year)
            if not self.esDB_cursor.fetchall():
                unknown_entrance_years.append(entrance_year)
        return unknown_entrance_years

    def get_estimated_studentIDs(self):
        self.esDB_cursor.execute('SELECT studentID FROM cse_students')
        return [studentID[0].encode('utf-8') for studentID in self.esDB_cursor.fetchall()]
        
    def get_estimated_studentIDs_from(self, entrance_year):
        self.esDB_cursor.execute('SELECT studentID FROM cse_students WHERE entrance_year = "%s"' % entrance_year)
        return [studentID[0].encode('utf-8') for studentID in self.esDB_cursor.fetchall()]


    def close(self):
        self.esDB.close()
        self.sDB.close()


def test():
    manager = StudentDBManager()
    manager.esDB = sqlite3.connect("DB/sample1.db")
    manager.sDB = sqlite3.connect("DB/sample2.db")
    manager.register_studentID("g1144704")
    manager.register_studentID("g0922222")
    manager.register_studentID("g0944444")
    manager.register_studentID("g0811111")
    manager.register_studentID("g1111116")
    print manager.get_unknown_students()
    print manager.get_estimated_studentIDs()
    print manager.get_estimated_studentIDs_from(2011)
    manager.register_studentIDs("www.cc.kyoto-su.ac.jp")
    manager.close()


def main():
    """Run an example for a StudentDBManager class."""
    manager = StudentDBManager()
    manager.register_studentIDs("www.cc.kyoto-su.ac.jp")
    manager.close()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
