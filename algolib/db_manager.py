__author__ = 'Bryan Kok'

from algolib import config
import joblib
import abc

# todo: write docstring above every method
class db_manager(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, filename):
        return

    @abc.abstractmethod
    def empty_db(self):
        return

    @abc.abstractmethod
    # @staticmethod
    def init_db(filename):
        return

    @abc.abstractmethod
    def get_img(self, filename):
        return
    # @abc.abstractmethod
    def add_img(self, filename):
        return

    @abc.abstractmethod
    def img_filenames(self):
        return

    @abc.abstractmethod
    def commit(self):
        return


# this class is not meant to be used directly!
# todo: implement singleton pattern for this class!

class db_manager_flat_file(db_manager):
    # todo: specify db schema
    def __init__(self, filename):
        db_manager.__init__(self, filename)
        self.db_file = filename
        self.idb, self.idb_metadata = joblib.load(filename)
        # return self

    def empty_db(self):
        self.idb = {}
        self.idb_metadata = {}

    @staticmethod
    def init_db(filename):
        idb = {}
        idb_metadata = {}
        # leave metadata for later
        # self.idb_metadata['BoW_vocabulary']
        joblib.dump((idb, idb_metadata), filename, compress=config["compression_level"])

    def get_img(self, filename):
        return self.db_img(self, filename)

    def add_img(self, filename):
        self.idb[filename] = {'sift_desc':None, 'BoW_hist': None, 'color_hist': None}
        return self.db_img(self, filename)

    def img_filenames(self):
        return self.idb.keys()


    def get_BoW_vocabulary(self):
        return self.idb_metadata['BoW_voc']

    def set_BoW_vocabulary(self, cluster_centers):
        #todo: consider removing all the existing BoW histograms based on the old centers?
        self.idb_metadata['BoW_voc'] = cluster_centers

    def commit(self):
        joblib.dump((self.idb, self.idb_metadata), self.db_file, compress=config["compression_level"])

    # todo: error checking for getters and setters
    def _get_sift_descriptor(self, img_filename):
        return self.idb[img_filename]['sift_desc']
    def _set_sift_descriptor(self, img_filename, des_arr):
        self.idb[img_filename]['sift_desc'] = des_arr

    def _get_BoW_hist(self, img_filename):
        return self.idb[img_filename]['BoW_hist']
    def _set_BoW_hist(self, img_filename, BoW_hist):
        self.idb[img_filename]['BoW_hist'] = BoW_hist

    def _get_color_hist(self, img_filename):
        return self.idb[img_filename]['color_hist']
    def _set_color_hist(self, img_filename, color_hist):
        self.idb[img_filename]['color_hist'] = color_hist

    # use factory design pattern to instantiate image objects.
    class db_img(object):
        def __init__(self, db_manager, filename):
            self.filename = filename
            self.db_manager = db_manager

        def get_sift_descriptor(self):
            return self.db_manager._get_sift_descriptor(self.filename)
        def set_sift_descriptor(self, des_arr):
            self.db_manager._set_sift_descriptor(self.filename, des_arr)

        def get_BoW_hist(self):
            return self.db_manager._get_BoW_hist(self.filename)
        def set_BoW_hist(self, hist_arr):
            self.db_manager._set_BoW_hist(self.filename, hist_arr)

        def get_color_hist(self):
            return self.db_manager._get_color_hist(self.filename)
        def set_color_hist(self, hist_arr):
            self.db_manager._set_color_hist(self.filename, hist_arr)