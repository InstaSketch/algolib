import os
import cv2
from algolib.config import config
from algolib.descriptors.bow_descriptor import BoWDescriptor
from algolib.descriptors.color_descriptor import ColorDescriptor

__author__ = 'Bryan Kok, Dylan Wang'


class Populator(object):

    def __init__(self):
        self.bow_des = BoWDescriptor()
        self.color_des = ColorDescriptor(config["color_histogram_bins"])

    def generate_vocabulary(self, imgs, limit=None):
        return self.bow_des.compute_vocabulary(imgs, limit, config["bow_dictionary_size"])

    def bow_hist(self, img, bow_voc):
        return self.bow_des.describe(img, bow_voc)

    def color_hist(self, img):
        return self.color_des.describe(img)


def list_images(directory):
    img_types = set(config['img_types'])
    trav = os.walk(directory)
    imgs_found = []
    for i in trav:
        imgs_found += (os.path.join(i[0], x)
                       for x in (y for y in i[2] if os.path.splitext(y)[1] in img_types))
    assert len(imgs_found) > 0
    def yield_image_matrices():
        for i in imgs_found:
            img = cv2.imread(i)
            yield i, img
    imgs = yield_image_matrices()
    return imgs
