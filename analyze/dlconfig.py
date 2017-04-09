#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# This is a download config for collecting data from "cse.kyoto-su.ac.jp".
# Copyright (c) 2016-2017 Tasuku TAKAHASHI All rights reserved.
#
# TODO(Tasuku): remove all .DS_Store.
########################################################

#
# Grades or entrance years that you want to download.
#
# [WARNING]
# FILL NUMBERS LIKE BELLOW IN 'grades' OR 'entrance_years'.
# BUT, DO NOT FILL IT IN BOTH OF THEM, PLEASE.
#
grades = [] #[1,2,3,4,5,6,7,8,9]
#entrance_years = [2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]
entrance_years = [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]

#
# Switch 'True' if you want to download student data, again.
# Switch 'False' if you want to download student data that you have not downloaded.
#
#is_overwrite_DB = False

#
# Ignore this directories when student infos are downloaded.
#
exclude_directories = "~mina,~tamada,~ogihara,~naohaya,~atsushi,~akiyama,~ueda,~hidehiko,~kano,~kawai,~torikai,~oomoto,~hiraishi,circle,~g0947343,~g0946911" #~g0947343 and ~g0946911 are spam students.
#
#
#
urls_for_eachyear = [
    #Freshman, first year student
    #None,
    [
        "http://www.cc.kyoto-su.ac.jp/~%s/",
        "http://www.cc.kyoto-su.ac.jp/~%s/index-j.html"
    ],

    #Sophomore, second year student
    None, 

    #Junior, third year student
    [
        # 
        # Links that many of CSE students use for sure.
        #
        #"http://www.cse.kyoto-su.ac.jp/~%s/",
        #"http://www.cse.kyoto-su.ac.jp/~%s/index-j.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/SouriDaijin/",
        #"http://www.cse.kyoto-su.ac.jp/~%s/PL/",
        #"http://www.cse.kyoto-su.ac.jp/~%s/PL/SouriDaijin/",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/report03.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/report04.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/report05.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/1-3.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-1.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-2.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-4.html",
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-6.html"

        # 
        # Links estimated by analyzing websites of many of CSE students.
        #
        #"http://www.cse.kyoto-su.ac.jp/~%s/sample.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/gnuplot.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/report/example.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/TextCode.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/imageConvert.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/image_test.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/general.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/tool.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/kousatu.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/result.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/circuit2.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai6.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/index4.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai5.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai7.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai8.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai3.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/index2.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai4.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/kadai1.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/index3.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/w3c.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/index5.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/kekka.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox2.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/style.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox1.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/bridge.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/W3C.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox3.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/report03.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/mado0.gif", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/menu.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/link.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/styles.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox2.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai3.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/KSU.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/page1.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/kousatsu.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai4.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/profile.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/title.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/main.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/styles-bg.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/tubame.gif", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/hyouka.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/webcom/style.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/top.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/fox4.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai7.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai1.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/page2.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/circuit.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai6.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/screenshot_01.jpg", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/example.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/screenshot_03.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/page3.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/relation.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/common.css", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/consider.html", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai5.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/screenshot_01.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/plot_kadai8.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/ProgramEnshu/screenshot_02.png", 
        #"http://www.cse.kyoto-su.ac.jp/~%s/page4.html"
    ],

    #Senior, fourth year student
    None
]
# Download information is until here
########################################################




#
# These methods bellow are used in runtime.
# Therefore, do not touch it as much as possible, please.
#
########################################################
import sys
from constants import Constants

def get_exclude_dirs(): return exclude_directories
def get_grades():
    if grades: return grades
    else:
        return [Constants.get_grade(y) for y in entrance_years]

def get_urls(grade):
    urls = []
    for u in urls_for_eachyear[:grade]:
        if u: urls+=u
    return urls


def main():
    """Run an example for a download config."""
    print get_grades()
    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
