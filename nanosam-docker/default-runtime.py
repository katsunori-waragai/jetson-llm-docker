from pathlib import Path
import json

"""
In case torch2trt failed in your environment,
Be sure to check "/etc/docker/daemon.json"
SEE:
    https://github.com/NVIDIA-AI-IOT/torch2trt/issues/483
"""

if __name__ == "__main__":
    file = Path("/etc/docker/daemon.json")
    d = json.loads(file.open("rt").read())
    if d.get("default-runtime", None) == "nvidia":
      exit(0)  # OK

    message = f"""Be sure to add following line in {str(file)}
    "default-runtime": "nvidia",
    """
    print(message)
    exit(1)

    # d["default-runtime"] = "nvidia"
    # newfile = Path(file.name)
    # newfile.open("wt").write(json.dumps(d, sort_keys=True, indent=4))
    # print("generated new daemon.json")
