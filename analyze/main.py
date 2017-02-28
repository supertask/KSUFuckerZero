#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from studentID_downloader import StudentIDDownloader
from student_parser import StudentAnalyzer
from constants import Constants

def main():
    """Run an example for a studentIDGetter class."""
    sID_getter = StudentIDDownloader()

    #
    # Use it if you want to create an estimated student DB without using your hand.
    #
    #sID_getter.determine_studentID()

    #
    # Use it if you want to create an estimated student DB using your hand.
    #
    #estimated_students_db_manager = sID_getter.get_db_manager()
    #estimated_students_db_manager.register_studentIDs_ranging("g0846002", "g0847498") #2008
    #estimated_students_db_manager.register_studentIDs_ranging("g0946010", "g0947622") #2009
    #estimated_students_db_manager.register_studentIDs_ranging("g1044011", "g1045344") #2010
    #estimated_students_db_manager.register_studentIDs_ranging("g1144010", "g1145505") #2011
    #estimated_students_db_manager.label_traced_students_ranging("g1144010", "g1145505", datetime.date(2015,07,14))
    #estimated_students_db_manager.register_studentIDs_ranging("g1244028", "g1245397") #2012

    #
    # Download all student data using an estimated student DB above.
    #
    sID_getter.download_all()

    #
    # Analyze and save downloaded HTMLs into "cse_student_DB.db".
    #
    analyzer = StudentAnalyzer()
    #analyzer.analyze_n_save_HTMLs()
    #analyzer.analyze_n_save_images()
    analyzer.create_index_DB()

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
