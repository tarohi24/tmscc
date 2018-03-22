from pathlib import Path
import tempfile
import unittest

from tmscc import datasets, gsea, tm


class TestGSEA(unittest.TestCase):
    
    def setUp(self):
        self.profile, self.labels = datasets.load_klein()
        self.outdir = Path(__file__).parent.joinpath('data').resolve()

    def test_topic0(self):
        lda = tm.LDA(profile=self.profile, n_topics=4, outdir=self.outdir)
        mat = lda.get_topic_gene_matrix()
        with tempfile.TemporaryDirectory() as td:
            gsea.gsea(mat[0], outdir=td)
