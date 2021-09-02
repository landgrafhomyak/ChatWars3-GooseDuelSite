import sys
import os
import os.path
import shutil
from collections import deque
import pyhp.executor as pyhp

OUTPUT_DIR = f"./docs"
OUTPUT_DIR = os.path.abspath(OUTPUT_DIR)

INPUT_DIR = "./raw"
INPUT_DIR = os.path.abspath(INPUT_DIR)

TEMPLATE_PATH = "./template.pyhp"
TEMPLATE_PATH = os.path.abspath(TEMPLATE_PATH)

if os.path.exists(OUTPUT_DIR):
    if os.path.isdir(OUTPUT_DIR):
        print("Cleaning output directory")
        shutil.rmtree(OUTPUT_DIR)
        print("Output directory was cleaned")
    else:
        print(f"Output directory already exists and is not a dir", file=sys.stderr)
        exit(1)

os.mkdir(OUTPUT_DIR)

with open(TEMPLATE_PATH, "rt") as fin:
    TEMPLATE = fin.read()

q = deque([""])
while q:
    current_dir_relative = q.popleft()
    current_i_dir = os.path.join(INPUT_DIR, current_dir_relative)
    current_o_dir = os.path.join(OUTPUT_DIR, current_dir_relative)

    print(f"Processing '{current_dir_relative}'")
    for filename_clear in os.listdir(current_i_dir):
        filename_i = os.path.join(current_i_dir, filename_clear)
        filename_o = os.path.join(current_o_dir, filename_clear)

        if os.path.isdir(filename_i):
            q.append(os.path.join(current_dir_relative, filename_clear))
            continue
        elif os.path.splitext(filename_i)[1] != ".html":
            shutil.copyfile(filename_i, filename_o)
            print(f"'   '{filename_i}' -> '{filename_o}'")
            continue

        # filename_o = os.path.splitext(filename_o)[0] + ".html"

        with open(filename_i, "rt") as fin, open(filename_o, "wt") as fout:
            pyhp.exec_embed(TEMPLATE, fout, {"body": fin.read()})
        print(f"' # '{filename_i}' -> '{filename_o}'")

print("Site built successful")
