#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KSU Fucker
# -----------------
# Author:
#     Tasuku TAKAHASHI (supertask.jp)
# Coding style:
#     Google Python Style Guide
#     https://google.github.io/styleguide/pyguide.html
#

"""deploy script to upload the files to AWS S3 bucket

Usage:
    $ python uploader_to_s3.py <folder name for deploy>
"""

import os
import sys
import boto3

BUCKET_NAME = 'fuckin-face-bucket'

def main():
    # check arguments
    if len(sys.argv) is not 2:
        print '[ERROR] wrong number of arguments. (required 1, got %s)' % len(sys.argv)
        sys.exit(1)
    _file_name = str(sys.argv[1])

    # upload to S3
    try:
        upload_to_s3(_file_name)
    except Exception, e:
        raise e
        print '[ERROR] upload to S3 has been failed.'
    print '[OK] upload to S3 bucket has successfully completed. :)'


def upload_to_s3(file_name):
    # connect to S3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    # upload with metadata and publish
    fc = 0
    for path in upload_files(file_name):
        print 'Uploading: %s' % path
        a_file = open(path, 'rb')
        bucket.put_object(Key=path, Body=a_file)
        fc += 1
    print '[OK] %s files are uploaded.' % fc


def upload_files(basedir):
    parent_dir = os.path.dirname(os.path.realpath(basedir))
    for (path, dirs, files) in os.walk(basedir):
        for fn in files:
            if fn.startswith('.'):
                continue
            relpath = os.path.join(path, fn)
            yield relpath


if __name__ == '__main__':
    main()
