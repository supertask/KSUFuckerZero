#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from datetime import date
from constants import Constants
import dlconfig

"""
Links:
g0947064
http://www.cse.kyoto-su.ac.jp/~g0947343/webcom/

http://vaaaaaanquish.hatenablog.com/entry/2016/08/08/160353
http://qiita.com/howdy39/items/a1aef86fef1ce1b6d778
"""

class StudentIDDownloader(object):
    def __init__(self):
        self.students = self.get_students(
            student_type = dlconfig.get_student_type(),
            department = dlconfig.get_department(),
            grades = dlconfig.get_grades()
        )
        self.last_student_ID = self.trace_last_student("http://www.cc.kyoto-su.ac.jp")

    @classmethod
    def get_year(self, grade, date_today):
        """Estimates a year from grade using a date.

        Example:
            if today -> 2016
            1,2,3,4 -> 2016,2015,2014,2013
        """
        if date_today.month < 4:
            freshman_year = date_today.year - 1
        else:
            freshman_year = date_today.year
        return freshman_year - grade + 1 

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


    def trace_last_student(self, a_url):
        root_folder = a_url[len(Constants.PROTOCOL):]
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
        date_today = date.today()
        department = str(department)

        for a_grade in grades:
            a_year = str(self.get_year(a_grade, date_today))
            student_number_head = a_year[-1] + department
            student_ID_head = student_type + a_year[-2:] + department

            for index in range(0000, 10000): #0000~9999
                student_number = student_number_head + str(index).zfill(4)
                student_ID = student_ID_head + str(index).zfill(4)
                combined_number = sum([int(c) for c in student_number])
                if combined_number % 10 == 0:
                    students.append([a_grade, student_ID])
        return students


    def download_from_urls(self, urls, student_ID):
        for url in urls:
            url = url % student_ID 
            #print grade, student_ID, url
            shell_line = ["wget", "-r", "--random-wait", "--exclude-directories=%s" % dlconfig.get_exclude_dirs(), url]
            #subprocess.call(shell_line)


    def download(self):
        for grade, student_ID in self.students:
            print student_ID,
            if self.last_student_ID:
                if self.compare_sID(self.last_student_ID, student_ID) == 0: print
                if self.compare_sID(self.last_student_ID, student_ID) > 0:
                    continue
            self.download_from_urls(dlconfig.get_urls(grade), student_ID)
        print
        print "Finished"


def main():
    """Run an example for a studentIDGetter class."""

    sID_getter = StudentIDDownloader()
    sID_getter.download()
    #print "Number of student: ", len(students)
    #print self.last_student_ID

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
