#!/usr/bin/python
DOCUMENTATION = '''
---
module: logentries
version_added: "2.0"
short_description: Send a message to logentries.
description:
   - Send a message to logentries
options:
  token:
    description:
      - Log token.
    required: true
  msg:
    description:
      - The message body.
    required: true
    default: null
  api:
    description:
      - API endpoint
    required: false
    default: data.logentries.com
  port:
    description:
      - API endpoint port
    required: false
    default: 10000
requirements: [ ]
author: "Jimmy Tang <jimmy.tang@logentries.com>"
'''

EXAMPLES = '''
- logentries:
    token=00000000-0000-0000-0000-000000000000
    msg="{{ ansible_hostname }}"
'''


def send_msg(module, token, msg, api, port):
    import socket

    message = "{} {}\n".format(token, msg)

    api_ip = socket.gethostbyname(api)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((api_ip, port))
    try:
        s.send(message)
    except:
        module.fail_json(msg="failed to send message, msg=%s" % str(message))
    s.close()

def main():
    module = AnsibleModule(
            argument_spec=dict(
                token=dict(required=True),
                msg=dict(required=True),
                api=dict(default="data.logentries.com"),
                port=dict(default=10000)
                ),
            supports_check_mode=False
            )

    token = module.params["token"]
    msg = module.params["msg"]
    api = module.params["api"]
    port = module.params["port"]

    try:
        send_msg(module, token, msg, api, port)
    except Exception, e:
        module.fail_json(msg="unable to send msg: %s" % e)

    changed = True
    module.exit_json(changed=changed, msg=msg)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

main()
