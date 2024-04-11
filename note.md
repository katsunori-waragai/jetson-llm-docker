host environment

waragai@waragai-orin:/usr/lib/python3.8/dist-packages/tensorrt$ grep import __init__.py 
import ctypes
import glob
import os
import sys
import warnings
from .tensorrt import *
    import numpy as np


running docker build
Step 27/30 : RUN python3 -c "import tensorrt"
 ---> Running in 08a5724354fa
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3.8/dist-packages/tensorrt/__init__.py", line 68, in <module>
    from .tensorrt import *
ImportError: libnvdla_compiler.so: cannot open shared object file: No such file or directory


in guest environment

root@waragai-orin:/# grep import /usr/lib/python3.8/dist-packages/tensorrt/__init__.py 
import ctypes
import glob
import os
import sys
import warnings
from .tensorrt import *
    import numpy as np
root@waragai-orin:/# 


the same md5sum __init__.py

