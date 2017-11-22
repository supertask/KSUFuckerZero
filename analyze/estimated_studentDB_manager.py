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

import os
import sys
from constants import Constants
from tool import Tool

# This means someone who has a secret folder can use this package ;)
from db_auth import SQLAuth

class EstimatedStudentDBManager(object):
    """ A database manager for storing estimated students.

    This is used for estimating whther a student id exists in school.
    First, student id has some logical pattern like bellow.
        "student id = 558129" -> 5+5+8+1+2+9 = 30
        The 30 is able to divide by 10.
    Second, we try to get a html page(http://www.cc.kyoto-su.ac.jp/~<prefix><student id>/)
    using estimated id. if it fails, it means the student id DOES NOT EXIST.
    And then, this manager puts the student information into the database if it succeeds.
    That's it! Pretty easy right? ;)

    By the way I do not test entire functions bellow
    because html pages in my school(only cc domain) have access restriction.
    """

    def __init__(self, DB, table_name):
        """Inits the class and creates the table.
            Good(11/20/2017)
        Args:
            table_name - A string of a table name for a student database
        """
        self.DB = DB
        self.table_name = table_name
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(entrance_year SMALLINT, studentID VARCHAR(12), traced_date DATE)' % self.table_name)

    def register_estimated_studentID(self, studentID):
        """Registers estimated single student id into the database.
            Good(11/20/2017)
        Args:
            studentID - A string of student id in school. (ex. 'g0811111')
        """
        print studentID
        entrance_year = int('20' + studentID[1:3])
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s WHERE studentID = "%s"' % (self.table_name, studentID))
        if not cursor.fetchall():
            insert_head = 'INSERT INTO %s VALUES' % self.table_name
            cursor.execute(insert_head + '(%s, %s, NULL)', (entrance_year, studentID))
        self.DB.commit()

    def register_estimated_studentIDs(self, root_dir):
        """Registers entire estimated students information into the database
            Good(11/20/2017)

        It uses some directory like the folder "www.cc.kyoto-su.ac.jp"
        Args:
            root_dir: A string of directory that has students information.
        """
        for folder_name in os.listdir(root_dir):
            matcher = Constants.STUDENT_ID_RE.search(folder_name)
            if matcher:
                self.register_estimated_studentID(matcher.group())

    def register_studentIDs_ranging(self, begin_sID, end_sID):
        """Registers specified students information into the database
            Good(11/20/2017)

        Args:
            begin_sID: A string of student id which is the ranging head.
            end_sID: A string of student id which is the ranging tail.
        """
        for studentID in self.get_studentIDs_from(begin_sID, end_sID):
            self.register_estimated_studentID(studentID)

    def label_traced_students_ranging(self, begin_sID, end_sID, traced_date):
        """Add a label if the system downloaded files using the input range.
            Good(11/20/2017)
        Args:
            begin_sID: A string of student id which is the ranging head.
            end_sID: A string of student id which is the ranging tail.
            traced_date: A date the system downloaded files using the 'wget' command.
                (ex. '2017-11-20')
        """
        cursor = self.DB.cursor()
        studentIDs = self.get_studentIDs_from(begin_sID, end_sID)
        self.label_traced_students(studentIDs, traced_date)

    def label_traced_students(self, studentIDs, traced_date):
        """Add a label if the system downloaded files using a studentID list.
            Good(11/20/2017)
        Args:
            studentIDs: A list of strings of student id.
                (ex. ['g0811111','g1111116'])
            traced_date: A date the system downloaded files using the 'wget' command.
                (ex. '2017-11-20')
        """
        cursor = self.DB.cursor()
        for studentID in studentIDs:
            update_head = 'UPDATE %s SET ' % self.table_name
            cursor.execute(update_head + 'traced_date = %s WHERE studentID = %s', (traced_date, studentID))
        self.DB.commit()
        
    def get_studentIDs_from(self, begin_sID, end_sID):
        """Gets student ids from begin_sID and end_sID
            Good(11/20/2017)
        Args:
            begin_sID: A string of student id which is the ranging head.
            end_sID: A string of student id which is the ranging tail.
        Returns:
            A list of strings of student id. (ex. ['g0811111','g1111116'])
        """
        studentIDs = []
        for studentID_tail in range(int(begin_sID[1:]), int(end_sID[1:])+1):
            studentID = "g" + str(studentID_tail).zfill(7)
            combined_number = sum([int(c) for c in studentID[2:]])
            if combined_number % 10 == 0:
                studentIDs.append(studentID)
        return studentIDs

    def get_unknown_grades(self):
        """Gets unknown grades
        Returns:
            A list of grade numbers. (ex. [9, 8, 6, 5, 1])
        """
        freshman_entrance_year = Constants.get_year(1) #1=freshman

        unknown_grades = []
        cursor = self.DB.cursor()
        for entrance_year in range(Constants.ENTRANCE_YEAR_OF_OLDEST_OB, freshman_entrance_year+1):
            cursor.execute('SELECT entrance_year FROM %s WHERE entrance_year = "%s"' % (self.table_name, entrance_year))
            if not cursor.fetchall():
                unknown_grades.append(Constants.get_grade(entrance_year))
        return unknown_grades

    def get_estimated_studentIDs(self):
        """Gets entire estimated student IDs
        Returns:
            A list of strings of student id. (ex. ['g0811111','g1111116'])
        """
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s' % self.table_name)
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]
        
    def get_estimated_studentIDs_from(self, entrance_year):
        """Gets estimated student IDs from entrance year
        Args:
            entrance_year: A number of entrance year. (ex. 2016)
        Returns:
            A list of strings of student id. (ex. ['g0811111','g1111116'])
        """
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s WHERE entrance_year = "%s"' % (self.table_name, entrance_year))
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]


    def get_not_traced_students_yet(self):
        """Gets student ids which is not traced yet.
        Returns:
            A list of strings of a grade and a student id . (ex. [[10, 'g0811111'],[10, 'g0811003']])
        """
        cursor = self.DB.cursor()
        cursor.execute("SELECT entrance_year, studentID FROM %s WHERE ifnull(length(traced_date), 0) = 0"% self.table_name)
        return [[Constants.get_grade(row_line[0]), row_line[1].encode('utf-8')] for row_line in cursor.fetchall()]

    def close(self):
        """Closes the DB connection"""
        self.DB.close()


def check():
    DB = SQLAuth().connection
    manager = EstimatedStudentDBManager(DB, "estimated_cse_students_example")
    manager.register_estimated_studentID("g0811111")
    manager.register_estimated_studentID("g1111116")
    from datetime import date
    manager.label_traced_students(["g1111116","g0811111"], date.today())
    manager.register_estimated_studentIDs(Constants.CC_DOMAIN)

    manager.register_studentIDs_ranging("g0846002", "g0847498")
    print manager.get_unknown_grades()
    print manager.get_estimated_studentIDs()
    print manager.get_estimated_studentIDs_from(2011)
    print manager.get_not_traced_students_yet()
    manager.close()


def main():
    """Run an example for an EstimatedStudentDBManager class."""
    check()
    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
