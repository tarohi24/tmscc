from abc import ABCMeta
from pathlib import Path
import numpy as np
import tempfile

from tmmsc import JARFILE_PATH
from sampler import GibbsSampler


class TopicModelBase(ABCMeta):
    def __init__(self, outdir, sampler='default'):
        self.outdir = Path(outdir)
        if not outdir.is_dir():
            raise AssertionError('Outdir should be an existing directory.')
        if sampler == 'default':
            self.sampler = GibbsSampler(n_iter=1000, n_burnin=100)
        else:
            self.sampler = sampler


class LDA(TopicModelBase):
    def __init__(self, n_topics, profile, gene_names,
                 outdir, sampler='default'):
        """
        params:
        n_topics:
            the number of topics
        profile:
            gene expression profile,
            a numpy array whose shape is (n_genes, n_cells)
        gene_names:
            a list of gene names(str), whose length must be same as the
            profile's column length
        """
        super(LDA, self).__init__(outdir, sampler)
        self.n_topics = int(n_topics)

        if not isinstance(profile, np.array):
            raise AssertionError('profile must be a numpy array')
        elif profile.ndim != 2:
            raise AssertionError('profile must be a 2D numpy array')
        self.profile = profile

        if len(gene_names) != profile.shape[0]:
            raise AssertionError('gene_name\'s length must be same as the'
                                 'number of rows of the profile.')

        outputfile_fmt = self.outdir.resolve() + '/{0}-{1}'
        self.theta_file = Path(
            outputfile_fmt.format(self.n_topics, 'theta.txt'))
        self.phi_file = Path(
            outputfile_fmt.format(self.n_topics, 'phi.txt'))

        self.theta = None
        self.phi = None

    def estimate(self):
        def _estimate_mallet(self):
            """
            the result will be stored in the outdir you specified
            """
            datafp = tempfile.NamedTemporaryFile()
            np.savetxt(datafp.name, self.profile.T, delimiter=',')
            genefp = tempfile.NamedTemporaryFile()
            genefp.write(','.join(self.gene_names))

            cmd = ['java',
                   '-jar',
                   JARFILE_PATH,
                   str(self.n_topics),
                   datafp.fname,
                   genefp.fname,
                   self.theta_file.resolve(),
                   self.phi_file.resolve(),
                   str(self.sampler.n_thread),
                   str(self.sampler.n_burnin)]

            procs.append(subprocess.Popen(' '.join(cmd), shell=True))
            datafp.close()
            genepf.close()

        def _estimate_celltree(self):
            # TODO
            pass

        if isinstance(self.sampler, GibbsSampler):
            _estimate_mallet()
        else:
            _estimate_celltree()

    def load_params(self):
        """
        load results of estimate()
        parameters will be in self.theta (cells*topics matrix) and
        self.phi (words*topics matrix).
        """
        if not self.theta_file.exists():
            raise AssertionError('execute estimate() before calling this'
                                 'method.')
        else:
            self.theta = np.loadtxt(self.theta_file.resolve(), delimiter=',')
        
        if not self.phi_file.exists():
            raise AssertionError('execute estimate() before calling this'
                                 'method.')
        else:
            self.phi = np.loadtxt(self.phi_file.resolve(), delimiter=',')

        return (self.theta, self.phi)
