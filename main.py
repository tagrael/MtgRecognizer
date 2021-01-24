import cv2
import ContourDetector
import CameraStream
import time
import copy
import SearchEngine
import os
import pickle

# for pickle deserialization
from HashHelper import hamming

CAMERA_DIM_WIDTH = 1920
CAMERA_DIM_HEIGHT = 1080
WINDOW_NAME = "Mtg Card Recognizer"
PICKLE_HASH_LOC = os.path.join("C:\\", "Users", "Tomek", "PycharmProjects", "pythonProject", "data", "hash.pickle")
PICKLE_TREE_LOC = os.path.join("C:\\", "Users", "Tomek", "PycharmProjects", "pythonProject", "data", "tree.pickle")


def start_window(name):

    print("Loading data (VP-Tree and hashes)...")
    tree = pickle.loads(open(PICKLE_TREE_LOC, "rb").read())
    hashes = pickle.loads(open(PICKLE_HASH_LOC, "rb").read())

    cv2.namedWindow(name)
    camera_stream = CameraStream.CameraStream((CAMERA_DIM_WIDTH,CAMERA_DIM_HEIGHT), 0).start()
    time.sleep(1)  # camera warmup

    rval = True

    while rval:
        frame = camera_stream.read()
        original_image = copy.deepcopy(frame)
        pre_processed = ContourDetector.preprocess_image(frame, 1)
        cv2.imshow("preprocess", pre_processed)
        cards = ContourDetector.find_cards(pre_processed)

        if len(cards) != 0:

            cv2.drawContours(frame, cards, -1, (255, 0, 0), 2)

        cv2.imshow(name, frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            rval = False
        if key == ord('q') and len(cards) == 1:
            if len(cards) == 1:
                query_image = ContourDetector.crop_contour(original_image, cards[0])
                cv2.imshow("Query", query_image)
                search_result = SearchEngine.search(query_image, tree, hashes)
                print("Detected card: " + str(search_result[0][0] ))
                print("Sorted results: " + str(search_result))
                print("Number of results: " + str(len(search_result)))
                result_image = cv2.imread(str(search_result[0][0]))
                cv2.imshow("Result", result_image)

    camera_stream.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    start_window(WINDOW_NAME)
