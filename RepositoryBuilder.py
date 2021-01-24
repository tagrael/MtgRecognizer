import time
import vptree
import os
import pickle
from PIL import Image

from HashHelper import hamming, compute_single_hash

FOLDERS_TO_USE = ["ELD", "WAR", "ZNR", "M21"]

SAVE_LOCATION = os.path.join("C:\\", "Users", "Tomek", "PycharmProjects", "pythonProject", "data")
FOLDER_LOCATION = os.path.join("E:", "Card_Images")


def build_vp_tree(specific_folders, all_folders=1):

    print("Building VP tree...")
    start = time.time()
    hashes = {}

    if all_folders:
        _, specific_folders, _ = os.walk(FOLDER_LOCATION)

    for folder in specific_folders:
        print("Processing folder: " + str(folder))
        path = os.path.join(FOLDER_LOCATION, folder)
        files = os.listdir(path)
        for file in files:
            print("\tProcessing file: " + str(file))
            file_path = os.path.join(FOLDER_LOCATION, folder, file)
            image = Image.open(file_path)

            calc_hash = compute_single_hash(image)
            list_for_given_hash = hashes.get(calc_hash, [])
            list_for_given_hash.append(file_path)
            hashes[calc_hash] = list_for_given_hash

    points = list(hashes.keys())
    tree = vptree.VPTree(points, hamming)

    end = time.time()
    print("VP tree built in: " + str(end - start) + " seconds.")

    print("Serializing hashes...")
    f = open(os.path.join(SAVE_LOCATION, "hash.pickle"), "wb")
    f.write(pickle.dumps(hashes))
    f.close()

    print("Serializing VP-Tree...")
    f = open(os.path.join(SAVE_LOCATION, "tree.pickle"), "wb")
    f.write(pickle.dumps(tree))
    f.close()


if __name__ == '__main__':
    build_vp_tree(FOLDERS_TO_USE, 0)
