"""Main module."""

from abc import ABCMeta


class TopicModelBase(ABCMeta):
    def __init__(self, outdir, sampling_method='gibbs'):
        self.outdir = outdir
        self.sampling_method = sampling_method


class 
