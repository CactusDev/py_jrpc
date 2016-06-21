# py_jrpc
A Python 3 module that provides packet generation and compliance checking for the JSON-RPC 2.0 specification

## Usage:

py_jrpc is a fairly simple module that provides packet generation and compliance checking for the JSON-RPC 2.0 specification.

## Compliance checking

For example, if you wanted to check if some JSON you have is compliant with JSON-RPC, you would do something like this:

```python
import py_jrpc

# Let's check a JSON packet!
to_test = {
    "jsonrpc": "2.0",
    "id": 42,
    "method": "spam:eggs",
    "params": {
        "foo": "bar"
    }
}

success, errors = py_jrpc.verify_packet(to_test, py_jrpc.JSONRPCTypes.REQUEST)

if success == True:
    print("Success! This is a JSON-RPC compliant packet!")
else:
    print("Something is invalid in this packet!")
    print("Errors:")
    print(errors)
```

It's that simple!

## Packet generation

py_jrpc can also generate JSON-RPC compliant packets for you!

#### Result Example

```python
import py_jrpc

result_data = {
    "spam": "eggs",
    "towels": 42
}

# Create the JSONRPCResult object
result = py_jrpc.JSONRPCResult(result_data, response_id=2)

# Let's access our newly generated packet
result_packet = result.packet
print(result_packet)

# Output
# {
#     "jsonrpc": "2.0",
#     "id": 2,
#     "result": {
#         "spam": "eggs",
#         "towels": 42
#     }
# }
```

### Error example

This also works for generating errors!

```python
import py_jrpc

error_data = {
    "foo": "bar",
    "extra": ["additional", "data"]
}

# Create the JSONRPCResult object
result = py_jrpc.JSONRPCError(
                                200,
                                "The warp drive didn't engage!",
                                data=error_data,
                                response_id=2
                                )

# Let's access our newly generated packet
result_packet = result.packet
print(result_packet)

# Output
# {
#     "jsonrpc": "2.0",
#     "id": 2,
#     "error": {
#         "code": 200,
#         "message": "foo",
#         "data": {"extra": ['additional', 'data'], 'foo': 'bar'}
#     }
# }
```

### Request example

You can also generate request packets!

```python
import py_jrpc

request_params = {
    "one_ring": [
        "is_secret",
        "is_safe"
    ]
}

# Create the JSONRPCResult object, but this time it's a notification
result = py_jrpc.JSONRPCResult("check:frodo_baggins",
                                request_params,
                                response_id=2)

# Let's access our newly generated packet
result_packet = result.packet
print(result_packet)

# Output
# {
#     "jsonrpc": "2.0",
#     "id": 2
#     "method": "check:frodo_baggins"
#     "params": {
#         "one_ring": [
#           "is_secret",
#           "is_safe"
#         ],
#     }
# }
```

### Notification example

You can also generate notification packets by simply creating a request object like we did previously, but without the `response_id` argument and with setting the `is_notif` argument to True

```python
import py_jrpc

request_params = {
    "one_ring": [
        "is_secret",
        "is_safe"
    ]
}

# Create the JSONRPCResult object, but this time it's a notification, so set is_notif to True
result = py_jrpc.JSONRPCResult("check:frodo_baggins",
                                request_params,
                                is_notif=True)

# Let's access our newly generated packet
result_packet = result.packet
print(result_packet)

# Output
# {
#     "jsonrpc": "2.0",
#     "method": "confirm:frodo_baggins"
#     "params": {
#         "one_ring": [
#           "is_secret",
#           "is_safe"
#         ],
#     }
# }
```

### Validating generated packets

You can validate the generated packets while accessing them via the `return_packet()` function

```python
request_params = {
    "Aragorn": [
        "is_king",
        "is_fighting"
    ]
}

# Create the JSONRPCResult object
result = py_jrpc.JSONRPCResult("check:Aragorn",
                                request_params,
                                response_id=2)

# Let's access our newly generated packet, but this time via .return_packet()
did_validate, packet, errors = result.return_packet()
print(did_validate)
print()
print(result_packet)
print()
print(errors)

# Output
# True
#
# {
#     "jsonrpc": "2.0",
#     "method": "check:aragorn"
#     "params": {
#       "Aragorn": [
#           "is_king",
#           "is_fighting"
#       ]
#    }
# }
#
# None
```

## Predefined error packets

There are several JSON-RPC error packets built in to the module that are easily accessible for drop in use!

```python
import py_jrpc

# Let's say you wanted an "Invalid Request" error packet
# You can do this both by the error string (case insensitive)
packet = py_jrpc.generate_error_packet("Invalid request")
# OR by the ID
packet = py_jrpc.generate_error_packet(-32600)

print(packet)
# Output:
# {
#     'error': {
#         'code': -32600
#         'message': 'Invalid Request'
#     },
#     'id': None,
#     'jsonrpc': '2.0'
#  }
```
