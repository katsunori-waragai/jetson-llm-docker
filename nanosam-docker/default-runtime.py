from pathlib import Path
import json
import os
import inspect
import shutil

file = Path("/etc/docker/daemon.json")
d = json.loads(file.open("rt").read())
print(d)
if d.get("default-runtime", None) == "nvidia":
  exit(0)  # OK


message = f"""Be sure to add following line in {str(file)}
"default-runtime": "nvidia",
"""

print(message)
exit(1)

# if os.access(file, os.W_OK):
#   # make dated backup
#   backupname = file.dirname() / f"{file.name}_back"
#   shutil.copy(str(file), str(backupname))
#
# print(f"{file.stat().st_mode=}")
# print(f"{file.is_writable()=}")
#
# d["default-runtime"] = "nvidia"
# newfile = Path(file.name)
# newfile.open("wt").write(json.dumps(d, sort_keys=True, indent=4))
# print("generated new daemon.json")
