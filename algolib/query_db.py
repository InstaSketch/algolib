__author__ = 'Bryan Kok'

from algolib import config
import cv2
import numpy as np

from db_manager import db_manager_flat_file

from descriptors.BoW_descriptor import BoWDescriptor
from descriptors.color_descriptor import ColorDescriptor

from PIL import Image
import scipy


class query_db(object):
    def __init__(self, db_file):
        self.db_manager = db_manager_flat_file(db_file)
        self.BoW_des = BoWDescriptor()
        self.color_des = ColorDescriptor(config["color_histogram_bins"])
        self.distance_metrics = ['jaccard', 'cosine']


    # def chi2_distance(self, histA, histB, eps = 1e-10):
    #     # compute the chi-squared distance
    #     d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
    #         for (a, b) in zip(histA, histB)])
    #     # return the chi-squared distance
    #     return d

    def chi_square(self, h1, h2, eps=1e-10):
        result = scipy.square(h1 - h2) / (h1 + h2+eps)
        return 0.5 * scipy.sum(result)

    def query_image(self, filename, sketch=False, metric='jaccard'):
        # todo: implement other distance measures
        assert metric in self.distance_metrics
        img = cv2.imread(filename)

        BoW_hist = self.BoW_des.describe(img, self.db_manager.get_BoW_vocabulary())

        if sketch:
            avg_colors = [0,0,0]
            for i in xrange(3):
                avg_colors[i] = np.sum(np.concatenate(img[:,:,i]))/img[:,:,0].size

            avg_colors = map (int, avg_colors)
            print avg_colors
            img[np.where((img == [255,255,255]).all(axis = 2))] = avg_colors

        color_hist = self.color_des.describe(img)

        matchscores = []
        for path in self.db_manager.img_filenames():
            db_img = self.db_manager.get_img(path)
            BoW_dist = scipy.spatial.distance.jaccard(db_img.get_BoW_hist(), BoW_hist)

            # color_dist = cv2.compareHist(np.array(db_img.get_color_hist()), np.array(color_hist), cv2.cv.CV_COMP_CHISQR)
            color_dist = self.chi_square(db_img.get_color_hist(), np.array(color_hist))
            matchscores.append( (path, BoW_dist, color_dist))

        return matchscores