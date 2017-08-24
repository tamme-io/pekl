import pytest
import json
import boto3
import os
import sys

# TEST FILES
source_path = os.path.realpath(os.path.dirname(__file__)+"/../pekl")
print "source path: %s" % str(source_path)
sys.path.append(source_path)

import Pekl

class TestPekl(object):

    def test_receiveEvent(self):
        assert 1


    def test_respondToEvent(self):
        assert 1
