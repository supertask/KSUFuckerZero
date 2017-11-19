#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from constants import Constants
import dlconfig
from tool import Tool

# This means someone who has a secret folder can use this package ;)
from secret.auth import SQLAuth

class EstimatedStudentDBManager(object):
    """ A data base manager for storing estimated students.

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
        """ Inits the class and creates the table.
            Good(11/20/2017)
        Args:
            table_name - A string of a table name of estimated students
        """
        self.DB = DB
        self.table_name = table_name
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(entrance_year SMALLINT, studentID VARCHAR(12), traced_date DATE)' % self.table_name)

    def register_estimated_studentID(self, studentID):
        """ Registers estimated single student id into the database.
            Good(11/20/2017)
        Args:
            studentID - A string of student id in school. (ex: 'g0811111')
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
        """ Registers entire estimated students information into the database
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
        for studentID in self.get_studentIDs_from(begin_sID, end_sID):
            self.register_estimated_studentID(studentID)

    def label_traced_students_ranging(self, begin_sID, end_sID, traced_date):
        cursor = self.DB.cursor()
        studentIDs = self.get_studentIDs_from(begin_sID, end_sID)
        self.label_traced_students(studentIDs, traced_date)

    def label_traced_students(self, studentIDs, traced_date):
        """ Add a label if students traced.
            Good(11/20/2017)
        Args:
            studentIDs: A list of strings of student id.
                (ex: ['g0811111','g1111116'])
            traced_date: A date the system downloaded files using the 'wget' command.
                (ex: '2017-11-20')
        """
        cursor = self.DB.cursor()
        for studentID in studentIDs:
            update_head = 'UPDATE %s SET ' % self.table_name
            cursor.execute(update_head + 'traced_date = %s WHERE studentID = %s', (traced_date, studentID))
        self.DB.commit()
        

    def get_studentIDs_from(self, begin_sID, end_sID):
        studentIDs = []
        for studentID_tail in range(int(begin_sID[1:]), int(end_sID[1:])+1):
            studentID = "g" + str(studentID_tail).zfill(7)
            combined_number = sum([int(c) for c in studentID[2:]])
            if combined_number % 10 == 0:
                studentIDs.append(studentID)
        return studentIDs


    def get_unknown_grades(self):
        freshman_entrance_year = Constants.get_year(1) #1=freshman

        unknown_grades = []
        cursor = self.DB.cursor()
        for entrance_year in range(Constants.ENTRANCE_YEAR_OF_OLDEST_OB, freshman_entrance_year+1):
            cursor.execute('SELECT entrance_year FROM %s WHERE entrance_year = "%s"' % (self.table_name, entrance_year))
            if not cursor.fetchall():
                unknown_grades.append(Constants.get_grade(entrance_year))
        return unknown_grades

    def get_estimated_studentIDs(self):
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s' % self.table_name)
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]
        
    def get_estimated_studentIDs_from(self, entrance_year):
        cursor = self.DB.cursor()
        cursor.execute('SELECT studentID FROM %s WHERE entrance_year = "%s"' % (self.table_name, entrance_year))
        return [studentID[0].encode('utf-8') for studentID in cursor.fetchall()]


    def get_not_traced_students_yet(self):
        cursor = self.DB.cursor()
        cursor.execute("SELECT entrance_year, studentID FROM %s WHERE ifnull(length(traced_date), 0) = 0"% self.table_name)
        return [[Constants.get_grade(row_line[0]), row_line[1].encode('utf-8')] for row_line in cursor.fetchall()]

    def close(self):
        self.DB.close()


class StudentDBManager(object):
    def __init__(self, DB, table_name):
        self.DB = DB
        self.table_name = table_name
        #self.DB.text_factory = lambda x: unicode(x, "utf-8", "ignore") #for SQLite
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(entrance_year SMALLINT, studentID VARCHAR(12), firstnames TEXT, lastnames TEXT, page_keywords TEXT, page_titles TEXT, page_paths TEXT, image_links TEXT, faceimage_position TEXT, coding_size INT)' % self.table_name)


    def create_index_DB(self):
        keywords_db_manager = KeywordsDBManager(Constants.KEYWORDS_DB)
        cursor = self.DB.cursor()
        cursor.execute('SELECT entrance_year,studentID,firstnames,lastnames,page_keywords,page_titles,page_paths,image_links FROM %s' % self.table_name)
        for row in cursor.fetchall():
            keywords = [str(row[0]), row[1]] + row[2].split(Constants.SPLIT_CHAR) + row[3].split(Constants.SPLIT_CHAR) + row[4].split(Constants.SPLIT_CHAR)
            keywords_db_manager.register(row[1], keywords)
        keywords_db_manager.create_index_for_speed()


    def convert_to_string(self, attributes):
        """Convert a list of a list to a list of string.
        """
        return map(lambda x: Tool.conv_encoding(Constants.SPLIT_CHAR.join(x)), attributes)

    def register_HTML(self, studentID, firstnames, lastnames, page_keywords, page_titles, page_paths, coding_size):
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
                    some_attributes = self.convert_to_string(some_attributes)
                    updating_attributes[i] = some_attributes[i]

            updating_attributes[len(some_attributes):] = self.convert_to_string([page_titles, page_paths]) + [coding_size]
            cursor.execute('UPDATE %s SET firstnames=?,lastnames=?,page_keywords=?,page_titles=?,page_paths=?,coding_size=? WHERE studentID = ?' % self.table_name, updating_attributes + [studentID])
        else:
            some_attributes += [page_titles, page_paths]
            some_attributes = self.convert_to_string(some_attributes)
            all_attributes = [entrance_year, studentID] + some_attributes + [None, None, coding_size]
            cursor.execute('INSERT INTO %s VALUES(?,?,?,?,?, ?,?,?,?,?)' % self.table_name, all_attributes)
        self.DB.commit()


    def register_images(self, studentID, paths, face_rects):
        cursor = self.DB.cursor()
        updating_attributes = []
        updating_attributes.append(Constants.SPLIT_CHAR.join(paths))
        face_rects = [str(r).replace(" ","") for r in face_rects]
        DOUBLE_SPLIT_CHAR = Constants.SPLIT_CHAR + Constants.SPLIT_CHAR
        #print face_rects
        updating_attributes.append(DOUBLE_SPLIT_CHAR.join(face_rects))
        cursor.execute('UPDATE %s SET image_links=?,faceimage_position=? WHERE studentID = ?' % self.table_name, updating_attributes + [studentID])
        self.DB.commit()

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
        """

class KeywordsDBManager(object):
    def __init__(self, DB, table_name):
        self.DB = DB
        self.table_name = table_name
        #self.DB.text_factory = lambda x: unicode(x, "utf-8", "ignore") #for SQLite
        cursor = self.DB.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS %s(keyword TEXT, studentIDs TEXT)' % self.table_name)

    def register(self, studentID, keywords):
        for keyword in keywords:
            cursor = self.DB.cursor()
            cursor.execute('SELECT studentIDs FROM %s WHERE keyword = "%s"' % (self.table_name,keyword))
            row = cursor.fetchone()
            if row:
                studentIDs = row[0].split(Constants.SPLIT_CHAR)
                studentIDs.append(studentID)
                studentIDs_line = Constants.SPLIT_CHAR.join(set(studentIDs))
                cursor.execute('UPDATE %s SET studentIDs=? WHERE keyword="%s"' % (self.table_name, keyword), [studentIDs_line])
            else:
                cursor.execute('INSERT INTO %s VALUES(?,?)' % self.table_name, [keyword, studentID])
            self.DB.commit()

    def create_index_for_speed(self):
        cursor = self.DB.cursor()
        cursor.execute('CREATE INDEX keyword_index on %s(keyword)' % self.table_name)
        self.DB.commit()


def test():
    DB = SQLAuth().connection
    manager = EstimatedStudentDBManager(DB, "sample_estimated_students")
    manager.register_estimated_studentID("g0811111")
    manager.register_estimated_studentID("g1111116")

    from datetime import date
    manager.label_traced_students(["g1111116","g0811111"], date.today())

    manager.register_estimated_studentIDs(Constants.CC_DOMAIN)

    """
    print manager.get_unknown_grades()
    print manager.get_estimated_studentIDs()
    print manager.get_estimated_studentIDs_from(2011)
    #manager.register_estimated_studentIDs("www.cc.kyoto-su.ac.jp")
    """
    manager.close()


def main():
    """Run an example for a EstimatedStudentDBManager and StudentDBManager class."""
    test()

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
