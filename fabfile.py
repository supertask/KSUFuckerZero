# -*- coding:utf-8 -*-
# 
# This is a fabric file helping to deploy my products
# and showing you a maintenance page as well.
# The maintenance page is at './maintenance/maintenance.html'.
# And .htaccess which is at './' has a quite important role for showing maintenace page.
# Please check these out.
#
# Required:
#   $ sudo pip install fabric
#   $ sudo vim httpd.conf
#       Set paths of DocumentRoot and Directory indicate your workspace.
#       AllowOverride None -> AllowOverride All
#       Make sure that rewrite_module is commented out.
#           LoadModule rewrite_module modules/mod_rewrite.so
#   $ sudo service httpd start
#   $ fab deploy or sudo /usr/local/bin/fab deploy
#
# BTW, I am following Google Python Style Guide bellow as writting this cool code:
#   https://google.github.io/styleguide/pyguide.html
#
# Copyright (c) 2018 Tasuku TAKAHASHI All rights reserved.
#

import os
import shutil
from fabric.api import task, run, local, cd

EX_HTACCESS = '.htaccess.no_maintenance'

def enable_maintenance():
    shutil.copyfile(EX_HTACCESS, '.htaccess') #.htaccess is const value

def disable_maintenance():
    os.remove('.htaccess') #.htaccess is const value

@task
def deploy():
    """Deploys the product after enabling the maintenance page.
    """
    enable_maintenance()

    #Pulls a master branch at this time
    local('git checkout master')
    local('git pull origin master')
    print 'sleeping...'
    import time
    time.sleep(5) #Faked maintenance time FOR TEST
    disable_maintenance()


