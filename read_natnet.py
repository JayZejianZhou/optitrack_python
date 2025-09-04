import ctypes
import time
import os

# adjust to your .so path (example: build/libnatnetwrapper.so)
SO_PATH = os.path.join(os.path.dirname(__file__), 'lib', 'libnatnetwrapper.so')
SO_PATH = os.path.abspath(SO_PATH)

lib = ctypes.CDLL(SO_PATH)

# C API declarations
lib.natnet_connect.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.natnet_connect.restype = ctypes.c_int

lib.natnet_disconnect.argtypes = []
lib.natnet_disconnect.restype = None

lib.natnet_get_num_rigid_bodies.argtypes = []
lib.natnet_get_num_rigid_bodies.restype = ctypes.c_int

lib.natnet_get_rigid_body.argtypes = [
    ctypes.c_int,                      # index
    ctypes.POINTER(ctypes.c_int),      # id
    ctypes.POINTER(ctypes.c_double),   # x
    ctypes.POINTER(ctypes.c_double),   # y
    ctypes.POINTER(ctypes.c_double),   # z
    ctypes.POINTER(ctypes.c_double),   # qx
    ctypes.POINTER(ctypes.c_double),   # qy
    ctypes.POINTER(ctypes.c_double),   # qz
    ctypes.POINTER(ctypes.c_double)    # qw
]
lib.natnet_get_rigid_body.restype = ctypes.c_int

def connect(server_ip=None, local_ip=None):
    sip = server_ip.encode('utf-8') if server_ip else None
    lip = local_ip.encode('utf-8') if local_ip else None
    return lib.natnet_connect(sip, lip)

def disconnect():
    lib.natnet_disconnect()

def get_rigid_bodies():
    n = lib.natnet_get_num_rigid_bodies()
    result = []
    for i in range(n):
        cid = ctypes.c_int()
        x = ctypes.c_double(); y = ctypes.c_double(); z = ctypes.c_double()
        qx = ctypes.c_double(); qy = ctypes.c_double(); qz = ctypes.c_double(); qw = ctypes.c_double()
        ok = lib.natnet_get_rigid_body(i,
                                       ctypes.byref(cid),
                                       ctypes.byref(x), ctypes.byref(y), ctypes.byref(z),
                                       ctypes.byref(qx), ctypes.byref(qy), ctypes.byref(qz), ctypes.byref(qw))
        if ok == 0:
            result.append({
                'id': cid.value,
                'pos': (x.value, y.value, z.value),
                'quat': (qx.value, qy.value, qz.value, qw.value)
            })
    return result

if __name__ == "__main__":
    # Replace "192.168.x.y" with your Motive/NatNet server IP, or use "" to pass an empty C string.
    # rc = connect(server_ip="192.168.0.235", local_ip="192.168.0.231")
    rc = connect(None, None)
    if rc != 0:
        print("natnet_connect failed, code:", rc)
        raise SystemExit(1)
    print("connected")

    try:
        while True:
            bodies = get_rigid_bodies()
            if bodies:
                for b in bodies:
                    print("RB", b['id'], "pos", b['pos'], "quat", b['quat'])
            else:
                print("no rigid bodies")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        disconnect()
        print("disconnected")

    print("calling")
    print(lib.natnet_connect(None, None))
    print("returned")