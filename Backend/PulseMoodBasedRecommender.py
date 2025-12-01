# %%
import cv2
from fer import FER
import pandas as pd
import random
import time

# --- Loading Spotify dataset ---
# %%
df = pd.read_csv("D:\Workspace\Multimodal-Music-Recommender-2nd-Iteration\datasets\SpotifyRecommendationData.csv")
df = df.dropna(subset=["tempo", "energy", "valence", "danceability"])

# --- Heart rate mood mapping function ---
def mood_from_hr(heart_rate):
    if heart_rate < 70:
        return "calm", (0, 90), (0, 0.5), (0, 0.6)
    elif 70 <= heart_rate < 100:
        return "balanced", (90, 120), (0, 0.7), (0, 0.8)
    else:
        return "energetic", (120, 200), (0.6, 1.0), (0, 0.8)

# --- Emotion adjustment mapping ---
emotion_adjust = {
    "happy": {"valence": 0.1, "energy": 0.1},
    "sad": {"valence": -0.2, "energy": -0.1},
    "neutral": {"valence": 0.0, "energy": 0.0},
    "angry": {"valence": 0.0, "energy": 0.2},
    "surprise": {"valence": 0.1, "energy": 0.1},
    "fear": {"valence": -0.1, "energy": 0.1},
    "disgust": {"valence": -0.2, "energy": -0.1}
}

# --- Recommend songs based on BPM + emotion ---
def recommend_songs(heart_rate, emotion, n=5):
    mood, tempo_range, energy_range, valence_range = mood_from_hr(heart_rate)
    adj = emotion_adjust.get(emotion.lower(), {"valence": 0, "energy": 0})

    filtered = df[
        (df["tempo"].between(*tempo_range)) &
        (df["energy"].between(max(0, energy_range[0]+adj["energy"]), min(1, energy_range[1]+adj["energy"]))) &
        (df["valence"].between(max(0, valence_range[0]+adj["valence"]), min(1, valence_range[1]+adj["valence"])))
    ]

    if filtered.empty:
        filtered = df.sample(n)

    filtered["tempo_diff"] = abs(filtered["tempo"] - heart_rate)
    recommended = filtered.sort_values("tempo_diff").head(n)

  # prepare list of song dictionaries for UI
    songs = recommended[["track_name", "artists", "tempo", "energy", "valence"]].to_dict(orient="records")
    return songs

# --- New: webcam + emotion detector moved into its own function ---
def detect_pulse_and_emotion():

    cap = cv2.VideoCapture(0)
    detector = FER(mtcnn=True)

    last_emotion = "neutral"
    last_heart_rate = 0
    last_recommendation = df.sample(5)[["track_name","artists","tempo","energy","valence"]]
    emotion="neutral"
    heart_rate=0
    recommended = last_recommendation.to_dict(orient="records")

    start_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.top_emotion(frame)
            if result:
                emotion, score = result
                if score is None or score < 0.5:
                    emotion = "neutral"
            else:
                emotion = "neutral"

            heart_rate = random.randint(60, 120)

            recommended = recommend_songs(heart_rate, emotion, n=10)

            cv2.putText(frame, f"Emotion: {emotion}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Emotion + Heart Rate Recommender", frame)

            key=cv2.waitKey(1)

            if time.time() - start_time > 5:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return emotion, heart_rate, recommended

  