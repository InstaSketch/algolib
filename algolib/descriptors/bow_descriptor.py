import cv2
import numpy as np
from scipy.cluster.vq import vq

__author__ = 'Bryan Kok, Dylan Wang'


class BoWDescriptor(object):

    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()
        # self.trainer

    def compute_vocabulary(self, img_mat_list, limit, dict_size):
        _, descriptors = self.sift.detectAndCompute(
            next(img_mat_list)[1], None)
        # assumes the image is square!
        count = 0
        for _, image in img_mat_list:
            if count == limit:
                break
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (300, 300))
            _, img_des = self.sift.detectAndCompute(img, None)
            descriptors = np.vstack((descriptors, img_des))
            count += 1

        _, _, means = cv2.kmeans(data=descriptors, K=dict_size, bestLabels=None,
                                 criteria=(cv2.TERM_CRITERIA_EPS +
                                           cv2.TERM_CRITERIA_MAX_ITER, 10, 0.05),
                                 attempts=2, flags=cv2.KMEANS_RANDOM_CENTERS)
        return means

    def describe(self, img, vocabulary):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (300, 300))

        img_kp, img_des = self.sift.detectAndCompute(img, None)
        # img_kp and img_des have the same length

        # divide the image up into 16 chunks
        current_hist = np.zeros((16, len(vocabulary)), 'float32')
        sort = {}
        # iterate over each descriptor in the keypoint to organize them into
        # chunks
        if img_kp:
            for j in range(len(img_des)):
                x_chunk_size = img.shape[0] // 4
                current_chunk = 4 * (int(img_kp[j].pt[1]) // x_chunk_size) + \
                    (int(img_kp[j].pt[0]) // x_chunk_size)

                if current_chunk not in sort:
                    sort[current_chunk] = np.array([img_des[j]])
                else:
                    sort[current_chunk] = np.vstack(
                        (sort[current_chunk], img_des[j]))

            for key in sort.keys():
                words, _ = vq(sort[key], vocabulary)

                for w in words:
                    current_hist[key][w] += 1

        return np.concatenate(current_hist)
