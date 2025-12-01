from youtubesearchpython import VideosSearch

def get_youtube_id(query):
    try:
        search = VideosSearch(query, limit=1).result()
        return search['result'][0]['id']
    except:
        return None