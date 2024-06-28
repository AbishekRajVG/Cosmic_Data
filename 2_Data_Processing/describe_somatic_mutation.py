import pandas as pd
import gzip


def get_df_from_tsv(file_path: str) -> pd.DataFrame:
    # file_path = '../simple_somatic_mutation.open.BLCA-CN.tsv.gz'
    columns_to_read = ['icgc_mutation_id', 'transcript_affected', 'icgc_sample_id', 'mutated_from_allele', 'mutated_to_allele']

    try:
        with gzip.open(file_path, 'rt') as f:
            df = pd.read_csv(f, delimiter='\t', usecols=columns_to_read)
    except FileNotFoundError as fnfe:
        print(f"Error: The file {file_path} was not found.")
        raise fnfe

    return df


def get_unique_icgc_mutations(
    df: pd.DataFrame
) -> pd.DataFrame:
    """here I'm combining columns icgc_mutation_id and transcript_affected 
    to get uniqe icgc mutations"""

    df['unique_icgc_mutation_id'] = df['icgc_mutation_id'].astype(str) + \
        '_' + df['transcript_affected'].astype(str)
    
    return df[['unique_icgc_mutation_id',
               'icgc_sample_id', 
               'mutated_from_allele', 
               'mutated_to_allele']]


def get_unique_icgc_mutations_count_from_mutated_allele_patterns(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    # Group by mutated_from_allele and then by mutated_to_allele and count unique combinations of icgc_mutation_id and transcript_affected
    grouped_df = df.groupby(
        ['mutated_from_allele', 'mutated_to_allele']
        )['unique_icgc_mutation_id'].nunique().reset_index()

    # Rename the columns for clarity
    grouped_df.columns = ['mutated_from_allele', 
                          'mutated_to_allele', 
                          'unique_icgc_mutation_id']
    return grouped_df


def get_unique_icgc_mutations_count_from_icgc_sample_id(df: pd.DataFrame
                                                        ) -> pd.DataFrame:
    
    grouped_df = df.groupby('icgc_sample_id'
                            )['unique_icgc_mutation_id'].nunique().reset_index()
    grouped_df.columns = ['icgc_sample_id',
                          'unique_icgc_mutation_id']

    # find min and max
    max_unique_mutations = grouped_df.loc[grouped_df['unique_icgc_mutation_id'].idxmax()]
    min_unique_mutations = grouped_df.loc[grouped_df['unique_icgc_mutation_id'].idxmin()]
    
    result_df = pd.DataFrame([max_unique_mutations, min_unique_mutations], index=['Highest', 'Lowest'])

    return result_df

def main():
    df_from_tsv = get_df_from_tsv('../simple_somatic_mutation.open.BLCA-CN.tsv.gz')
    df_unique_icgc_mutations = get_unique_icgc_mutations(df_from_tsv)
    
    df_res1 = get_unique_icgc_mutations_count_from_mutated_allele_patterns(df_unique_icgc_mutations)
    df_res2 = get_unique_icgc_mutations_count_from_icgc_sample_id(df_unique_icgc_mutations)


    print(df_res1.to_string(index=False))
    print()
    print(df_res2.to_string(index=True))



if __name__ == "__main__":
    main()


