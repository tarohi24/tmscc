from gensim.models.ldamulticore import LdaMulticore
from pathlib import Path
import numpy as np
from scipy import sparse
import subprocess
import sys
import tempfile

from . import conf
from .sampler import GibbsSampler


class TopicModelBase(object):
    def __init__(self, sampler='default', sampler_opts=None):
        if sampler == 'default':
            if sampler_opts is not None:
                self.sampler = GibbsSampler(**sampler_opts)
            else:
                self.sampler = GibbsSampler()
        else:
            self.sampler = sampler


class LDA(TopicModelBase):
    def __init__(self, n_topics, profile, sampler='default',
                 labels=None, sampler_opts=None):
        """
        params:
        n_topics:
            the number of topics
        profile:
            gene expression profile,
            a pandas dataframe whose shape is (n_genes, n_cells)
            profile's index should be the gene names
        labels:
            cluster labels
        """
        super(LDA, self).__init__(sampler=sampler, sampler_opts=sampler_opts)
        self.n_topics = int(n_topics)
        self.profile = profile

        self.corpus, self.id2word = LDA._profile_to_corpus(profile)
        self.is_trained = False
        self.theta = None
        self.phi = None
        self.labels = labels

    @classmethod
    def _profile_to_corpus(cls, profile):
        id2word = dict(enumerate(profile.index))
        sp = sparse.csr_matrix(profile.values)
        corpus = [
            [(sp.indices[j], sp.data[j])
             for j in range(sp.indptr[i], sp.indptr[i+1])]
            for i in range(len(sp.indptr)-1)]
        return (corpus, id2word)
        
    @classmethod
    def _phi_to_mat(cls, phi_file, n_topics):
        mask = 2 ** (n_topics-1).bit_length() - 1
        mask_len = mask.bit_length()

        with open(phi_file, 'r') as f:
            phidata = [
                [int(i) for i in l[:-1].split(',')] for l in f.readlines()
            ]

        phi = [
            [
                (v & mask, v >> mask_len) for v in lst if v != 0
            ]
            for lst in phidata
        ]

        phi_mat = np.zeros([len(phi), n_topics])
        for i, lst in enumerate(phi):
            for topic, count in lst:
                try:
                    phi_mat[i][topic] = count
                except:
                    print(i, topic, n_topics)

        return phi_mat

    def load_theta(self):
        self.theta = np.loadtxt(self.theta_file.resolve(), delimiter=',')
        return self.theta

    def load_phi(self):
        self.phi = LDA._phi_to_mat(self.phi_file, self.n_topics)
        return self.phi

    def _estimate_gensim(self):
        lda = LdaMulticore(self.corpus,
                           # id2word=self.id2word,
                           num_topics=self.n_topics)
                           

    def _estimate_mallet(self):
        """
        the result will be stored in the outdir you specified
        """
        cmd = ['java',
               '-jar',
               str(conf.JARFILE_PATH.resolve()),
               str(self.n_topics),
               str(self.profile_file.resolve()),
               str(self.gene_file.resolve()),
               str(self.theta_file.resolve()),
               str(self.phi_file.resolve()),
               str(self.sampler.n_thread),
               str(self.sampler.n_iter),
               str(self.sampler.n_burnin)]
        
        sys.stderr.write('executing commands...')
        proc = subprocess.Popen(' '.join(cmd), shell=True)
        proc.wait()
        sys.stderr.write('loading result...')
        self.load_theta()
        self.load_phi()
        sys.stderr.write('\ndone!')

    def _estimate_celltree(self):
        # TODO
        sys.stderr.write('This sampler has not implemented yet.')
        pass

    def estimate(self):
        self.is_trained = True
        if isinstance(self.sampler, GibbsSampler):
            self._estimate_gensim()
        else:
            self._estimate_celltree()

    def __repr__(self):
        return '''
        LDA Model:
        n_topics: {0}
        trained: {1},
        sampler: {2}
        '''.format(self.n_topics, self.is_trained, self.sampler)
