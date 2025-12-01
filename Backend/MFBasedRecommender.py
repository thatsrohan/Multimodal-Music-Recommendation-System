#%%
import scipy.sparse as sparse
import implicit
import pandas as pd
from ChunkSampler import load_triplets_in_chunks

# Load chunk-sampled dataframe
df = load_triplets_in_chunks(
    r"D:\Workspace\Multimodal-Music-Recommender-2nd-Iteration\datasets\train_triplets.txt"
)
print (df.head())
#%%
# ===========================
# GLOBAL LABEL ENCODING
# ===========================
# Encoding user and item IDs as categorical integer IDs
df['user_id'] = df['user_id'].astype('category')
df['song_id'] = df['song_id'].astype('category')

#%%
# ===========================
# BUILDING SPARSE MATRIX
# ===========================
R_sparse = sparse.coo_matrix(
    (df['play_count'].astype(float),
     (df['user_id'].cat.codes,
      df['song_id'].cat.codes))
)


# ===========================
# ALS MODEL
# ===========================
model = implicit.als.AlternatingLeastSquares(
    factors=50,
    regularization=0.1,
    use_gpu=False,
    calculate_training_loss=False
)

model.approximate_similar_items = True
model.approximate_recommend = True

# Training ALS
model.fit(R_sparse)

#%%
# ===========================
#AVAILABLE USERS
# ===========================
unique_users = df['user_id'].cat.codes.unique()
print("Total users:", len(unique_users))
print("First 20 user indexes:", unique_users[:20])
print("Max user index:", unique_users.max())
#%%
# ===========================
#PICKING THE FIRST VALID user_id
# ===========================

first_user = df['user_id'].cat.codes.iloc[0]
print ("First user index:", first_user)

recommended_songs = model.recommend(
    userid=first_user,
    user_items=R_sparse.tocsr()[first_user]
)
print("Songs for you:", df['song_id'].cat.categories[recommended_songs[0]])

#Load unique tracks metadata
tracks = pd.read_csv(
    r"D:\Workspace\Multimodal-Music-Recommender-2nd-Iteration\datasets\unique_tracks.txt",
    sep='<SEP>',
    header=None,
    names=['track_id', 'song_id', 'artist', 'track_name'],
    engine='python'
)
# Removing duplicate song_ids, keep first occurrence
tracks = tracks.drop_duplicates(subset='song_id', keep='first')

# Create lookup dict: song_id -> {artist, track_name}
song_map = tracks.set_index('song_id')[['artist', 'track_name']].to_dict('index')


def get_mf_recommendations():
    try:
        # Recommended song_ids (Pandas Index)
        rec_ids = df['song_id'].cat.categories[recommended_songs[0]]

        results = []

        for sid in rec_ids:
            if sid in song_map:
                artist = song_map[sid]['artist']
                track = song_map[sid]['track_name']
            else:
                artist = "Unknown Artist"
                track  = "Unknown Track"

            results.append({
                "song_id": sid,
                "artist": artist,
                "track_name": track
            })

        return results

    except Exception as e:
        print("MF Mapping Error:", e)
        return []

                    
# %%
