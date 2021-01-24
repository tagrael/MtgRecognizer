import cv2
import HashHelper
import time
from PIL import Image
import vptree

MAXIMUM_HAMMING_DISTANCE = 10


def search(query_image, tree, hashes):

    # Convert from CV2 image to PIL
    rgb_img = cv2.cvtColor(query_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(rgb_img)

    query_hash = HashHelper.compute_single_hash(im_pil)
    print("Searching...")
    start = time.time()
    query_results = sorted(tree.get_all_in_range(query_hash, MAXIMUM_HAMMING_DISTANCE))
    end = time.time()
    print("Search completed in " + str(end - start) + " seconds")

    results = []
    for (d, h) in query_results:
        results.append(hashes.get(h, []))
    return results
