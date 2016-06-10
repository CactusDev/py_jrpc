"""
Test cases for the JSON-RPC module

Perfect 10.00/10 pylint score!
"""

import json_rpc
from json_rpc import JSONRPCTypes, JSONRPCException

"""
The MIT License (MIT)

Copyright (c) 2016 RPiAwesomneness

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def print_results(success, errors, should_pass=True, type=None):
    if type is not None:
        print("Type:\t", type)
    print("Pass:\t", success)
    print("Errors:  {}".format(errors))
    print("Success: {}\n".format(success == should_pass))
    print("---------------------------------------------------------")


def run_validate_test(packet, j_type, should_pass=True):
    """
    Takes the data for the test case and displays output
    """
    success, errors = json_rpc.verify_packet(packet, j_type)
    print_results(success, errors, should_pass=should_pass)


# ---------------------------------------------------
# Response tests
# ---------------------------------------------------
VERIFY_VALIDATE = []

# Create the packet in dict form
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "result": "Success! It's working!"
}

# Append tuple:
#   packet: The JSON-RPC packet to test
#       REQUIRED
#   j_type: JSONRPCTypes object to test packet against
#       REQUIRED
#   should_pass: Boolean on whether or not it *should* pass)
#       REQUIRED - set to None if unknown what result should be
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, True))

# Fail (incorrect jsonrpc value)
TEST = {
    "jsonrpc": "3.0",
    "id": 13,
    "result": "Success! It's working!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (incorrect jsonrpc value, missing key "id")
TEST = {
    "jsonrpc": "3.0",
    "result": "Success! It's working!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "jsonrpc", missing key "result")
TEST = {
    "id": 13,
    "resul": "Success! It's working!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "id")
TEST = {
    "jsonrpc": "2.0",
    # "id": 13,
    "result": "Success! It's working!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "jsonrpc", missing key "id", missing key "result")
TEST = {
    # "jsonrpc": "2.0",
    # "id": 13,
    # "result": "Success! It's working!"
    "spam": "eggs"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Pass
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, True))

# Fail (incorrect error code)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32601,
        "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing both "error" and "result" keys)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    # "error": {
    #     "code": -32600,
    #     "message": "Invalid Request"
    # }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing error message)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        # "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing error code)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        # "code": -32600,
        "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (both "error" and "result" are included)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        "message": "Invalid Request"
    },
    "result": "Success!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (error code isn't type int)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": "-32600",
        "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (error code is in range of reserved JSON-RPC codes)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32012,
        "message": "Invalid Request"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.RESPONSE, False))

# ---------------------------------------------------
# Notification tests
# ---------------------------------------------------

# Pass
TEST = {
    "jsonrpc": "2.0",
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.NOTIF, True))

# Fail (notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.NOTIF, False))

# Fail (missing required 'method' key, notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    # "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.NOTIF, False))

# ---------------------------------------------------
# Request tests
# ---------------------------------------------------

# Pass
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.REQUEST, True))

# Fail (missing ID, missing required key 'method')
TEST = {
    "jsonrpc": "2.0",
    # "id": 13,
    # "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail (method starts with JSON-RPC reserved for internal use value 'rpc.')
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "rpc.queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail ('params' key isn't structured type (list or dict))
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": "The crown has been stolen!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail ('method' key isn't type str,
#       'params' key isn't structured type (list or dict))
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": 14,
    "params": "The crown has been stolen!"
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.REQUEST, False))

# ---------------------------------------
# Begin running test cases
# ---------------------------------------
for test in VERIFY_VALIDATE:
    run_validate_test(test[0], test[1], should_pass=test[2])

# ---------------------------------------
# Begin testing of packet creation
# ---------------------------------------
VERIFY_CREATE_REQUEST = []
VERIFY_CREATE_RESULT = []
VERIFY_CREATE_ERROR = []

# ---------------------------------------
# Request creation
# ---------------------------------------
# To test, create a dict of the values you would pass to JSONRPCRequest
#   and append that in a tuple to VERIFY_CREATE_REQUEST with True/False
#   as the second value in the tuple as to whether or not it should pass

# Pass
test = {
    "response_id": 1,
    "method": "spam:eggs",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
should_pass = True
VERIFY_CREATE_REQUEST.append((test, should_pass))

# Pass
test = {
    "response_id": 1,
    "method": "spam:eggs",
    "params": ["spam", "beautiful", "spam"]
}
should_pass = True
VERIFY_CREATE_REQUEST.append((test, should_pass))

# Pass
test = {
    "response_id": 1,
    "method": "spam:eggs",
}
should_pass = True
VERIFY_CREATE_REQUEST.append((test, should_pass))

# Fail (response_id is a str)
test = {
    "response_id": "YOU SHALL NOT PASS!",
    "method": "spam:eggs",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
should_pass = False
VERIFY_CREATE_REQUEST.append((test, should_pass))

# Fail (method starts with JSON-RPC reserved string 'rpc.')
test = {
    "response_id": 1,
    "method": "rpc.spam",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
should_pass = False
VERIFY_CREATE_REQUEST.append((test, should_pass))

# Fail (method is type list)
test = {
    "response_id": 1,
    "method": ["spam", "eggs"],
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
should_pass = False
VERIFY_CREATE_REQUEST.append((test, should_pass))

# ---------------------------------------
# Error creation
# ---------------------------------------

# Pass
test = {
    "response_id": 1,
    "code": 200,
    "message": "Success",
    "data": {
        "innectic": "java < python"
    }
}
should_pass = True
VERIFY_CREATE_ERROR.append((test, should_pass))

# Pass
test = {
    "response_id": 1,
    "code": 200,
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
should_pass = True
VERIFY_CREATE_ERROR.append((test, should_pass))

# ---------------------------------------
# Result creation
# ---------------------------------------

pass

# ---------------------------------------
# Run the tests
# ---------------------------------------


for test in VERIFY_CREATE_REQUEST:
    error = None
    try:
        json_rpc.JSONRPCRequest(**test[0])
        success = True
    except JSONRPCException as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, test[1], "REQUEST")

for test in VERIFY_CREATE_ERROR:
    error = None
    try:
        json_rpc.JSONRPCError(**test[0])
        success = True
    except JSONRPCException as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, test[1], "ERROR")

for test in VERIFY_CREATE_RESULT:
    error = None
    try:
        json_rpc.JSONRPCResult(**test[0])
        success = True
    except JSONRPCException as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, test[1], "RESULT")

# Will return JSON-RPC Error packet for code -32700
print(json_rpc.generate_error_packet(-32700))
# Will return JSON-RPC Error packet for "Invalid Request"
print(json_rpc.generate_error_packet("Invalid Request"))
