import spotipy
import networkx as nx
import matplotlib.pyplot as plt


from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f6f2ad1a3118471691471fa533eff1f4", client_secret="40d8cd756cb4474dbab23bcc945528e0"))

def featGenerator(artist_id, artist_name):
    artists = []
    done = []
    # nodo di partenza
    artists.append((artist_id, artist_name))
    for i in range(5):
        artist = artists.pop(0)
        done.append(artist)
        print(artist[1] + "\n")
        album_ids = []
        song_ids = []
        featurings = []
        # per ottenere lista id album per un artista
        results = spotify.artist_albums(artist[0], album_type='album')
        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])
        for album in albums:
            album_ids.append(album['id'])
        # per ottenere lista canzoni in un album
        for j in range(len(album_ids)):
            results = spotify.album_tracks(album_ids[j])
            tracks = results['items']
            while results['next']:
                results = spotify.next(results)
                tracks.extend(results['items'])
            for track in tracks:
                song_ids.append(track['id'])
        # per ottenere featurings
        for j in range(len(song_ids)):
            results = spotify.track(song_ids[j])
            feat = results['artists']
            for k in range(len(feat)):
                if ((feat[k]['id'], feat[k]['name']) not in featurings and feat[k]['id'] != artist[0]):
                    featurings.append((feat[k]['id'], feat[k]['name']))
                # se l'artista x non è già stato processato o se sarà processato prossimamente allora...
                if ((feat[k]['id'], feat[k]['name']) not in done and (feat[k]['id'], feat[k]['name']) not in artists):
                    artists.append((feat[k]['id'], feat[k]['name']))
        # stampare su file di testo
        f = open("/Users/nicolafarronato/Desktop/prova/network.txt", "a")
        for j in range(len(featurings)):
            if (featurings[j][0] != artist[0]):
                f.write(artist[0] + " " + featurings[j][0] + "\n")


def buildNetwork(path):
    g = nx.read_edgelist(path, nodetype=str, create_using=nx.Graph())
    #print(g.edges(data=True))
    nx.draw(g,with_labels=False)
    plt.show()

def computeScore(path):
    g = nx.read_edgelist(path, nodetype=str, create_using=nx.Graph())
    #print(nx.closeness_centrality(g))
    print(nx.closeness_centrality(g))
    


    





def main():
    #featGenerator("2YZyLoL8N0Wb9xBt1NhZWg", "Kendrick Lamar")
    #buildNetwork("/Users/nicolafarronato/Desktop/prova/network.txt")
    computeScore("/Users/nicolafarronato/Desktop/prova/network.txt")
    

if __name__ == "__main__":
    main()