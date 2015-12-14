from algolib import config
from index_tree import index_tree

import shelve
import os
import cv2
import itertools
import numpy as np

def listImages(directory):
    img_types = set(config['img_types'])
    return map(lambda y: os.path.join(directory, y),
               filter(lambda x: os.path.splitext(x)[1] in img_types, os.listdir(directory)))


def create_db(filename, directory_list):
    idb = shelve.open(filename, writeback=True)

    global_histogram = [0] * 510
    total_pixels = 0
    name_to_median = {}

    tree_root = index_tree(True)

    for img in list(itertools.chain.from_iterable(
            map(lambda directory: listImages(directory), filter(lambda x: os.path.exists(x), directory_list)))):
        bgr_img = cv2.imread(img)
        rg = bgr_img[:, :, 2].astype(int) - bgr_img[:, :, 1].astype(int)
        name_to_median[img] = np.median(rg)
        tree_root.images.append(img)
        # print rg.min()
        # break
        total_pixels = total_pixels + rg.shape[0] * rg.shape[1]
        global_histogram = np.add(global_histogram, np.histogram(rg, range(-255, 256))[0])

    median_point = total_pixels/2
    histogram_index = 0

    # print global_histogram
    while median_point > 0:
        # print median_point
        median_point = median_point - global_histogram[histogram_index]
        histogram_index += 1

    histogram_index -= 255 - 1
    # print histogram_index-255-1
    # print name_to_median

    left = []
    right = []
    for key, value in name_to_median.iteritems():
        print value
        if value < histogram_index:
            left.append(key)
        else:
            right.append(key)

    tree_root.median = histogram_index

    tree_root.left = process_subtree(left, False, tree_root, 0)
    tree_root.right = process_subtree(right, False, tree_root, 0)

    idb['root'] = tree_root

    idb.close()

# returns a tree, alternates between dividing the RG or BY component at every level
def process_subtree(images, is_rg, parent, level):
    level = level + 1
    print level

    print images
    histogram = [0] * 510
    total_pixels = 0
    name_to_median = {}

    tree_root = index_tree(is_rg)

    tree_root.images = images
    tree_root.parent = parent

    if len(images) == len(parent.images):
        return None

    for img in images:
        bgr_img = cv2.imread(img)
        if is_rg:
            component = bgr_img[:,:,2].astype(int) - bgr_img[:,:,1].astype(int)
        else:
            component = 0.5*(bgr_img[:,:,2].astype(int)+bgr_img[:,:,1].astype(int)) - bgr_img[:,:,0].astype(int)

        name_to_median[img] = np.median(component)
        total_pixels = total_pixels + component.shape[0] * component.shape[1]
        histogram = np.add(histogram, np.histogram(component, range(-255, 256))[0])


    median_point = total_pixels/2
    histogram_index = 0

    # print global_histogram
    while median_point > 0:
        # print median_point
        median_point = median_point - histogram[histogram_index]
        histogram_index += 1

    # print histogram_index
    histogram_index -= 255 - 1
    tree_root.median = histogram_index

    left = []
    right = []
    for key, value in name_to_median.iteritems():
        if value < histogram_index:
            left.append(key)
        else:
            right.append(key)

    if len(left) > 1:
        tree_root.left = process_subtree(left, not is_rg, tree_root, level)

    if len(right) > 1:
        tree_root.right = process_subtree(right, not is_rg, tree_root, level)

    return tree_root