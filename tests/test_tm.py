import numpy as np
import pandas as pd
from pathlib import Path
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

    def test_init(self):
        profile, _ = datasets.load_klein()
        

    def test_estimate_klein(self):
        profile, _ = datasets.load_klein()
        lda = LDA(
            n_topics=4,
            profile=profile,
        )
        lda.estimate()
