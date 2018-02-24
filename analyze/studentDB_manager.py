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
from db_auth import SQLAuth

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


    def __get_comma_line_on_each(self, attributes):
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
        #print some_attributes #ここまではOK

        if cursor.fetchall():
            # Second insert or more
            cursor.execute('SELECT firstnames,lastnames,page_keywords,page_titles,page_paths,coding_size FROM %s WHERE studentID = "%s"' % (self.table_name, studentID))
            updating_attributes = list(cursor.fetchall()[0]) #One result, all the time

            some_attributes += [page_titles, page_paths]
            updating_attributes = self.__get_comma_line_on_each(some_attributes) + [coding_size]
            #for s in updating_attributes: print s

            update_head = 'UPDATE %s SET ' % self.table_name
            cursor.execute(update_head + 'firstnames=%s,lastnames=%s,page_keywords=%s,page_titles=%s,page_paths=%s,coding_size=%s WHERE studentID = %s', updating_attributes + [studentID])
        else:
            # First insert
            some_attributes += [page_titles, page_paths]
            some_attributes = self.__get_comma_line_on_each(some_attributes)
            all_attributes = [entrance_year, studentID] + some_attributes + [None, None, coding_size]
            insert_head = 'INSERT INTO %s VALUES' % self.table_name
            cursor.execute(insert_head + '(%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)', all_attributes)
        self.DB.commit()


    def register_images(self, studentID, paths):
        """Registers image informations analyzed HTML pages and images
            by MeCab into the database. This is used by a StudentAnalyzer class.

        Args:
            studentID: A string of student id which is the ranging head
            paths: A list of strings of an image path
                This list is sorted by face size anylized by the face library 'dlib'
                (ex. ['cc.kyot-su.ac.jp/~i1558129/japanese.jpg', ...])
        """
        cursor = self.DB.cursor()
        updating_attributes = []
        updating_attributes.append(Constants.SPLIT_CHAR.join(paths))
        #face_rects = [str(r).replace(" ","") for r in face_rects]
        DOUBLE_SPLIT_CHAR = Constants.SPLIT_CHAR + Constants.SPLIT_CHAR
        #updating_attributes.append(DOUBLE_SPLIT_CHAR.join(face_rects))
        empty_rects = ['' for path in paths]
        updating_attributes.append(DOUBLE_SPLIT_CHAR.join(empty_rects))
        update_head = 'UPDATE %s SET ' % self.table_name
        cursor.execute(update_head + 'image_links=%s,faceimage_position=%s WHERE studentID = %s', updating_attributes + [studentID])
        self.DB.commit()

    #TODO(Tasuku): Needs to have studentID who starts as input
    def create_index_DB(self):
        """Creates an index database dictionary for a searching system."""
        keywords_db_manager = KeywordsDBManager(SQLAuth().connection, Constants.KEYWORDS_TABLE_NAME)
        cursor = self.DB.cursor()
        cursor.execute('SELECT entrance_year,studentID,firstnames,lastnames,page_keywords,page_titles,page_paths,image_links FROM %s' % self.table_name)
        print "Starts a create index DB function"
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
            if keyword == '': continue
            cursor = self.DB.cursor()
            cursor.execute('SELECT studentIDs FROM %s WHERE keyword = "%s"' % (self.table_name,keyword))
            row = cursor.fetchone()
            if row:
                studentIDs = row[0].split(Constants.SPLIT_CHAR)
                studentIDs.append(studentID)
                studentIDs_line = Constants.SPLIT_CHAR.join(set(studentIDs))
                update_head = 'UPDATE %s SET ' % self.table_name
                cursor.execute(update_head + 'studentIDs=%s WHERE keyword=%s', (studentIDs_line, keyword))
            else:
                insert_head = 'INSERT INTO %s VALUES' % self.table_name
                cursor.execute(insert_head + '(%s,%s)', (keyword, studentID))
            print cursor._executed
        self.DB.commit()

    def create_index_for_speed(self):
        """Creates databse index for improving the searching speed.
        """
        cursor = self.DB.cursor()
        exec_line = 'CREATE INDEX keyword_index ON %s(keyword(255))' % self.table_name
        try:
            cursor.execute(exec_line)
        except:
            print "Duplicate key name. But it's fine. Don't care about that."

        self.DB.commit()

    def close(self):
        """Closes the DB connection"""
        self.DB.close()


def check():
    DB = SQLAuth().connection
    manager = StudentDBManager(DB, "cse_students_example")
    manager.close()


def main():
    """Run an example for StudentDBManager and KeywordsDBManager classes."""
    check()
    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
