__author__ = 'Bryan Kok'

import numpy as np
import cv2

from scipy.cluster.vq import *

# this class is not meant to be used directly
class BoWDescriptor:
    def __init__(self, algorithm='SIFT'):

        self.sift = cv2.SIFT()
        # self.trainer

    def compute_vocabulary(self, img_mat_list, dict_size):

        kp, descriptors = self.sift.detectAndCompute(img_mat_list.next()[1], None)

        # assumes the image is square!
        for path, image in img_mat_list:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (300, 300))
            img_kp, img_des = self.sift.detectAndCompute(img, None)
            descriptors = np.vstack((descriptors, img_des))

        temp, classified_points, means = cv2.kmeans(data=descriptors, K=dict_size, bestLabels=None,
	criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.05), attempts=2, flags=cv2.KMEANS_RANDOM_CENTERS )

        return means

    def describe(self, img, vocabulary):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (300, 300))

        img_kp, img_des = self.sift.detectAndCompute(img, None)
        # img_kp and img_des have the same length

        # divide the image up into 16 chunks
        current_hist = np.zeros((16, len(vocabulary)), 'float32')
        sort = {}
        # iterate over each descriptor in the keypoint to organize them into chunks

        for j in xrange(len(img_des)):
            x_chunk_size = img.shape[0]/4
            current_chunk = 4*( int(img_kp[j].pt[1])/x_chunk_size) + ( int(img_kp[j].pt[0])/x_chunk_size)

            if current_chunk not in sort:
                sort[current_chunk] = np.array( [ img_des[j] ])
            else:
                sort[current_chunk] = np.vstack( ( sort[current_chunk], img_des[j]) )

        for key in sort.keys():
            words, distance = vq(sort[key], vocabulary)

            for w in words:
                current_hist[key][w] += 1

        return np.concatenate(current_hist)