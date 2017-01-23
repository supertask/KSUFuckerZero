#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import MeCab
from HTMLParser import HTMLParser
from constants import Constants
from tool import Tool
from studentDB_manager import StudentDBManager

class StudentHTMLParser(HTMLParser):
    def __init__(self, page_path):
        HTMLParser.__init__(self)
        self.content = ""
        self.page_path = page_path.replace("‾","~")
        self.page_title = ""
        self.page_size = os.path.getsize(page_path)
        self.is_content_cnt = 0
        self.is_title = False
        self.is_spam = False
        self.htmltag_re = re.compile("html|h[1-6]|body|title|center|div|span|section|header|nav|article|section|footer|form|p|ul|ol|li|dl|dt|dd|pre|table|tr|th|td|a")
        self.spam_htmltag_re = re.compile("script|style")

    def increase_parameter(self, tag, param=[1,True,True]):
        if self.htmltag_re.match(tag):
            self.is_content_cnt+=param[0]
            if tag == "title":
                self.is_title = param[1]
        if self.spam_htmltag_re.match(tag):
            self.is_spam = param[2]
    
    def handle_starttag(self, tag, attrs):
        self.increase_parameter(tag)
    
    def handle_endtag(self, tag):
        self.increase_parameter(tag,[-1,False,False])
    
    def handle_data(self, content):
        if self.is_spam: return
        if self.is_content_cnt > 0:
            if self.is_title:
                self.page_title = content.replace('\n','').encode("utf-8")
            self.content += content + " "

    def show(self):
        print "-------------"
        print self.page_title
        print self.page_path
        print self.page_size
        print "-------------"


class StudentAnalyzer(object):
    def __init__(self):
        #self.analyzing_folders = ["www.cse.kyoto-su.ac.jp/~g1544133/", "www.cse.kyoto-su.ac.jp/‾g1544133/", "www.cc.kyoto-su.ac.jp/~g1544133/", "www.cc.kyoto-su.ac.jp/‾g1544133/"]
        self.analyzing_folders = ["www.cse.kyoto-su.ac.jp","www.cc.kyoto-su.ac.jp/"]
        self.db_manager = StudentDBManager(Constants.CSE_STUDENT_DB)
        self.tagger = MeCab.Tagger("-Ochasen")
        self.content = ""
        self.back_studentID = ""
        self.page_titles = []
        self.page_paths = []
        self.page_size = 0

    def clear_features(self):
        self.__init__()

    def save_features(self):
        firstnames, lastnames, page_keywords = self.analyze_some_features()
        self.db_manager.register(self.back_studentID, firstnames, lastnames, page_keywords, self.page_titles, self.page_paths, self.page_size)
        self.clear_features()

    def analyze_HTML(self, path, studentID):
        if len(self.back_studentID) > 0 and self.back_studentID != studentID:
            self.save_features()
        with open(path, 'r') as f:
            parser = StudentHTMLParser(path)
            content = f.read()
            parser.feed(Tool.conv_encoding(content))
            self.content += parser.content.encode("utf-8") + " "
            self.page_titles.append(parser.page_title)
            self.page_paths.append(parser.page_path)
            self.page_size += parser.page_size
            parser.close()

        self.back_studentID = studentID
    

    def analyze_HTMLs(self):
        for folder in self.analyzing_folders:
            Tool.search_HTMLs(os.path.join(folder), self.analyze_HTML)
            self.save_features()

    def analyze_some_features(self):
        self.content = Constants.URL_RE.sub('', self.content)
        node = self.tagger.parseToNode(self.content)
        firstnames, lastnames, page_keywords = set(),set(),set()
        while node:
            features = node.feature.split(",")
            if features[0] == "名詞":
                if "人名" in features:
                    if "名" in features:
                        firstnames.add(node.surface)
                    elif "姓" in features:
                        lastnames.add(node.surface)
                elif "数" in features or "サ変接続" in features:
                    pass
                else:
                    page_keywords.add(node.surface)
            node = node.next
        return firstnames, lastnames, page_keywords


def main():
    """Run an example for a StudentHTMLParser class."""
    analyzer = StudentAnalyzer()
    #path = "www.cc.kyoto-su.ac.jp/~g1544133/index.html"
    #analyzer.analyze_HTML(path, "g1544133")
    analyzer.analyze_HTMLs()

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
