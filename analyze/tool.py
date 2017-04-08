#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
from constants import Constants
from collections import Counter
from HTMLParser import HTMLParser

"""
Links:
Nishina san: 947064, Choro: 245009
http://www.cse.kyoto-su.ac.jp/~g0947343/webcom/
----
Gotten using my hand cc.kyoto-su.ac.jp
----
2008: g0846002 ~ g0847498: cse
2009: g0946010 ~ g0947622: cse
2010: g1044011 ~ g1045344: cse
2011: g1144010 ~ g1145505: cse: DID!!
2012: g1244028 ~ g1245397: cse
----
Get using cc.kyoto-su.ac.jp
2013: g1344018 ~ g1345530: cse
2014: g1444026 ~ g1445548: cse
2015: g1544016 ~ g1547932: cc (almost CSE) , "Bugs" from ~g1547572
2016: g1648237: cc (総合生命:only one)

2015, 2016のcseを辿る
"""

class Tool(object):
    def __init__(self):
        self.spam_link_studentIDs = []
        self.spam_code_studentIDs = {}

    def print_most_common(self, a_list, limited_cnt):
        for element, cnt in Counter(a_list).most_common():
            if cnt < limited_cnt: break
            print element, cnt
        print "-" * 20

    def register_path(self, path_list, root, relative_path):
        path = os.path.join(root, relative_path)
        matcher = Constants.CSE_URL_DIR_RE.search(path)
        if matcher:
            found_relative_path = matcher.group(2)
            path_list.append(found_relative_path)

    def print_popular_urls(self, a_dir):
        dirs_path = []
        files_path = []
        for root, dirs, files in os.walk(a_dir, topdown=False):
            for a_dir in dirs:
                self.register_path(dirs_path, root, a_dir)
            for a_file in files:
                self.register_path(files_path, root, a_file)

        self.print_most_common(dirs_path, 10)
        self.print_most_common(files_path, 10)



    class SpamHTMLParser(HTMLParser):
        def __init__(self, studentID, path):
            HTMLParser.__init__(self)
            self.studentID = studentID
            self.path = path
            self.A_TAG = "a"
            self.spam_link_cnt = 0
        
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == self.A_TAG:
                if "href" in attrs:
                    if not attrs["href"]: return
                    matcher = Constants.CSE_URL_DIR_RE.search(attrs["href"])
                    if matcher and matcher.group(1) != self.studentID:
                        self.spam_link_cnt+=1;

    def print_spam_links_studentID(self, path, studentID):
        with open(path, 'r') as f:
            parser = self.SpamHTMLParser(studentID, path)
            content = f.read()
            parser.feed(Tool.conv_encoding(content))
            self.spam_link_studentIDs += [studentID for c in range(parser.spam_link_cnt)]
            parser.close()

    def print_spam_links_studentIDs(self, root_dir):
        self.search_HTMLs(root_dir, self.print_spam_links_studentID)
        self.print_most_common(self.spam_link_studentIDs, 0)


    def print_spam_code_studentID(self, path, studentID):
        if studentID in self.spam_code_studentIDs:
            self.spam_code_studentIDs[studentID] += os.path.getsize(path)
        else:
            self.spam_code_studentIDs[studentID] = os.path.getsize(path)

    def print_spam_code_studentIDs(self, root_dir):
        self.search_HTMLs(root_dir, self.print_spam_code_studentID)
        for studentID, filesize in sorted(self.spam_code_studentIDs.items(), key=lambda x:x[1], reverse=True):
            if filesize > 100000:
                print studentID, filesize

    @classmethod
    def search_HTMLs(self, root_dir, callback):
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for a_file in files:
                _, ext = os.path.splitext(a_file)
                if ext == '.html':
                    path = os.path.join(root, a_file)
                    matcher = Constants.STUDENT_ID_RE.search(path) #Here
                    if not matcher: return
                    studentID = matcher.group(1)
                    callback(path, studentID)
                    print path

    @classmethod
    def search_images(self, root_dir, callback):
        exts = [".jpg", ".jpeg", "png", ".gif", ".tiff", ".bmp"]
        exts += [ext.upper() for ext in exts]
        Tool.search_files_of(root_dir, callback, exts)

    @classmethod
    def search_files_of(self, root_dir, callback, exts):
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for a_file in files:
                _, ext = os.path.splitext(a_file)
                if ext in exts:
                    path = os.path.join(root, a_file)
                    matcher = Constants.STUDENT_ID_RE.search(path) #Here
                    if not matcher: return
                    studentID = matcher.group(1)
                    callback(path, studentID)
                    print path


    @classmethod
    def conv_encoding(self, data):
        """ much faster than a 'chardet' lib.
        """
        lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                'shift_jis', 'shift_jis_2004','shift_jisx0213',
                'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
                'iso2022_jp_ext','latin_1', 'ascii')
        encode = None
        for encoding in lookup:
            try:
                data = data.decode(encoding)
                encode = encoding
                break
            except:
                pass
        if isinstance(data, unicode):
            return data
        else:
            raise LookupError

def main():
    """Run an example for a Tools class."""
    tool = Tool()
    #tool.print_popular_urls("www.cse.kyoto-su.ac.jp")
    #tool.print_spam_links_studentIDs("www.cse.kyoto-su.ac.jp")
    #tool.print_spam_code_studentIDs("www.cse.kyoto-su.ac.jp")

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
