algolib
=======
This branch of the library implements the Bag of Words technique as described in section 7.2 of [Programming Computer Vision with Python](http://programmingcomputervision.com/downloads/ProgrammingComputerVision_CCdraft.pdf). 

Spatial information is currently represented by splitting the image up into 16 equal parts, i.e. a level 2 decomposition in terms of the [Spatial Pyramid Matching](http://www.cs.unc.edu/~lazebnik/publications/pyramid_chapter.pdf) method, and projecting the SIFT descriptors present in that location onto the vocabulary.

The color histogram implementation is taken almost verbatim from [The complete guide to building an image search engine with Python and OpenCV](http://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/) with the chi-squared distance rewritten using scipy so linear search becomes feasible.

Querying is done by computing the color histogram and projecting the BoW vocabulary onto the input image.

Ranking is done by sorting an array of tuples, the first element representing the [Jaccard Distance](https://www.cs.utah.edu/~jeffp/teaching/cs5955/L4-Jaccard+Shingle.pdf) between the BoW histogram of the input image and all the images in the database and the second element representing the chi-squared distance between the color histograms.

####Sample runs:

Here are some sample runs on a dataset of 610 images, a significant portion of which are natural outdoor scenes.

![figure_1](http://i.imgur.com/n3VJPA1.png)
https://gist.github.com/Transfusion/5ae12b05ad9b5f797507

![figure_2](http://i.imgur.com/K6tNOQ2.png)
https://gist.github.com/Transfusion/494d5d38b4f68cd9f5a0

![figure_3](http://i.imgur.com/8I9BPfS.png)
https://gist.github.com/Transfusion/e2ab5d699dda20b87d58

![figure_4](http://i.imgur.com/nYbZ86I.png)
https://gist.github.com/Transfusion/32598be2c005dc3764f8
(Note how high dimensional features are completely unsuitable for sketched images; chances are the user will remember the color more accurately than the structure of the scene they have in mind!)

Script used to generate the above demos:
https://gist.github.com/Transfusion/52129142a9e8e3e3963f

##Usage:##
```
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
>>> import algolib
>>> algolib.db_manager_flat_file.init_db('db.pkl')
>>> pop = algolib.db_populator('db.pkl')
>>> pop.add_dir('/home/transfusion/InstaSketch_Algo/image_repo', recursive=True, overwrite=True)

>>> query = algolib.query_db('db.pkl')
>>> results = query.query_image('/home/transfusion/InstaSketch_Algo/image_repo/cdn/00078.JPEG', 16)

>>> a.query_image('/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image32.jpg', 10)
[('/home/transfusion/InstaSketch_Algo/image_repo/cdn/00388.JPEG', 0.99628942486085348, 12.56696605682373), ('/home/transfusion/InstaSketch_Algo/image_repo/cdn/00390.JPEG', 0.95713107996702396, 14.383894920349121), ('/home/transfusion/InstaSketch_Algo/image_repo/cdn/00180.JPEG', 0.91382904794996522, 15.544892311096191), ...]

```
