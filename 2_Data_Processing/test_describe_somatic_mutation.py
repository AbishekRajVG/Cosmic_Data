import pandas as pd
import gzip
import tempfile
import os
import pytest
from describe_somatic_mutation import (get_df_from_tsv, 
        get_unique_icgc_mutations,
        get_unique_icgc_mutations_count_from_mutated_allele_patterns,
        get_unique_icgc_mutations_count_from_icgc_sample_id)



def test_get_df_from_tsv_file_not_found():
    file_path = 'non_existing_file.tsv.gz'
    with pytest.raises(FileNotFoundError):
        get_df_from_tsv(file_path)


def test_get_df_from_tsv_valid_case():
    file_content = "icgc_mutation_id\ttranscript_affected\ticgc_sample_id\tmutated_from_allele\tmutated_to_allele\n" \
                   "mutation1\ttranscript1\tsample1\tA\tT\n" \
                   "mutation2\ttranscript2\tsample2\tC\tG\n"
    
    with gzip.open('mock_file.tsv.gz', 'wt') as f:
        f.write(file_content)
    
    df = get_df_from_tsv('mock_file.tsv.gz')
    
    expected_columns = ['icgc_mutation_id', 'transcript_affected', 'icgc_sample_id', 'mutated_from_allele', 'mutated_to_allele']
    assert list(df.columns) == expected_columns
    assert len(df) == 2

    os.remove('mock_file.tsv.gz')


def test_get_unique_icgc_mutations():
    df = pd.DataFrame({
        'icgc_mutation_id': ['id1', 'id2'],
        'transcript_affected': ['trans1', 'trans2'],
        'icgc_sample_id': ['sample1', 'sample2'],
        'mutated_from_allele': ['A', 'T'],
        'mutated_to_allele': ['C', 'G']
    })

    result_df = get_unique_icgc_mutations(df)
    assert 'unique_icgc_mutation_id' in result_df.columns
    assert result_df.shape[0] == 2 


def test_get_unique_icgc_mutations_count_from_mutated_allele_patterns():
    df = pd.DataFrame({
        'unique_icgc_mutation_id': ['id1_trans1', 'id1_trans1', 'id2_trans2'],
        'mutated_from_allele': ['A', 'A', 'T'],
        'mutated_to_allele': ['C', 'C', 'G']
    })

    result_df = get_unique_icgc_mutations_count_from_mutated_allele_patterns(df)
    assert 'unique_icgc_mutation_id' in result_df.columns
    assert result_df.shape[0] == 2 


def test_get_unique_icgc_mutations_count_from_icgc_sample_id():
    df = pd.DataFrame({
        'unique_icgc_mutation_id': ['id1_trans1', 'id1_trans2', 'id2_trans1'],
        'icgc_sample_id': ['sample1', 'sample1', 'sample2']
    })

    result_df = get_unique_icgc_mutations_count_from_icgc_sample_id(df)
    assert 'unique_icgc_mutation_id' in result_df.columns
    assert 'icgc_sample_id' in result_df.columns
    assert result_df.shape[0] == 2


