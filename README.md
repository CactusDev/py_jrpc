# json_rpc
A Python 3 module that provides packet generation and validation for the JSON-RPC 2.0 specification

## Usage:

json_rpc is a fairly simple module that provides packet generation and validation for the JSON-RPC 2.0 specification.

### Compliance checking


For example, if you wanted to check if some JSON you have is compliant with JSON-RPC, you would do something like this:

```python
import json_rpc

# Let's check a JSON packet!
to_test = {
    "jsonrpc": "2.0",
    "id": 42,
    "method": "spam:eggs",
    "params": {
        "foo": "bar"
    }
}

success, errors = json_rpc.verify_packet(to_test, json_rpc.JSONRPCTypes.REQUEST)

if success == True:
    print("Success! This is a JSON-RPC compliant packet!")
else:
    print("Something is invalid in this packet!")
    print("Errors:")
    print(errors)
```

It's that simple!

### Packet generation

json_rpc can also generate JSON-RPC compliant packets for you!

#### Result Example

```python
import json_rpc

result_data = {
    "spam": "eggs",
    "towels": 42
}

# Create the JSONRPCResult object
result = json_rpc.JSONRPCResult(result_data, response_id=2)

# You can access the generated packet via two Methods
# 1 - Via the return_packet() function
result_packet = result.return_packet()
print(result_packet)

# or 2 - via the .packet member of the object
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

This also works for generating errors!
