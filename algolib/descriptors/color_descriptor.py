import cv2
import numpy as np

__author__ = 'Bryan Kok, Dylan Wang'


class ColorDescriptor:

    def __init__(self, bins):
        # store the number of bins for the 3D histogram
        self.bins = bins

    def describe(self, image, sketch=False, threshold=100):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        if not sketch:
            image = cv2.resize(image, (300, 300))
        else:
            transparent_indices = np.where(image[:, :, 3] < threshold)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # divide the image into four rectangles/segments (top-left,
        # top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
                    (0, cX, cY, h)]

        # construct an elliptical mask representing the center of the
        # image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
            # the elliptical center from it

            if sketch:
                cornerMask = np.empty(image.shape[:2], dtype="uint8")
                cornerMask.fill(255)
                cornerMask[transparent_indices] = 0

                rectangleMask = np.zeros(image.shape[:2], dtype="uint8")
                cv2.rectangle(rectangleMask, (startX, startY),
                              (endX, endY), 255, -1)
                cornerMask[np.where(rectangleMask == 0)] = 0
                cornerMask = cv2.subtract(cornerMask, ellipMask)

            else:
                cornerMask = np.zeros(image.shape[:2], dtype="uint8")
                cv2.rectangle(cornerMask, (startX, startY),
                              (endX, endY), 255, -1)
                cornerMask = cv2.subtract(cornerMask, ellipMask)

            # extract a color histogram from the image, then update the
            # feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        # extract a color histogram from the elliptical region and
        # update the feature vector
        if sketch:
            cornerMask = np.empty(image.shape[:2], dtype="uint8")
            cornerMask.fill(255)
            cornerMask[transparent_indices] = 0
            cornerMask[np.where(ellipMask == 0)] = 0
            hist = self.histogram(image, cornerMask)
        else:
            hist = self.histogram(image, ellipMask)
        features.extend(hist)

        # return the feature vector
        return np.array(features)

    def histogram(self, image, mask):
        # extract a 3D color histogram from the masked region of the
        # image, using the supplied number of bins per channel; then
        # normalize the histogram
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 180, 0, 256, 0, 256])

        hist = np.array(cv2.normalize(hist, hist).flatten())

        # return the histogram
        return hist
