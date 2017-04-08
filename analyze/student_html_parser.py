#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os.path
from HTMLParser import HTMLParser

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
