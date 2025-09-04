Tested on the following system
    Ubuntu 24.04.3 LTS
    NatnetSDK 4.3.0

Known problems,:
    If finding libNatNet.so fails, add the following to the code
    ctypes.CDLL("path/libNatNet.so", mode=ctypes.RTLD_GLOBAL)
