"""
Test cases for the JSON-RPC module

Perfect 10.00/10 pylint score!

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

import py_jrpc
from py_jrpc import JSONRPCTypes, JSONRPCException


def print_results(did_pass, errors, should_pass=True, packet_type=None):
    """
    Prints test-case results in a standardized manner
    """
    if packet_type is not None:
        print("Type:\t", packet_type)
    print("Pass:\t", did_pass)
    print("Errors:  {}".format(errors))
    print("Success: {}\n".format(did_pass == should_pass))
    print("---------------------------------------------------------")


def run_validate_test(packet, j_type, should_pass=True):
    """
    Takes the data for the test case and displays output
    """
    did_pass, errors = json_rpc.verify_packet(packet, j_type)
    print_results(did_pass, errors, should_pass=should_pass)


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

# To create a test-case for the packet generators, create a dict
#   with the keys being the argument and the data being the data as you
#   would with a call
# Example:
# test = {
#     "jsonrpc": "2.0",
#     "method": "notify:queen_of_england",
#     "params": {
#         "crown": "Has been stolen"
#     }
# }
# would be equivalen to:
#   json_rpc.JSONRPCRequest(json_rpc="2.0",
#                           method="notify:queen_of_england",
#                           params={
#                               "crown": "Has been stolen"
#                           }
#                           )

# Pass
TEST = {
    "jsonrpc": "2.0",
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    },
    "is_notif": True
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.NOTIF, True))

# Fail (notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    },
    "is_notif": True
}
VERIFY_VALIDATE.append((TEST, JSONRPCTypes.NOTIF, False))

# Fail (missing required 'method' key, notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    # "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    },
    "is_notif": True
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
# Begin running TEST cases
# ---------------------------------------
for TEST in VERIFY_VALIDATE:
    run_validate_test(TEST[0], TEST[1], should_pass=TEST[2])

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
TEST = {
    "response_id": 1,
    "method": "spam:eggs",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
SHOULD_PASS = True
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# Pass
TEST = {
    "response_id": 1,
    "method": "spam:eggs",
    "params": ["spam", "beautiful", "spam"]
}
SHOULD_PASS = True
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# Pass
TEST = {
    "response_id": 1,
    "method": "spam:eggs",
}
SHOULD_PASS = True
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# Fail (response_id is a str)
TEST = {
    "response_id": "YOU SHALL NOT PASS!",
    "method": "spam:eggs",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
SHOULD_PASS = False
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# Fail (method starts with JSON-RPC reserved string 'rpc.')
TEST = {
    "response_id": 1,
    "method": "rpc.spam",
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
SHOULD_PASS = False
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# Fail (method is type list)
TEST = {
    "response_id": 1,
    "method": ["spam", "eggs"],
    "params": {
        "foo": "bar",
        "towel": 42
    }
}
SHOULD_PASS = False
VERIFY_CREATE_REQUEST.append((TEST, SHOULD_PASS))

# ---------------------------------------
# Error creation
# ---------------------------------------

# Pass
TEST = {
    "response_id": 1,
    "code": 200,
    "message": "Success",
    "data": {
        "innectic": "java < python"
    }
}
SHOULD_PASS = True
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Pass
TEST = {
    "response_id": 1,
    "code": 200,
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = True
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Fail (missing required 'code' key)
TEST = {
    "response_id": 1,
    # "code": 200,
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = False
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Fail (missing required 'code' & 'message' keys)
TEST = {
    "response_id": 1,
    # "code": 200,
    # "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = False
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Fail ('code' key is not type int)
TEST = {
    "response_id": 1,
    "code": "200",
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = False
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Fail (code is predefined JSON-RPC error, but message doesn't match)
TEST = {
    "response_id": 1,
    "code": -32700,
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = False
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# Fail (code is in JSON-RPC reserved range)
TEST = {
    "response_id": 1,
    "code": -32000,
    "message": "Success",
    "data": [
        "spam", "eggs", "foo", "bar"
    ]
}
SHOULD_PASS = False
VERIFY_CREATE_ERROR.append((TEST, SHOULD_PASS))

# ---------------------------------------
# Result creation
# ---------------------------------------

# Pass
TEST = {
    "response_id": 13,
    "result": "Success! It's working!"
}
SHOULD_PASS = True
VERIFY_CREATE_RESULT.append((TEST, SHOULD_PASS))

# Pass
TEST = {
    "response_id": 13,
    "result": {
        "sucess": True,
        "message": "Success! It's working!"
    }
}
SHOULD_PASS = True
VERIFY_CREATE_RESULT.append((TEST, SHOULD_PASS))

# Fail (id is not type int)
TEST = {
    "response_id": "foo bar",
    "result": "Success! It's working!"
}
SHOULD_PASS = False
VERIFY_CREATE_RESULT.append((TEST, SHOULD_PASS))

# Fail (result isn't type dict or str)
TEST = {
    "response_id": 13,
    "result": b"Success! It's working!"
}
SHOULD_PASS = False
VERIFY_CREATE_RESULT.append((TEST, SHOULD_PASS))
# ---------------------------------------
# Run the TESTs
# ---------------------------------------


for TEST in VERIFY_CREATE_REQUEST:
    error = None
    try:
        json_rpc.JSONRPCRequest(**TEST[0])
        success = True
    except (JSONRPCException, TypeError) as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, TEST[1], "REQUEST")

for TEST in VERIFY_CREATE_ERROR:
    error = None
    try:
        json_rpc.JSONRPCError(**TEST[0])
        success = True
    except (JSONRPCException, TypeError) as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, TEST[1], "ERROR")

for TEST in VERIFY_CREATE_RESULT:
    error = None
    try:
        json_rpc.JSONRPCResult(**TEST[0])
        success = True
    except (JSONRPCException, TypeError) as exception:
        success = False
        error = exception
    finally:
        print_results(success, error, TEST[1], "RESULT")

# Will return JSON-RPC Error packet for code -32700
print(json_rpc.generate_error_packet(-32700))
# Will return JSON-RPC Error packet for "Invalid Request"
print(json_rpc.generate_error_packet("Invalid Request"))
