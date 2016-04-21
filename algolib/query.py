import cv2
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
        self.matchscores = []

    def chi_square(self, h1, h2, eps=1e-10):
        result = scipy.square(h1 - h2) / (h1 + h2 + eps)
        return 0.5 * scipy.sum(result)

    def compare(self, bow_hist, color_hist, img_data, metric):
        for img, bow, color in img_data:
            bow_dist = scipy.spatial.distance.jaccard(
                bow, bow_hist)
            color_dist = cv2.compareHist(
                color, color_hist, method=metric)
            self.matchscores.append((img, bow_dist, color_dist))

    def query_image(self, img, bow_hist, color_hist, img_data, bow_voc, metric, sketch):
        if metric not in self.distance_metrics.keys() or metric is None:
            metric = 'chisqr_alt'
        metric = self.distance_metrics[metric]
        self.matchscores = []
        if img is not None:
            bow_hist_local = self.bow_des.describe(img, bow_voc)
            color_hist_local = self.color_des.describe(img, sketch)

            self.compare(bow_hist_local, color_hist_local, img_data, metric)
        else:
            self.compare(bow_hist, color_hist, img_data, metric)
        return self.matchscores
