import numpy as np
import pandas as pd
import tempfile
import unittest

from tmscc.sampler import GibbsSampler
from tmscc.tm import LDA
from tmscc import datasets


class TestLDA(unittest.TestCase):
    def setUp(self):
        self.sampler = GibbsSampler(
            n_iter=100
        )
        self.testdir = tempfile.TemporaryDirectory()

    def test_estimate_with_valid_data(self):
        profile = pd.DataFrame(
            np.arange(200).reshape([5, 40])
        )  # gene expression profile (genes*cells matrix)
        profile.index = ['CHEK2', 'MSH2', 'PTEN', 'TSC1', 'HER2']

        lda = LDA(
            n_topics=2,
            profile=profile,
            outdir=self.testdir.name,
        )
        lda.estimate()

    def test_estimate_klein(self):
        profile, _ = datasets.load_klein()
        lda = LDA(
            n_topics=4,
            profile=profile,
            outdir=self.testdir.name,
        )
        lda.estimate()

