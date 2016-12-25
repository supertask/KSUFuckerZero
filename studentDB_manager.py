#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import filecmp
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
                self.register_studentID(matcher.group())

    def clean_garbage_pages(self, root_dir, index_page):
        import os.path
        for folder_name in os.listdir(root_dir):
            student_path = os.path.join(root_dir, folder_name)
            if not os.path.isdir(student_path):
                continue
            page_1 = os.path.join(student_path, "index.html")
            page_2 = os.path.join(student_path, "index-j.html")
            if os.path.isfile(page_1) and os.path.isfile(page_2):
                is_delete = filecmp.cmp(page_1, index_page) and filecmp.cmp(page_2, index_page)
                if is_delete:
                    shutil.rmtree(student_path)

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
    manager.clean_garbage_pages("www.cc.kyoto-su.ac.jp", Constants.KSU_TEMPLATE_INDEX)
    manager.close()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
