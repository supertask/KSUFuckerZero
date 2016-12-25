#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

class Constants(object):
    """A class defining a fixed numer for some classes."""
    #
    # Exit statuses
    #
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1

    PROTOCOL = 'http://'
    STUDENT_ID_RE = re.compile('(g\d{7})')

def main():
    """Run an example for a Constants class."""
    print Constants.EXIT_SUCCESS
    print Constants.EXIT_FAILURE

    print Constants.PROTOCOL
    print Constants.STUDENT_ID_RE

    return Constants.EXIT_SUCCESS

if __name__ == '__main__':
    sys.exit(main())
