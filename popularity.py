import spotipy
def computePopularity(artist_id):
    # the popularity score is an integer
    return spotipy.Spotify.artist('spotify:artist:'+artist_id)['popularity']