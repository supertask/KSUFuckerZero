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
import botocore.session
#import pkg_resources
#print pkg_resources.get_distribution("boto3").version
#boto3.set_stream_logger()

from constants import Constants
from botocore.exceptions import ClientError


class Uploader:
    def __init__(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
        #print os.getcwd()
        #print open("/home/ec2-user/.aws/credentials",'r').read()
        #print open("/home/ec2-user/.aws/config",'r').read()
        self.bucket = s3.Bucket('fuckin-face-bucket')
        
    def run(self, folder_name):
        # upload to S3
        try:
            self.upload_to_s3(folder_name)
        except Exception, e:
            raise e
            print '[ERROR] upload to S3 has been failed.'
        print '[OK] upload to S3 bucket has successfully completed. :)'

    def upload_to_s3(self, folder_name):
        # connect to S3
        # upload with metadata and publish
        fc = 0
        for path in self.upload_files(folder_name):
            a_file = open(path, 'rb')
            #print "Uploading....."
            self.bucket.put_object(Key=path, Body=a_file)
            print 'Uploaded %s into S3' % path
            fc += 1
        print '[OK] %s files are uploaded.' % fc

    def upload_files(self, basedir):
        parent_dir = os.path.dirname(os.path.realpath(basedir))
        for (path, dirs, files) in os.walk(basedir):
            #print path
            for fn in files:
                if fn.startswith('.'):
                    continue
                relpath = os.path.join(path, fn)
                yield relpath

def main():
    #Uploader().run("tmp")
    Uploader().run(Constants.CC_DOMAIN)
    Uploader().run(Constants.CSE_DOMAIN)

    return Constants.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
