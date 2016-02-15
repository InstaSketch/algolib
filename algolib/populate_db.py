__author__ = 'Bryan Kok'

from algolib import config

from db_manager import db_manager_flat_file
import os
import cv2

from descriptors.BoW_descriptor import BoWDescriptor
from descriptors.color_descriptor import ColorDescriptor

class db_populator:
    def __init__(self, db_file):
        self.db_manager = db_manager_flat_file(db_file)
        self.BoW_des = BoWDescriptor()
        self.color_des = ColorDescriptor(config["color_histogram_bins"])

    def list_images(self, directory, recursive=False):
        img_types = set(config['img_types'])
        if recursive:
            trav = os.walk(directory)
            imgs_found = []
            for i in trav:
                imgs_found += map(lambda x: os.path.join(i[0], x), ( filter(lambda x: os.path.splitext(x)[1] in img_types, i[2]) ) )
            return imgs_found
        else:
            return map(lambda y: os.path.join(directory, y), filter(lambda x: os.path.splitext(x)[1] in img_types, os.listdir(directory)))


    def add_dir(self, directory, recursive=False, overwrite=False):
        # overwrite controls whether the means are recomputed (and thus the existing BoW histograms invalidated.)
        # files of the same path will have both histograms recomputed in any case.
        path_list = self.list_images(directory, recursive)
        assert len(path_list) > 0

        def yield_image_matrices():
            for i in path_list:
                # img = cv2.imread(i, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                img = cv2.imread(i)
                # yield i, cv2.resize(img, (300,300))
                yield i, img

        if overwrite:
            # todo: recompute existing images' histograms since we store their feature descriptors in the DB anyways
            self.db_manager.empty_db()
            img_list = yield_image_matrices()
            vocabulary = self.BoW_des.compute_vocabulary(img_list, config["BoW_dictionary_size"])
            self.db_manager.set_BoW_vocabulary(vocabulary)
            self.db_manager.commit()

        img_list = yield_image_matrices()

        for path, img in img_list:
            print path
            img_entry = self.db_manager.add_img(path)

            BoW_hist = self.BoW_des.describe(img, self.db_manager.get_BoW_vocabulary())
            img_entry.set_BoW_hist(BoW_hist)

            color_hist = self.color_des.describe(img)
            img_entry.set_color_hist(color_hist)

        self.db_manager.commit()