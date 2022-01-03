from networkx.classes.function import nodes
import spotipy
import networkx as nx
import matplotlib.pyplot as plt
import ArtistFeatures

from spotipy.oauth2 import SpotifyClientCredentials


class NetworkManager:

    # Pubblici
    SPOTIFY_MANAGER = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="f6f2ad1a3118471691471fa533eff1f4",
            client_secret="40d8cd756cb4474dbab23bcc945528e0"))
    Graph_network = []
    # Costruttore

    def __init__(self):
        pass
    # Metodi 

    def featGenerator(self, artist_id: str, artist_name: str, max_depth: int, outPath: str):
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
            results = NetworkManager.SPOTIFY_MANAGER.artist_albums(
                artist[0], album_type='album')
            albums = results['items']
            while results['next']:
                results = NetworkManager.SPOTIFY_MANAGER.next(results)
                albums.extend(results['items'])
            for album in albums:
                album_ids.append(album['id'])
            # per ottenere lista canzoni in un album
            for j in range(len(album_ids)):
                results = NetworkManager.SPOTIFY_MANAGER.album_tracks(
                    album_ids[j])
                tracks = results['items']
                while results['next']:
                    results = NetworkManager.SPOTIFY_MANAGER.next(results)
                    tracks.extend(results['items'])
                for track in tracks:
                    song_ids.append(track['id'])
            # per ottenere featurings
            for j in range(len(song_ids)):
                results = NetworkManager.SPOTIFY_MANAGER.track(song_ids[j])
                feat = results['artists']
                for k in range(len(feat)):
                    if ((feat[k]['id'], feat[k]['name']) not in featurings and feat[k]['id'] != artist[0]):
                        featurings.append((feat[k]['id'], feat[k]['name']))
                    # se l'artista x non è già stato processato o se sarà processato prossimamente allora...
                    if ((feat[k]['id'], feat[k]['name']) not in done and (feat[k]['id'], feat[k]['name']) not in artists):
                        artists.append((feat[k]['id'], feat[k]['name']))
            # stampare su file di testo
            f = open(outPath, "a")
            for j in range(len(featurings)):
                if (featurings[j][0] != artist[0]):
                    f.write(artist[0] + " " + featurings[j][0] + "\n")

    def _featSearch(self, artist_id: str, artist_name: str,
                    act_depth: int, done_set, artist_set):
        # nodo di partenza
        artist_set.append((artist_id, artist_name))
        artist = artist_set.pop(0)
        done_set.append(artist)
        print(artist[1] + "\n")
        album_ids = []
        song_ids = []
        featurings = []
        # per ottenere lista id album per un artista
        results = NetworkManager.SPOTIFY_MANAGER.artist_albums(
            artist[0], album_type='album')
        albums = results['items']
        while results['next']:
            results = NetworkManager.SPOTIFY_MANAGER.next(results)
            albums.extend(results['items'])
        for album in albums:
            album_ids.append(album['id'])
            # per ottenere lista canzoni in un album
        for j in range(len(album_ids)):
            results = NetworkManager.SPOTIFY_MANAGER.album_tracks(
                album_ids[j])
            tracks = results['items']
            while results['next']:
                results = NetworkManager.SPOTIFY_MANAGER.next(results)
                tracks.extend(results['items'])
            for track in tracks:
                song_ids.append(track['id'])
            # per ottenere featurings
        for j in range(len(song_ids)):
            results = NetworkManager.SPOTIFY_MANAGER.track(song_ids[j])
            feat = results['artists']
            for k in range(len(feat)):
                if ((feat[k]['id'], feat[k]['name']) not in featurings and feat[k]['id'] != artist[0]):
                    featurings.append((feat[k]['id'], feat[k]['name']))
                # se l'artista x non è già stato processato o se sarà processato prossimamente allora...
                if ((feat[k]['id'], feat[k]['name']) not in done_set and (feat[k]['id'], feat[k]['name']) not in artist_set):
                    artist_set.append((feat[k]['id'], feat[k]['name']))

    def buildNetwork(self, path: str):
        NetworkManager.Graph_network = nx.read_edgelist(
            path, nodetype=str, create_using=nx.Graph())

    def plotGraph(self, labels: bool):
        nx.draw(NetworkManager.Graph_network, with_labels=labels)
