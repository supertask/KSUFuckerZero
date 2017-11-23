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

import sys
from page_downloader import PageDownloader
from student_analyzer import StudentAnalyzer
from uploader import Uploader
from constants import Constants
import datetime

commands = ["download_all", "upload_to_s3", "analyze_HTMLs", "create_index_DB"]

def help():
    print "SYNOPSIS"
    print ' '*4 + "python main.py <command>"
    print "COMMANDS"
    for cmd in commands:
        print ' '*4 + cmd

def main():
    """Run a main program of the KSU Fucker."""
    if len(sys.argv) < 2:
        help()
        return Constants.EXIT_SUCCESS
    cmd = sys.argv[1]
    
    #downloader = PageDownloader()
    #
    # Use it if you want to create an estimated student DB automatically.
    #
    #downloader.determine_studentID()

    #
    # Use it if you want to create an estimated student DB using your hand.
    #
    #estimated_students_db_manager = downloader.get_db_manager()
    #estimated_students_db_manager.register_studentIDs_ranging("g0846002", "g0847498") #entrance_year=2008
    #estimated_students_db_manager.register_studentIDs_ranging("g0946010", "g0947622") #entrance_year=2009
    #estimated_students_db_manager.register_studentIDs_ranging("g1044011", "g1045344") #entrance_year=2010
    #estimated_students_db_manager.register_studentIDs_ranging("g1144010", "g1145505") #entrance_year=2011
    #estimated_students_db_manager.label_traced_students_ranging("g1144010", "g1145505", datetime.date(2015,07,14))
    #estimated_students_db_manager.register_studentIDs_ranging("g1244028", "g1245397") #entrance_year=2012
    #estimated_students_db_manager.register_studentIDs_ranging("g1344018", "g1349031") #entrance_year=2013
    #estimated_students_db_manager.register_studentIDs_ranging("g1444026", "g1445539") #entrance_year=2014
    #estimated_students_db_manager.register_studentIDs_ranging("g1540074", "g1547932") #entrance_year=2015

    #
    # Download all student data using an estimated student DB above.
    #
    if cmd == "download_all":
        downloader = PageDownloader()
        downloader.download_all()
    elif cmd == "upload_to_s3":
        u = Uploader()
        u.run("tmp")
        #u.run(Constants.CC_DOMAIN)
        #u.run(Constants.CSE_DOMAIN)

    #
    # Analyze and save downloaded HTMLs into "cse_student_DB.db".
    #
    elif cmd == "analyze_HTMLs":
        analyzer = StudentAnalyzer(Constants.STUDENT_TABLE_NAME)
        analyzer.analyze_HTMLs()
        #analyzer.analyze_images()
    elif cmd == "create_index_DB":
        analyzer = StudentAnalyzer(Constants.STUDENT_TABLE_NAME)
        analyzer.create_index_DB()
    else:
        help()

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
