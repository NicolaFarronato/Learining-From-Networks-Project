def computePopularity(artist_id):
    # the popularity score is an integer
    return spotify.artist(artist_id)['popularity']