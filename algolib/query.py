import cv2
import numpy as np
import scipy

from algolib.config import config
from algolib.descriptors.bow_descriptor import BoWDescriptor
from algolib.descriptors.color_descriptor import ColorDescriptor

__author__ = 'Bryan Kok, Dylan Wang'


class Query(object):

    def __init__(self):
        self.bow_des = BoWDescriptor()
        self.color_des = ColorDescriptor(config['color_histogram_bins'])
        self.distance_metrics = config['distance_metrics']

    def chi_square(self, h1, h2, eps=1e-10):
        result = scipy.square(h1 - h2) / (h1 + h2 + eps)
        return 0.5 * scipy.sum(result)

    def query_image(self, img, img_data, bow_voc, sketch=False, metric='jaccard'):
        assert metric in self.distance_metrics
        bow_hist_local = self.bow_des.describe(img, bow_voc)

        if sketch:
            avg_colors = [0, 0, 0]
            for i in range(3):
                avg_colors[i] = np.sum(np.concatenate(
                    img[:, :, i])) // img[:, :, 0].size

            avg_colors = list(map(int, avg_colors))
            img[np.where((img == [255, 255, 255]).all(axis=2))] = avg_colors

        color_hist_local = self.color_des.describe(img)

        matchscores = []
        for img, bow_hist, color_hist in img_data:
            bow_dist = scipy.spatial.distance.jaccard(
                bow_hist, bow_hist_local)
            color_dist = self.chi_square(
                color_hist, np.array(color_hist_local))
            matchscores.append((img, bow_dist, color_dist))
        return matchscores
