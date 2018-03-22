"""
Gene Set Enrichment Analysis using gseapy
"""
import gseapy
import logging


logger = logging.getLogger(__name__)


def gsea(weights, outdir, cutoff=0.1, threshold=0.95,
         gene_sets='GO_Biological_Process_2017'):
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
    @params gene_sets a library name in
                      http://amp.pharm.mssm.edu/Enrichr/#stats
    @return pd.DataFrame
    """
    nor_weights = weights / weights.sum()
    genes = nor_weights.sort_values(
        ascending=False)[nor_weights.cumsum() < threshold].index.tolist()
    logger.info('start GSEA...')
    enr = gseapy.enrichr(
        gene_list=genes,
        gene_sets=gene_sets,
        outdir=outdir,
        cutoff=cutoff
    )
    return enr
