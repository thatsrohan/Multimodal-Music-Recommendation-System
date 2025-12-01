import pandas as pd

def load_triplets_in_chunks(path, chunk_size=200000, sample_size=500000):
    """
    Efficient chunk-based loader that samples rows from huge triplets file
    without loading entire dataset in RAM.
    """

    samples = []
    rows_needed = sample_size

    for chunk in pd.read_csv(
        path,
        sep='\t',
        names=['user_id', 'song_id', 'play_count'],
        chunksize=chunk_size
    ):
        take = min(len(chunk), rows_needed)
        samples.append(chunk.sample(take))
        rows_needed -= take

        if rows_needed <= 0:
            break

    return pd.concat(samples).reset_index(drop=True)