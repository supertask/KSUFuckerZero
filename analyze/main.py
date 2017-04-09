#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from student_downloader import StudentDownloader
from student_analyzer import StudentAnalyzer
from constants import Constants
import datetime

def main():
    """Run an example for a studentIDGetter class."""
    #downloader = StudentDownloader()

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
    #downloader.download_all()

    #
    # Analyze and save downloaded HTMLs into "cse_student_DB.db".
    #
    analyzer = StudentAnalyzer()
    #analyzer.analyze_HTMLs()
    #analyzer.analyze_images()
    analyzer.create_index_DB()

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
