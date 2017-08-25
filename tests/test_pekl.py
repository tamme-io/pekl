import pytest
import json
import boto3
import os
import sys
from random import randint

# TEST FILES
source_path = os.path.realpath(os.path.dirname(__file__)+"/../pekl")
print "source path: %s" % str(source_path)
sys.path.append(source_path)

import Pekl
pekl = Pekl.Pekl("pekl-test-transfer-bucket")

@pytest.fixture(scope="session")
def large_dictionary():
    s = ''.join(chr(97 + randint(0, 25)) for i in range(6000000))
    response_dictionary = {
        "large_text" : s
    }
    return response_dictionary


@pytest.fixture(scope="session")
def response_dictionary(large_dictionary):
    return pekl.respond(large_dictionary)



class TestPekl(object):


    def test_respondToEvent(self, response_dictionary):
        assert pekl.region == "us-east-1"
        assert pekl.bucket_name == "pekl-test-transfer-bucket"
        parsed_response = json.loads(response_dictionary)
        assert "pekl_bucket_name" in parsed_response
        assert "pekl_bucket_key" in parsed_response
        s3 = boto3.client("s3", region_name = pekl.region)
        try:
            s3.head_object(Bucket=parsed_response.get("pekl_bucket_name"), Key=parsed_response.get("pekl_bucket_key"))
        except ClientError:
            # Not found
            print "Object not found"
            assert 0


    def test_receiveEvent(self, response_dictionary, large_dictionary):
        assert pekl.region == "us-east-1"
        assert pekl.bucket_name == "pekl-test-transfer-bucket"
        parsed_response = json.loads(response_dictionary)
        event = pekl.receive(parsed_response)
        assert "large_text" in event
        assert event.get("large_text") == large_dictionary.get("large_text")
