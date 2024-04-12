from pathlib import Path
import time

found = False
p = Path("/usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so")
for i in range(100):
    if p.stat().st_size >  0:
       found = True
       break
    time.sleep(1)
print(f"{found=}")



