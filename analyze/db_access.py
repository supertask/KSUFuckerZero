#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#

from secret.auth import SQLAuth

cnx = SQLAuth().connection
cur = cnx.cursor(buffered=True)

cur.execute('show tables;')
print(cur.fetchall())
cur.execute('select * from estimated_cse_students;')
print(cur.fetchone())
cur.execute('select * from estimated_cse_students;')
print(cur.fetchone())

cur.close()
cnx.close()
