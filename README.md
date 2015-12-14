algolib
=======
This branch of the library solely implements [Visual guided navigation for image retrieval](http://ima.ac.uk/papers/qiu2007.pdf).

##Usage:##
```
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
>>> import algolib
>>> algolib.create_db("image_db.db", ["/home/transfusion/InstaSketch_Algo/image_repo/arborgreens"])
...

>>> a = algolib.query_db("image_db.db")

>>> a.query_image('/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image32.jpg', 10)
['/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image08.jpg', '/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image03.jpg', '/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image06.jpg', '/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image14.jpg', '/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image32.jpg', '/home/transfusion/InstaSketch_Algo/image_repo/arborgreens/Image07.jpg']


```
