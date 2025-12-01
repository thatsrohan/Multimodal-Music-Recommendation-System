# 🎧 Multimodal Music Recommender System

A smart music recommendation system that adapts to the user's real-time **mood** and **context**.  
It combines emotional signals, environmental factors, and listening behavior to recommend songs that match how the user feels.

---

## 🚀 Key Features
- 🎭 Facial Emotion + Pulse-Based Mood Detection  
- 🌦️ Weather Context Adaptation (Public IP → Geo → Weather API)  
- 🎼 Lyrics Sentiment & Theme Analysis  
- 🎧 MF-Based Personal Preference Learning  
- 🖥️ Fully Integrated Using NiceGUI (No separate API layer)  
- ⚡ Real-time dynamic recommendations

---

## 🧠 System Modules

| Module | Purpose |
|--------|---------|
| Mood-Based Recommender | Uses facial emotion + pulse inputs to detect mood |
| Weather-Based Recommender | Maps real-time weather → music mood |
| Lyric-Based Recommender | Sentiment + semantic similarity of lyrics |
| MF-Based Recommender | Learns long-term user preferences |

---

## 🛠️ Tech Stack
- Python  
- NiceGUI (Frontend + backend integration)
- Machine Learning (Matrix Factorization)
- Weather Data API (based on IP geolocation)
- Pandas, Requests, Implicit library

---
📂 Required Datasets (Download Before Running)

To enable recommendations, please download the following datasets manually:

Purpose                               	Dataset Name	                           Source Link
MF-Based Recommendations	Million Song Dataset – train_triplets.txt	https://labrosa.ee.columbia.edu/millionsong/

MF-Based Recommendations	Million Song Dataset – unique_tracks.txt	https://labrosa.ee.columbia.edu/millionsong/

Weather-based & Pulse-based Spotify Recommendation Dataset (2020)	https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-2020-160k-tracks

Lyrics Similarity       	Millsong Lyrics Dataset                  	https://labrosa.ee.columbia.edu/millionsong/

📌 Place downloaded datasets in the folders referenced inside the code (e.g., Datasets/ folder in backend).
