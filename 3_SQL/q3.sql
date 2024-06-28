-- 3.1
SELECT COUNT(ID_GENE) AS "# of Genes having id_biotype of 23" FROM cosmic.gene WHERE ID_BIOTYPE=23;

-- 3.2
SELECT ENSEMBL_GENE_ID FROM cosmic.gene WHERE GENE_SYMBOL='TTTY2';

-- 3.3
SELECT CHROMOSOME, COUNT(ID_GENE) AS "# of Genes per Chromosome" FROM cosmic.gene GROUP BY CHROMOSOME;

-- 3.4 
SELECT g.ID_GENE, g.GENE_SYMBOL, COUNT(t.ID_TRANSCRIPT) AS "# of Transcripts of GENE_SYMBOL RAI14" FROM cosmic.gene g JOIN cosmic.transcript t ON g.ID_GENE = t.ID_GENE WHERE g.GENE_SYMBOL = 'RAI14' GROUP BY g.ID_GENE, g.GENE_SYMBOL;

-- 3.5
SELECT g.ID_GENE, g.ENSEMBL_GENE_ID, t.IS_CANONICAL, t.ACCESSION as "Canonical Transcript Accession for ENSEMBL_GENE_ID" FROM cosmic.gene g JOIN cosmic.transcript t ON g.ID_GENE = t.ID_GENE AND g.ENSEMBL_GENE_ID = 'ENSG00000266960' AND t.IS_CANONICAL = 'y';

-- 3.6
SELECT t.ACCESSION AS "List of Transcript Accession" FROM cosmic.gene g JOIN cosmic.transcript t ON g.ID_GENE = t.ID_GENE AND g.GENE_SYMBOL = 'AK1' AND g.ID_BIOTYPE = '23' AND t.FLAGS = 'gencode_basic';

-- 3.8 
WITH some_gene as (Select * from cosmic.gene WHERE CHROMOSOME='10') SELECT g.CHROMOSOME, COUNT(g.ID_GENE) FROM some_gene s RIGHT OUTER JOIN cosmic.gene g ON s.ID_GENE = g.ID_GENE WHERE g.ID_BIOTYPE > 45 GROUP BY g.CHROMOSOME ORDER BY g.CHROMOSOME ;
