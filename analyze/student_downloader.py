#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import os.path
import subprocess
import filecmp
import shutil
import datetime
from datetime import date
from constants import Constants
import dlconfig
from studentDB_manager import EstimatedStudentDBManager


class StudentDownloader(object):
    def __init__(self):
        #self.last_student_ID = self.trace_last_student("www.cc.kyoto-su.ac.jp")
        self.db_manager = EstimatedStudentDBManager(Constants.ESTIMATED_CSE_STUDENT_DB)

    def get_db_manager(self):
        return self.db_manager

    def compare_sID(self, sID_L, sID_R):
        """
        Args:
            sID_L: a string indicated a student id, 'g\d{7}'
            sID_R: a string indicated a student id, 'g\d{7}'
        Returns:
            a number indicated whether which one should be traced priority.
        Example:
            input: sID_L -> g0000002, sID_R -> g0100000, output: 1
            input: sID_L -> g0100002, sID_R -> g0000000, output: -1
            input: sID_L -> g0000002, sID_R -> g0000000, output: 1
        """
        sID_L, sID_R = sID_L[1:], sID_R[1:]
        L_BLOCK_LEN = 2
        sID_L_2, sID_R_2 = int(sID_L[:L_BLOCK_LEN]), int(sID_R[:L_BLOCK_LEN])
        sID_L_4, sID_R_4 = int(sID_L[L_BLOCK_LEN:]), int(sID_R[L_BLOCK_LEN:])
        if sID_L_2 == sID_R_2: #16, 14
            if sID_L_4 == sID_R_4: return 0
            elif sID_L_4 > sID_R_4: return 1
            else: return -1
        elif sID_L_2 < sID_R_2: return 1
        else: return -1

    def trace_last_student(self, root_folder):
        try: folder_names = os.listdir(root_folder)
        except: return None
        student_IDs = []
        for folder_name in folder_names:
            matcher = Constants.STUDENT_ID_RE.search(folder_name)
            if matcher:
                student_IDs.append(matcher.group())
        student_IDs.sort(cmp=self.compare_sID)
        return student_IDs[-1]

    def get_students(self, student_type, department, grades=[1,2,3,4]):
        students = []
        department = str(department)

        for a_grade in grades:
            a_year = str(Constants.get_year(a_grade))
            student_number_head = a_year[-1] + department
            student_ID_head = student_type + a_year[-2:] + department

            for index in range(0000, 10000): #0000~9999
                student_number = student_number_head + str(index).zfill(4)
                student_ID = student_ID_head + str(index).zfill(4)
                combined_number = sum([int(c) for c in student_number])
                if combined_number % 10 == 0:
                    students.append([a_grade, student_ID])
        return students

    def clean_garbage_pages(self, root_dir, index_page):
        for folder_name in os.listdir(root_dir):
            student_path = os.path.join(root_dir, folder_name)
            if not os.path.isdir(student_path):
                continue
            page_1 = os.path.join(student_path, "index.html")
            page_2 = os.path.join(student_path, "index-j.html")
            if os.path.isfile(page_1) and os.path.isfile(page_2):
                is_delete = filecmp.cmp(page_1, index_page) and filecmp.cmp(page_2, index_page)
                print filecmp.cmp(page_1, index_page), filecmp.cmp(page_2, index_page)
                if is_delete:
                    shutil.rmtree(student_path)

    def download_from_urls(self, urls, student_ID, options=[]):
        for url in urls:
            url = url % student_ID 
            print student_ID, url
            shell_line = ["wget", "-r", "--random-wait", "--exclude-directories=%s" % dlconfig.get_exclude_dirs(), url] + options
            subprocess.call(shell_line)

    #Phase 1
    def determine_studentID(self):
        """Downloads index pages from "cc.kyoto-su.ac.jp" for ensuring whether a student id is currect.
        """
        unknown_grades = self.db_manager.get_unknown_grades()
        students = self.get_students(
            student_type = Constants.STUDENT_TYPE,
            department = Constants.DEPARTMENT,
            grades = unknown_grades
        )

        start = time.time()
        MIN_10, MIN_20 = 60 * 10, 60 * 20
        for grade, studentID in students:
            if  time.time() - start > MIN_20:
                print "wait.............." 
                time.sleep(MIN_10) #10min
                start = time.time()
            #self.download_from_urls(Constants.URLS_FOR_DETERMINING_STUDENT_ID, studentID, options=["--timeout", "300"])

        #self.db_manager.register_estimated_studentIDs(Constants.CC_DOMAIN) #Important!
        self.clean_garbage_pages(Constants.CC_DOMAIN, Constants.KSU_TEMPLATE_INDEX)

    #Phase2
    def download_all(self):
        students = self.db_manager.get_not_traced_students_yet()
        studentIDs = []
        start = time.time()
        MIN_10, MIN_20 = 60 * 10, 60 * 20

        for grade, studentID in students:
            if  time.time() - start > MIN_20:
                print "wait.............." 
                time.sleep(MIN_10) #10min
                start = time.time()
            self.download_from_urls(dlconfig.get_urls(grade), studentID)
            studentIDs.append(studentID)
        self.db_manager.label_traced_students(studentIDs, Constants.TODAY)
        print "Finished"

