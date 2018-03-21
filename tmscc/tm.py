from pathlib import Path
import numpy as np
import subprocess
import sys
import tempfile

from . import conf
from .sampler import GibbsSampler


class TopicModelBase(object):
    def __init__(self, outdir, sampler='default', sampler_opts=None):
        self.outdir = Path(outdir).expanduser().resolve()
        if not self.outdir.is_dir():
            raise AssertionError(
                '{0} is not an directory.'.format(self.outdir))
        if sampler == 'default':
            if sampler_opts is not None:
                self.sampler = GibbsSampler(**sampler_opts)
            else:
                self.sampler = GibbsSampler()
        else:
            self.sampler = sampler


class LDA(TopicModelBase):
    def __init__(self, n_topics, profile, outdir, sampler='default',
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
        super(LDA, self).__init__(outdir, sampler, sampler_opts)
        self.n_topics = int(n_topics)
        self.profile = profile

        outputfile_fmt = str(self.outdir.resolve()) + '/{0}-{1}'
        self.profile_file = self.outdir.joinpath('profile.txt')

        profile.T.to_csv(
            str(self.profile_file.resolve()), sep=',',
            index=False, header=False)
        self.gene_file = self.outdir.joinpath('genes.txt')
        with open(self.gene_file, 'w') as fp:
            fp.write(','.join(self.profile.index.tolist()))

        self.theta_file = Path(
            outputfile_fmt.format(self.n_topics, 'theta.txt'))
        self.phi_file = Path(
            outputfile_fmt.format(self.n_topics, 'phi.txt'))

        self.is_trained = False
        self.theta = None
        self.phi = None
        self.labels = labels

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
            self._estimate_mallet()
        else:
            self._estimate_celltree()

    def __repr__(self):
        return '''
        LDA Model:
        n_topics: {0}
        trained: {1},
        sampler: {2}
        '''.format(self.n_topics, self.is_trained, self.sampler)
