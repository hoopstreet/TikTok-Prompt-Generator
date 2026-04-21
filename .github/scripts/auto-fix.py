#!/usr/bin/env python3

import os
import re

def fix_requirements():
    if not os.path.exists("requirements.txt"):
        open("requirements.txt", "w").close()

    with open("requirements.txt", "r") as f:
        content = f.read()

    if "requests" not in content:
        with open("requirements.txt", "a") as f:
            f.write("\nrequests\n")
        print("✅ Added requests")

def fix_imports():
    if not os.path.exists("app.py"):
        return

    with open("app.py", "r") as f:
        code = f.read()

    if "import requests" not in code:
        code = "import requests\n" + code

    with open("app.py", "w") as f:
        f.write(code)

    print("✅ Imports fixed")

if __name__ == "__main__":
    fix_requirements()
    fix_imports()
