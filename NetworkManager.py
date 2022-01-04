from networkx.classes.function import is_empty, nodes
from networkx.classes.graph import Graph
import spotipy
import networkx as nx
import matplotlib.pyplot as plt
import operator
import logging

from spotipy.oauth2 import SpotifyClientCredentials


class NetworkManager:
    # Pubblici
    SPOTIFY_MANAGER = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="f6f2ad1a3118471691471fa533eff1f4",
            client_secret="40d8cd756cb4474dbab23bcc945528e0"))
    Graph_network = []
    Edges_list = []
    
    # Costruttore
    def __init__(self):
        pass
    
    # Metodi Pubblici
    def featGenerator(self, artist_id: str, artist_name: str, max_depth: int):
        # Init the two sets
        print('--------------------------------------------------------------' +'\n')
        print('-------------  Start Artist Featuring Generation -------------' +'\n')
        self.Edges_list.clear()
        artists = []
        done = []
        depthReached = False
        # Starting node with (artist_id,artist_name and depth=0)
        artists.append((artist_id, artist_name,0))
        while artists:  
            artist = artists.pop(0)
            if artist[2] >= max_depth:
                if not depthReached:
                    print('\n'+'--------------------------------------------------------------' +'\n')
                    print('------------  Maximum depth reached: refinement --------------' +'\n')
                    print('--------------------------------------------------------------' +'\n')                    
                    depthReached = True         
                print(artist[1]+ '('+str(artist[2])+')',end=" || ")
                done.append(artist)
                self._featRefine(artist,done,artists)  
            else:
                done.append(artist)
                print(artist[1]+'('+str(artist[2])+')',end=" || ")
                self._featSearch(artist,done,artists)   
        if not depthReached:
            print('\n'+'--------------------------------------------------------------' +'\n')
            print('-----------------  Maximum depth NOT reached -----------------' +'\n')
        #Done. Print statistics and return    
        print('\n'+'-------------------------------------------------------------' +'\n')
        print('Statistics : ' +'\n')
        print('Total numer of nodes : '+str(len(done)) +', \n')
        for i in range(0,max_depth+1):
            print('Nodes depth '+str(i)+' : '+str(operator.countOf([x[2] for x in done],i)) +' nodes, \n')
        #print('Nodes depth '+str((max_depth+1))+' : '+ str(operator.countOf([x[2] for x in artists],max_depth+1)+1)+' nodes. \n')    
        print('-------------------------------------------------------------' +'\n')
    def writeNetwork(self, path : str):
        print('---------------------------------------------------------' +'\n')
        print('---------------  Write Edges List to txt ----------------' +'\n')
        f = open(path,'a')
        for r in self.Edges_list:
            f.write(' '.join(str(s) for s in r) + '\n')  
        print('Successfully Written to '+ path +'\n')
        print('---------------------------------------------------------' +'\n')
    
    def buildNetworkFromTxt(self, path: str):
        self.Graph_network.clear()
        self.Graph_network = nx.read_edgelist(
            path, nodetype=str, create_using=nx.Graph())

    def buildGraphNetwork(self):
        self.Graph_network.clear()
        self.Graph_network = nx.Graph()
        self.Graph_network.add_edges_from(self.Edges_list)

    def plotGraph(self, labels: bool):
        if not self.Graph_network:
            try:
                self.getNetwork()
            except:
                logging.error("Need a graph to use this method!!")
                return
        nx.draw(self.Graph_network, with_labels=labels)

    #Metodi privati
    def _featSearch(self, artist_struct, done_set: list, artist_set:list):
        # nodo di partenza
        artist = artist_struct
        act_depth = artist[2]
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
            # per ottenere lista canzoni in un albumm
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
                if ((feat[k]['id'], feat[k]['name']) not in [x[0:2] for x in done_set] and 
                    (feat[k]['id'], feat[k]['name']) not in [x[0:2] for x in artist_set]):
                    artist_set.append((feat[k]['id'], feat[k]['name'],act_depth+1))
        # Save the edge list for the artist processed with the featuring artists
        for j in range(len(featurings)):
            if (featurings[j][0] != artist[0]):
                self.Edges_list.append((artist[0],featurings[j][0]))
    def _featRefine(self, artist_struct, done_set: list, artist_set:list):
        # nodo di partenza
        artist = artist_struct
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
            # per ottenere lista canzoni in un albumm
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
                if (((feat[k]['id'], feat[k]['name']) in [x[0:2] for x in done_set] or 
                    (feat[k]['id'], feat[k]['name']) in [x[0:2] for x in artist_set]) and 
                    (feat[k]['id'] != artist[0])):
                    featurings.append((feat[k]['id'], feat[k]['name']))
        # Save the edge list for the artist processed with the featuring artists
        for j in range(len(featurings)):
            if (featurings[j][0] != artist[0]):
                self.Edges_list.append((artist[0],featurings[j][0]))