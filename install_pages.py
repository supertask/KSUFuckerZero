from datetime import date
import subprocess

"""
g0947064
http://www.cse.kyoto-su.ac.jp/~g0947343/webcom/
"""

#student_type_dict = {"g": "B", "i": "M"} # B=Bachelor, M=Master

def get_year(grade, date_today):
    """Estimates a year from grade using a date.

    example:
        today -> 2016
        1,2,3,4 -> 2016,2015,2014,2013
    """
    if date_today.month < 4:
        freshman_year = date_today.year - 1
    else:
        freshman_year = date_today.year
    return freshman_year - grade + 1 


def get_student_IDs(student_type, department, grades=[1,2,3,4]):
    student_IDs = []
    date_today = date.today()
    department = str(department)

    for a_grade in grades:
        a_year = str(get_year(a_grade, date_today))
        student_number_head = a_year[-1] + department
        student_ID_head = student_type + a_year[-2:] + department

        for index in range(0000, 10000): #0000~9999
            student_number = student_number_head + str(index).zfill(4)
            student_ID = student_ID_head + str(index).zfill(4)
            combined_number = sum([int(c) for c in student_number])
            if combined_number % 10 == 0:
                student_IDs.append([a_grade, student_ID])
    return student_IDs

#year = datetime.datetime.now().year
# 2016=1, 2015=2, 2014=3, 2013=4, 2012=5
domains = ["http://www.cse.kyoto-su.ac.jp", "http://www.cc.kyoto-su.ac.jp"]
each_folders = [
    [
        "index.html",
        "index-j.html"
    ],
    None,
    [
        "SouriDaijin/",
        "PL/",
        "PL/SouriDaijin/",
        "webcom/index.html",
        "webcom/report03.html",
        "webcom/report04.html",
        "webcom/report05.html",
        "webcom/1-3.html",
        "webcom/2-1.html",
        "webcom/2-2.html",
        "webcom/2-4.html",
        "webcom/2-6.html",
    ],
    None
]

student_IDs = []
student_IDs += get_student_IDs(student_type="g", department=4, grades=[1,2,3,4])
#student_IDs += get_student_IDs(student_type="i", department=5, grades=[1,2]) #gradstudent
page_cnt = 0

for domain in domains:
    for grade, student_ID in student_IDs:
        student_url = "%s/~%s/" % (domain, student_ID)

        folders = []
        for f in each_folders[:grade]:
            if f: folders+=f

        for relative_path in folders:
            url = student_url + relative_path
            #subprocess.call(["wget","-r", url])
            page_cnt+=1
            print url

print page_cnt



