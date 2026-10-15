import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    quasi_identifiers = ["age", "gender", "zip3"]

    aux_counts = aux_df.groupby(quasi_identifiers).size().reset_index(name="count")
    unique_keys = aux_counts[aux_counts["count"] == 1][quasi_identifiers]

    unique_anon = anon_df.merge(
        unique_keys,
        on=quasi_identifiers,
        how="inner"
    )

    matches = unique_anon.merge(
        aux_df,
        on=quasi_identifiers,
        how="inner"
    )

    return matches[["anon_id", "name"]].rename(
        columns={"name": "matched_name"}
    )



def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(anon_df) == 0:
        return 0.0

    return len(matches_df) / len(anon_df)
        
