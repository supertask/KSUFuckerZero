# -*- coding:utf-8 -*-
# 
# This is a fabric file helping to deploy my products
# and showing you a maintenance page as well.
# The maintenance page at 'maintenance/maintenance.html' is very simple.
# And .htaccess has a quite important role for showing maintenace page.
# Please check these out.
#
# BTW, I am following Google Python Style Guide bellow as writting this code:
#   https://google.github.io/styleguide/pyguide.html
#
# Copyright (c) 2018 Tasuku TAKAHASHI All rights reserved.
#

import os
import shutil
from fabric.api import task, run, local, cd

#WORKSPACE = '/var/lib/jenkins/workspace/'
WORKSPACE = '/Users/tasuku/Sites/'

DEPLOY_DIR = WORKSPACE + 'KSUFuckerZero/'
EX_HTACCESS = '.htaccess.no_maintenance'

def prepare():
    """Prepares for showing a maintenace page.
    """
    #Copies a maintainance page in the deploy dir into the workspace.
    shutil.copy(DEPLOY_DIR + 'maintenance/maintenance.html',
        WORKSPACE + 'maintenance.html')

def enable_maintenance():
    shutil.copy(EX_HTACCESS, '.htaccess') #.htaccess is const value

def disable_maintenance():
    os.remove('.htaccess') #.htaccess is const value


def deploy():
    """Deploys the product after enabling the maintenance page.
    """
    prepare()
    enable_maintenance()
    with cd(DEPLOY_DIR):
        #Pulls a master branch at this time
        #run('git checkout master')
        #run('git pull origin master')
        local('git checkout master')
        local('git pull origin master')
    print 'sleeping...'
    import time
    time.sleep(3) #Faked maintenance time FOR TEST
    disable_maintenance()

