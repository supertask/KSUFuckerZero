#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KSU Fucker
# -----------------
# Author:
#     Tasuku TAKAHASHI (supertask.jp
# Coding style:
#     Google Python Style Guide
#     https://google.github.io/styleguide/pyguide.html
#

import os
import sys
from constants import Constants
import dlconfig
from tool import Tool

# This means someone who has a secret folder can use this package ;)
from secret.auth import SQLAuth

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



class StudentDBManager(object):
    """ A database manager for storing student informations.
    """
    def __init__(self, DB, table_name):
        """Inits the class and creates the table.
            Good(11/20/2017)
        Args:
            DB: A database connection
            table_name: A string of a table name for a student database
        """
        self.DB = DB
        self.table_name = table_name
        #self.DB.text_factory = lambda x: unicode(x, "utf-8", "ignore") #for SQLite
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(entrance_year SMALLINT, studentID VARCHAR(12), firstnames TEXT, lastnames TEXT, page_keywords TEXT, page_titles TEXT, page_paths TEXT, image_links TEXT, faceimage_position TEXT, coding_size INT)' % self.table_name)


    def __convert_to_string(self, attributes):
        """Encodes charactors and converts from list to string.
        Args:
            attributes: A list of a list of strings like above.
                (ex. [['tennis','soccer',...], ....])
        Returns:
            A list of strings of many keywords like above.  (ex.  -> ["tennis,soccer", ...])
        """
        return map(lambda x: Tool.conv_encoding(Constants.SPLIT_CHAR.join(x)), attributes)


    def register_HTML(self, studentID, firstnames, lastnames, page_keywords,
        page_titles, page_paths, coding_size):
        """Registers HTML informations analyzed HTML pages by MeCab into the database.
            And this is used by a StudentAnalyzer class.

        Args:
            studentID: A string of student id which is the ranging head
            firstnames: A list of strings of an ESTIMATED student first name
                 (ex. ['Tasuku','Task', 'Tasuuu'])
            lastnames: A list of strings of an ESTIMATED student last name
                (ex. ['Takahashi','Takashima', 'Aoki'])
            page_keywords: A list of strings of a page keyword
                (ex. ['tennis','rock', 'engineer'])
            page_titles: A list of strings of a page title
                (ex. ['Why japanese people?','What is PPAP?', ...])
            page_paths: A list of strings of a page path
                (ex. ['cc.kyot-su.ac.jp/~i1558129/why_japanese.html', ...])
            coding_size: A number of sum of page lines (ex. 205151)
        """
        entrance_year = int('20' + studentID[1:3])
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s WHERE studentID = "%s"' % (self.table_name, studentID))
        some_attributes = [firstnames, lastnames, page_keywords]

        if cursor.fetchall():
            cursor.execute('SELECT firstnames,lastnames,page_keywords,page_titles,page_paths,coding_size FROM %s WHERE studentID = "%s"' % (self.table_name, studentID))
            updating_attributes = list(cursor.fetchall()[0])

            for i in range(len(some_attributes)):
                if updating_attributes[i]:
                    some_attributes[i] = set(map(Tool.conv_encoding, some_attributes[i]))
                    attr = set(updating_attributes[i].split(Constants.SPLIT_CHAR)) | some_attributes[i]
                    updating_attributes[i] = Constants.SPLIT_CHAR.join(attr)
                else:
                    some_attributes = self.__convert_to_string(some_attributes)
                    updating_attributes[i] = some_attributes[i]

            updating_attributes[len(some_attributes):] = self.__convert_to_string([page_titles, page_paths]) + [coding_size]
            update_head = 'UPDATE %s SET ' % self.table_name
            cursor.execute(update_head + 'firstnames=%s,lastnames=%s,page_keywords=%s,page_titles=%s,page_paths=%s,coding_size=%s WHERE studentID = %s', updating_attributes + [studentID])
        else:
            some_attributes += [page_titles, page_paths]
            some_attributes = self.__convert_to_string(some_attributes)
            all_attributes = [entrance_year, studentID] + some_attributes + [None, None, coding_size]
            insert_head = 'INSERT INTO %s VALUES' % self.table_name
            cursor.execute(insert_head + '(%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)', all_attributes)
        self.DB.commit()


    def register_images(self, studentID, paths, face_rects):
        """Registers image informations analyzed HTML pages and images
            by MeCab into the database. This is used by a StudentAnalyzer class.

        Args:
            studentID: A string of student id which is the ranging head
            paths: A list of strings of an image path
                This list is sorted by face size anylized by the face library 'dlib'
                (ex. ['cc.kyot-su.ac.jp/~i1558129/japanese.jpg', ...])
            face_rects: A list of rectangles (ex. [[0,0,100,100], [10,10,200,200] ....])
        """
        cursor = self.DB.cursor()
        updating_attributes = []
        updating_attributes.append(Constants.SPLIT_CHAR.join(paths))
        face_rects = [str(r).replace(" ","") for r in face_rects]
        DOUBLE_SPLIT_CHAR = Constants.SPLIT_CHAR + Constants.SPLIT_CHAR
        #print face_rects
        updating_attributes.append(DOUBLE_SPLIT_CHAR.join(face_rects))
        update_head = 'UPDATE %s SET ' % self.table_name
        cursor.execute(update_head + 'image_links=%s,faceimage_position=%s WHERE studentID = %s', updating_attributes + [studentID])
        self.DB.commit()

    def create_index_DB(self):
        """Creates an index database dictionary for a searching system."""
        keywords_db_manager = KeywordsDBManager(Constants.KEYWORDS_DB)
        cursor = self.DB.cursor()
        cursor.execute('SELECT entrance_year,studentID,firstnames,lastnames,page_keywords,page_titles,page_paths,image_links FROM %s' % self.table_name)
        for row in cursor.fetchall():
            keywords = [str(row[0]), row[1]] + row[2].split(Constants.SPLIT_CHAR) + row[3].split(Constants.SPLIT_CHAR) + row[4].split(Constants.SPLIT_CHAR)
            keywords_db_manager.register(row[1], keywords)
        keywords_db_manager.create_index_for_speed()
        keywords_db_manager.close()

    def close(self):
        """Closes the DB connection"""
        self.DB.close()


class KeywordsDBManager(object):
    """ A database manager for storing student keyword informations.

    The database consists of a single keyword and multiple student ids.
    So the database table is used for mapping a keyword to student ids.
    This table provides the search engine vast speed access for searching.
    It means when a user searches on the portal website, he can access quickly ;)
    And these functions are used by a StudentDBManager class above.
    """
    def __init__(self, DB, table_name):
        """Inits the class and creates the table.
            Good(11/20/2017)
        Args:
            DB: A database connection
            table_name: A string of a table name for a student database
        """
        self.DB = DB
        self.table_name = table_name
        #self.DB.text_factory = lambda x: unicode(x, "utf-8", "ignore") #for SQLite
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(keyword TEXT, studentIDs TEXT)' % self.table_name)

    def register(self, studentID, keywords):
        """Registers student ID and keywords
        Args:
            studentID: A string of student id which is the ranging head
            keywords: A list of strings of a keyword
                (ex. ['Tasuku', 'g1144704', 'tennis','rock', 'engineer'])
        """
        for keyword in keywords:
            cursor = self.DB.cursor()
            cursor.execute('SELECT studentIDs FROM %s WHERE keyword = "%s"' % (self.table_name,keyword))
            row = cursor.fetchone()
            if row:
                studentIDs = row[0].split(Constants.SPLIT_CHAR)
                studentIDs.append(studentID)
                studentIDs_line = Constants.SPLIT_CHAR.join(set(studentIDs))
                update_head = 'UPDATE %s SET ' % self.table_name
                cursor.execute(update_head + 'studentIDs=? WHERE keyword="%s"', (keyword, studentIDs_line))
            else:
                insert_head = 'INSERT INTO %s VALUES' % self.table_name
                cursor.execute(insert_head + '(%s,%s)', (keyword, studentID))
            self.DB.commit()

    def create_index_for_speed(self):
        """Creates databse index for improving the searching speed.
        """
        cursor = self.DB.cursor()
        cursor.execute('CREATE INDEX keyword_index ON %s(keyword)' % self.table_name)
        self.DB.commit()

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

    manager = StudentDBManager(DB, "cse_students_example")
    manager.close()


def main():
    """Run an example for a EstimatedStudentDBManager, StudentDBManager, and KeywordsDBManager class."""
    check()
    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
