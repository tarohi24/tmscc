from gensim.models.ldamulticore import LdaMulticore
from scipy import sparse


class TopicModelBase(object):
    """
    Topic Model Base Class
    """
    def __ini__(self):
        pass


class LDA(TopicModelBase):
    def __init__(self, n_topics, profile, sampler='default',
                 labels=None, sampler_opts=None):
        """
        Initialize instance. This method doesn't execute method.
        @params n_topics the number of topics
        @params profile gene expression profile,
                a pandas dataframe whose shape is (n_genes, n_cells)
                profile's index should be the gene names
        @params labels cluster labels
        """
        super(LDA, self).__init__()
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

    def estimate(self):
        """
        Train LDA with self.profile
        """
        lda = LdaMulticore(self.corpus,
                           # id2word=self.id2word,
                           num_topics=self.n_topics)
        self.is_trained = True
        return lda

    def __repr__(self):
        return '''
        LDA Model:
        n_topics: {0}
        trained: {1},
        '''.format(self.n_topics, self.is_trained)
