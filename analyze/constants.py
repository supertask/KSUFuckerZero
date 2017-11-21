#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from datetime import date

class Constants(object):
    """A class defining a fixed numer for some classes."""
    #
    # Exit statuses
    #
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1

    #
    # Regular expression for finding any strings.
    #
    STUDENT_ID_RE = re.compile('(g\d{7})')
    DOMAIN_RE = re.compile('http[s]?://((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
    URL_RE =    re.compile('http\S+')
    CSE_URL_DIR_RE = re.compile("www\.cse\.kyoto-su\.ac\.jp\/.*(g\d{7})\/(.*)")
    CSE_DOMAIN_RE = re.compile("www\.cse\.kyoto-su\.ac\.jp")

    KSU_TEMPLATE_INDEX = "ksu_index.html"

    #
    # 'g'=bachelor or 'i'=master
    # Ex: g1144704 -> 'g'1144704, i1558129 -> 'i'1558129
    #
    STUDENT_TYPE = 'g'

    #
    # Probably, 4 is for computer science department.
    # Ex: g1144704 -> g11'4'4704
    #
    DEPARTMENT = 4 

    #
    # A date object indicated today for timestamp, for instance, '2016-12-25'.
    #
    TODAY = date.today()

    #
    # Analyzing domain names plus downloaded folder names.
    #
    CC_DOMAIN = "www.cc.kyoto-su.ac.jp"
    CSE_DOMAIN = "www.cse.kyoto-su.ac.jp"

    #
    # This URLs is used for determining a student id.
    #
    URLS_FOR_DETERMINING_STUDENT_ID = [
        "http://www.cc.kyoto-su.ac.jp/~%s/",
        "http://www.cc.kyoto-su.ac.jp/~%s/index-j.html"
    ]

    #
    # An entrance year of oldest OB.
    #
    ENTRANCE_YEAR_OF_OLDEST_OB = 2008

    #
    # Tables in database
    #
    ESTIMATED_STUDENT_TABLE_NAME = "estimated_cse_students"
    STUDENT_TABLE_NAME = "cse_students"
    KEYWORDS_TABLE_NAME = "keywords"

    #
    # A spliting charactor for a list element of the database
    #
    SPLIT_CHAR = ","

    #
    #
    #
    ANALYZING_FOLDERS = ["www.cse.kyoto-su.ac.jp/", "www.cc.kyoto-su.ac.jp/"]


    @classmethod
    def get_grade(self, year):
        """Estimates a grade from an entrance year using a date.

        Example:
            if today -> 2016
            2016,2015,2014,2013 -> 1,2,3,4
        """
        if Constants.TODAY.month < 4:
            freshman_year = Constants.TODAY.year - 1
        else:
            freshman_year = Constants.TODAY.year
        return freshman_year - year + 1 

    @classmethod
    def get_year(self, grade):
        """Estimates a year from grade using a date.

        Example:
            if today -> 2016
            1,2,3,4 -> 2016,2015,2014,2013
        """
        if Constants.TODAY.month < 4:
            freshman_year = Constants.TODAY.year - 1
        else:
            freshman_year = Constants.TODAY.year
        return freshman_year - grade + 1 


def main():
    """Run an example for a Constants class."""
    print Constants.EXIT_SUCCESS
    print Constants.EXIT_FAILURE

    print Constants.STUDENT_ID_RE

    #2016,2015,2014,2013 -> 1,2,3,4
    print Constants.get_grade(2016)
    print Constants.get_grade(2015)
    print Constants.get_year(1)
    print Constants.get_year(2)
    for year in [2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]:
        assert Constants.get_year(Constants.get_grade(year)) == year

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
