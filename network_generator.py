from networkx.classes.function import nodes
import spotipy
import networkx as nx
import matplotlib.pyplot as plt
from ArtistFeatures import ArtistFeatures

from spotipy.oauth2 import SpotifyClientCredentials

from NetworkManager import NetworkManager


spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f6f2ad1a3118471691471fa533eff1f4", client_secret="40d8cd756cb4474dbab23bcc945528e0"))

def featGenerator(artist_id, artist_name):
    artists = []
    done = []
    # nodo di partenza
    artists.append((artist_id, artist_name))
    for i in range(250):
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
        f = open("/Users/nicolafarronato/Desktop/prova/network_dpg12.txt", "a")
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
    album = []
    num_tracks = []
    pop = []
    artists = list(g.nodes._nodes)
    for i in range (1,len(g.nodes)):
        album.append(computeNumAlbums(artists[i]))
        pop.append(computePopularity(artists[i]))
        #num_tracks.append(computeNumTracks(artists[i]))
    
    ccs = nx.closeness_centrality(g)
    bc = nx.betweenness_centrality(g)
    clustcs = nx.clustering(g)
    AF = ArtistFeatures(list(clustcs))
    AF.add_cc(ccs)
    AF.add_bc(bc)
    AF.add_clustering_coef(clustcs)
    AF.add_numAlbums(album)
    #AF.add_numTracks(num_tracks)
    artists = list(g.nodes._nodes)
    AF.add_pv(pop)
    AF.create_csv("/Users/nicolafarronato/Desktop/prova/data2k.csv")
    
    

def computePopularity(artist_id):
    # the popularity score is an integer
    return spotify.artist(artist_id)['popularity']
    

def computeNumAlbums(artist_id):
    results = spotify.artist_albums(artist_id, album_type='album')
    albums = results['items']
    album_ids = []
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    for album in albums:
        album_ids.append(album['id'])
    return len(album_ids)

def computeNumTracks(artist_id):
    results = spotify.artist_albums(artist_id)
    albums = results['items']
    album_ids = []
    song_ids = []
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    for album in albums:
        album_ids.append(album['id'])
    for j in range(len(album_ids)):
            results = spotify.album_tracks(album_ids[j])
            tracks = results['items']
            while results['next']:
                results = spotify.next(results)
                tracks.extend(results['items'])
            for track in tracks:
                song_ids.append(track['id'])
    return len(song_ids)


def main():
    NM = NetworkManager()
    #NM.featGenerator("4CuMwzDzEdlUJMEna38VQ0", "Dark Polo Gang",1)
    NM.featGenerator('0r1S7BCoaU5uGAgAWptbl9', 'Ski & Wok',0)
    NM.writeNetwork("/Users/nicolafarronato/Desktop/prova/prova.txt")

    #featGenerator("4CuMwzDzEdlUJMEna38VQ0", "Dark Polo Gang")
    # buildNetwork("/Users/nicolafarronato/Desktop/prova/network_dpg12.txt")
    #computeScore("/Users/nicolafarronato/Desktop/prova/network_dpg12.txt")
    #g = nx.read_edgelist("/Users/nicolafarronato/Desktop/prova/network_dpg12.txt", nodetype=str, create_using=nx.Graph())
    #results = spotify.artist_albums((list(g.nodes._nodes)[1],'Ski & Wok'))
    #print(g)

    

if __name__ == "__main__":
    main()