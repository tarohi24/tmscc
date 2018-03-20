=======================================
Topic Models for Single Cell Clustering
=======================================


.. image:: https://img.shields.io/pypi/v/tmscc.svg
        :target: https://pypi.python.org/pypi/tmscc

.. image:: https://img.shields.io/travis/tarohi24/tmscc.svg
        :target: https://travis-ci.org/tarohi24/tmscc

.. image:: https://readthedocs.org/projects/tmscc/badge/?version=latest
        :target: https://tmscc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A package for reducing dimension of gene expression profiles and doing clustering them.

Installation
-------
.. code-block:: console

   $ pip install tmscc

for more information, see https://tmscc.readthedocs.io/en/latest/installation.html.

Example
-------
.. code-block:: python

   from tmscc import tm, datasets
   from sklearn.cluster import KMeans

   # load sample data
   profile, labels = datasets.load_klein()
   lda = tm.LDA(
       n_topics=4,
       profile=profile,
       outdir='~/tmp',
   )
   # LDA's estimation (This takes some time.)
   lda.estimate()
   # lda's theta can be used for clustering, such as k-means
   kmeans = KMeans(n_clusters=10).fit_predict(lda.theta)


* Free software: MIT license
* Documentation: https://tmscc.readthedocs.io.


Features
--------

* TODO


Requirements
-------

* Python >= 3.5
* Java >= 1.8

Credits
-------

* This package owes what this is to `Mallet`_. Thank you for the wonderful toolkit!
  
.. _Mallet: http://mallet.cs.umass.edu/
