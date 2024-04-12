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
- host環境, guest環境で 以下のファイルが見つかる。
- md5sum の値も一致した。
```commandline
orin:~$ sudo find / -name "libnvdla_compiler*" -print
/usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so
```

#### docker build の最中での上記のファイルの有無、md5sum値
- ファイルサイズが０であることが判明した。
```Dockerfile
RUN if [ -f /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File exists"; else echo "File does not exist"; fi
RUN if [ -s /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File is not empty"; else echo "File is empty"; fi
```

```commandline
Step 29/30 : RUN if [ -f /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File exists"; else echo "File does not exist"; fi
 ---> Running in 972bbcc4fd10
File exists
Removing intermediate container 972bbcc4fd10
 ---> 9438db06b516
Step 30/30 : RUN if [ -s /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File is not empty"; else echo "File is empty"; fi
 ---> Running in 214b04a3c3e4
File is empty
```

### Q: なぜそのファイルが、docker build の最中にemptyになってしまっているのか？

----
host environment

```
orin:/usr/lib/python3.8/dist-packages/tensorrt$ grep import __init__.py 
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

root@orin:/# grep import /usr/lib/python3.8/dist-packages/tensorrt/__init__.py 
import ctypes
import glob
import os
import sys
import warnings
from .tensorrt import *
    import numpy as np
root@orin:/# 

```

the same md5sum __init__.py

