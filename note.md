## 確認できていること
- host環境では`import tensorrt` が成功している。
- guest環境でも成功している。
- Doockerfile で RUNでtensorrtを呼び出すスクリプトの実行中にエラーを生じる。
```commandline
Step 27/29 : RUN python3 -c "import tensorrt"
 ---> Running in da75f8296f27
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3.8/dist-packages/tensorrt/__init__.py", line 68, in <module>
    from .tensorrt import *
ImportError: libnvdla_compiler.so: cannot open shared object file: No such file or directory
The command '/bin/sh -c python3 -c "import tensorrt"' returned a non-zero code: 1
```


### チェック1：tensortrt.__init__.py
host環境, guest環境でtensorrt/__init__.pyは一致した。
下記のようにして確認。
```commandline
$ python3
>>> import tensorrt
>>> tensorrt.__file__
'/usr/lib/python3.8/dist-packages/tensorrt/__init__.py'
$  md5sum /usr/lib/python3.8/dist-packages/tensorrt/__init__.py
01bd2c2b3b2ad126b561382660beb1f9  /usr/lib/python3.8/dist-packages/tensorrt/__init__.py
```

### チェック２：libnvdla_compiler.so
host環境, guest環境で 以下のファイルが見つかる。
```commandline
aragai@waragai-orin:~$ sudo find / -name "libnvdla_compiler*" -print
/usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so
```




----
host environment

```
waragai@waragai-orin:/usr/lib/python3.8/dist-packages/tensorrt$ grep import __init__.py 
import ctypes
import glob
import os
import sys
import warnings
from .tensorrt import *
    import numpy as np
```

running docker build
```
Step 27/30 : RUN python3 -c "import tensorrt"
 ---> Running in 08a5724354fa
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3.8/dist-packages/tensorrt/__init__.py", line 68, in <module>
    from .tensorrt import *
ImportError: libnvdla_compiler.so: cannot open shared object file: No such file or directory
```

in guest environment

```commandline

root@waragai-orin:/# grep import /usr/lib/python3.8/dist-packages/tensorrt/__init__.py 
import ctypes
import glob
import os
import sys
import warnings
from .tensorrt import *
    import numpy as np
root@waragai-orin:/# 

```

the same md5sum __init__.py

