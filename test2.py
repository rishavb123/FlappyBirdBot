import os

for root, dirs, files in os.walk("./agents/"):
    print(files[len(files) - 1])