import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'odootest'
USER = 'admin'
PASS = 'admin'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

# create a new note
args = {
    'client_id': 1,
    'design_id': 1,
    'create_uid': uid,
    'stage_id': 2,
}
#session_id = call(url, "object", "execute", DB, uid, PASS, 'tattoo.session', 'create', args)
#print("created Session: {}".format(session_id))

# READ A SESSION
try:
    session_id = call(url, "object", "execute", DB, uid, PASS, 'tattoo.session', 'read', [10])
    print("created Session: {}".format(session_id))
except Exception as e:
    print(e)

# UPDATE A SESSION
args = {
    'client_id': 2,
    'design_id': 1,
    'create_uid': uid,
}
try:
    session_id = call(url, "object", "execute", DB, uid, PASS, 'tattoo.session', 'write', [10], args)
    print("Session Updated: {}".format(session_id))
except Exception as e:
    print(e)

# DELETE A SESSION
try:
    session_id = call(url, "object", "execute", DB, uid, PASS, 'tattoo.session', 'unlink', [10])
    print("Session Deleted: {}".format(session_id))
except Exception as e:
    print(e)