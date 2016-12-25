import os
import filecmp
import os.path
from constants import Constants
import dlconfig

ksu_template_index = "ksu_index.html"


def delete_garbage_directory(path):
    

def delete_garbage_one_page(path):
    is_delete = filecmp.cmp(path + "/index.html", ksu_template_index) and filecmp.cmp(path + "/index-j.html", ksu_template_index)
    print is_delete


delete_garbage_pages("http://www.cc.kyoto-su.ac.jp")

