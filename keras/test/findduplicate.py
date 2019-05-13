import os

DIR = "../data/combined"

level = []
files = []

for folder in os.listdir(DIR):
    for img in os.listdir(DIR + "/" + folder):
        if img in files:
            print(level[files.index(img)] + ":> " + folder + ":>" + img)
        else:
            files.append(img)
            level.append(folder)
