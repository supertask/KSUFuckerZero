# 'g'=bachelor or 'i'=master
student_type = 'g'

# Probably, 4 is for computer science department.
department = 4 

# Grades that you want to download.
grades = [1,2,3,4]

# An entered year of oldest OB
entrance_year_of_oldestOB = 2008

# Database
estimated_cse_student_DB = "DB/estimated_cse_student_DB.db"
cse_student_DB = "DB/cse_student_DB.db"

urls_for_studentID = [
    "http://www.cc.kyoto-su.ac.jp/~%s/",
    "http://www.cc.kyoto-su.ac.jp/~%s/index-j.html"
]

urls_for_eachyear = [
    urls_for_studentID,
    None,
    [
        "http://www.cse.kyoto-su.ac.jp/~%s/",
        "http://www.cse.kyoto-su.ac.jp/~%s/index-j.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/SouriDaijin/",
        "http://www.cse.kyoto-su.ac.jp/~%s/PL/",
        "http://www.cse.kyoto-su.ac.jp/~%s/PL/SouriDaijin/",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/report03.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/report04.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/report05.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/1-3.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-1.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-2.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-4.html",
        "http://www.cse.kyoto-su.ac.jp/~%s/webcom/2-6.html",
    ],
    None
]
exclude_directories = "~mina,~tamada,~ogihara,~naohaya,~atsushi,~akiyama,~ueda,~hidehiko,~kano,~kawai,~torikai,~oomoto,~hiraishi,circle"

def get_estimated_cse_student_DB():
    return estimated_cse_student_DB

def get_cse_student_DB():
    return cse_student_DB

def get_student_type():
    return student_type

def get_department():
    return department

def get_grades():
    return grades

def get_urls(grade):
    urls = []
    for u in urls_for_eachyear[:grade]:
        if u: urls+=u
    return urls

def get_urls_for_studentID():
    return urls_for_studentID

def get_exclude_dirs():
    return exclude_directories
