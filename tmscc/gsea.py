"""
Gene Set Enrichment Analysis using gseapy
"""
import gseapy
import logging


logger = logging.getLogger(__name__)


def gsea(weights, outdir, cutoff=0.1, threshold=0.95):
    """
    execute GSEA.
    For example, when you evaluate Topic 0 in a LDA model, only you have to
    execute
    >>> gsea(model.get_topic_gene_matrix.loc[0])

    @param weights a pd.Serias instance whose indices are gene names and
                   whose values are the weights of the genes
    @param outdir a directory where the result will stored
    @param cutoff p-value cutoff
    @param threshold a value of percentile. A set of genes whose cumsum() are
                     lower than this value are regarded as the gene set of
                     its topic.
    @return pd.DataFrame
    """
    genes = weigts.sort_values(ascending=False)[gene_list.cumsum() < threshold]
    logger.info('start GSEA...')
    enr = gseapy.enrichr(
        gene_list=genes
        gene_sets=weights.index.tolist(),
        outdir=outdir,
        cutoff=cutoff
    )
    return enr
