import shelve
import cv2
import numpy as np


class query_db(object):
    def __init__(self, filename):
        self.idb = shelve.open(filename)

    # def query_median(rg_median, by_median, limit):
    def query_image(self,filename, limit):
        # print self.idb
        bgr_img = cv2.imread(filename)
        rg = bgr_img[:,:,2].astype(int) - bgr_img[:,:,1].astype(int)
        by = 0.5*(bgr_img[:,:,2].astype(int)+bgr_img[:,:,1].astype(int)) - bgr_img[:,:,0].astype(int)

        rg_median = np.median(rg)
        by_median = np.median(by)

        query_root = self.idb['root']
        while(len(query_root.images) > limit):
            if(query_root.is_rg):
                if (rg_median > query_root.median):
                    if not query_root.right:
                        break
                    query_root = query_root.right
                else:
                    if not query_root.left:
                        break
                    query_root = query_root.left
            else:
                if ( by_median> query_root.median):
                    if not query_root.right:
                        break
                    query_root = query_root.right
                else:
                    if not query_root.left:
                        break
                    query_root = query_root.left
        return query_root.images