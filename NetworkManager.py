
from os import system
from networkx.classes.function import is_empty, nodes
from networkx.classes.graph import Graph
import spotipy
import networkx as nx
import matplotlib.pyplot as plt
import operator
import logging
import time
import sys
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
    def featGenerator(self, artist_id: str, artist_name: str, max_distance: int):
        # Init the two sets
        print('--------------------------------------------------------------' +'\n')
        print('-------------  Start Artist Featuring Generation -------------' +'\n')
        print('--------------------------------------------------------------' +'\n')
        start = time.perf_counter()
        self.Edges_list.clear()
        artists = []
        done = []
        distReached = False
        # Starting node with (artist_id,artist_name and depth=0)
        artists.append((artist_id, artist_name,0))
        while artists:  
            artist = artists.pop(0)
            if artist[2] >= max_distance:
                if not distReached:
                    print('\n'+'-----------------------------------------------------------------' +'\n')
                    print('------------  Maximum distance reached: refinement --------------' +'\n')
                    print('-----------------------------------------------------------------' +'\n')                    
                    distReached = True         
                print(artist[1]+ '('+str(artist[2])+')',end=" || ")
                done.append(artist)
                success = False
                while not success:
                    try:
                        self._featRefine(artist,done,artists)  
                        success = True
                    except :   #If we lose internet connection wait 30 seconds instead of loosing all the progresses
                        logging.warning("Spotify is not working, lets wait a minute before continue.")
                        time.sleep(60)
                    
            else:
                done.append(artist)
                print(artist[1]+'('+str(artist[2])+')',end=" || ")
                success = False
                while not success:
                    try:
                        self._featSearch(artist,done,artists)  
                        success = True 
                    except :   #If we lose internet connection wait 30 seconds instead of loosing all the progresses
                        logging.warning("Spotify is not working, lets wait a minute before continue.")
                        time.sleep(60)
                
                
        if not distReached:
            print('\n'+'-----------------------------------------------------------------' +'\n')
            print('-----------------  Maximum distance  NOT reached -----------------' +'\n')
        #Done. Print statistics and return    
        print('\n'+'----------------------------------------------------------------' +'\n')
        end = time.perf_counter()
        elapsed = end-start
        print('Statistics : ' +'\n')
        print('Total numer of nodes : '+str(len(done)) +', \n')
        for i in range(0,max_distance+1):
            print('Nodes distance '+str(i)+' : '+str(operator.countOf([x[2] for x in done],i)) +' nodes, \n')
        #print('Nodes depth '+str((max_distance+1))+' : '+ str(operator.countOf([x[2] for x in artists],max_distance+1)+1)+' nodes. \n')  
        print("Total elapsed time : %.2f" %elapsed)  
        print("Elapsed time per artist : %.2f"%(elapsed/len(done)))
        print('----------------------------------------------------------------' +'\n')
    
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
        options = {"node_size": 50, "linewidths": 0, "width": 0.1}
        nx.draw(self.Graph_network, with_labels=labels, **options)

    def getPopularityScores(self):
        if self.Edges_list == [] and self.Graph_network == []:
            logging.error(" You should have and edge list before! ")
            return
        print('--------------------------------------------------------------' +'\n')
        print('------------  Start Artist Popularity Calculation ------------' +'\n')
        print('--------------------------------------------------------------' +'\n')
        start = time.perf_counter()
        popularities = []
        n = len(self.Graph_network.nodes())
        k = 0
        for artist in self.Graph_network.nodes():
            success = False
            while not success:
                try:
                    popularities.append(self.SPOTIFY_MANAGER.artist(artist)['popularity'])
                    success = True
                except :
                    logging.warning("Spotify is not responding. Waiting 20s and trying again")
                    time.sleep(20)
            k +=1
            sys.stdout.write('\r')
            j = (k + 1) / n
            sys.stdout.write("[%-60s] %d%%" % ('='*int(60*j), 100*j))
            sys.stdout.flush()
            time.sleep(0.05)
        end = time.perf_counter()
        print("Elapsed time : %.2f"%(end-start))
        return popularities
    
    def getFollowersNumber(self):
        if self.Edges_list == [] and self.Graph_network == []:
            logging.error(" You should have and edge list before! ")
            return
        print('--------------------------------------------------------------' +'\n')
        print('------------  Start Artist Followers Calculation -------------' +'\n')
        print('--------------------------------------------------------------' +'\n')
        start = time.perf_counter()
        followers = []
        n = len(self.Graph_network.nodes())
        k = 0
        for artist in self.Graph_network.nodes():
            success = False
            while (not success):
                try:
                    followers.append((self.SPOTIFY_MANAGER.artist(artist)['followers']['total']))
                    success = True
                except :
                    logging.warning("Spotify is not responding. Waiting 20s and trying again")
                    time.sleep(20)
            k +=1
            sys.stdout.write('\r')
            j = (k + 1) / n
            sys.stdout.write("[%-60s] %d%%" % ('='*int(60*j), 100*j))
            sys.stdout.flush()
            time.sleep(0.05)
        end = time.perf_counter()
        print("Elapsed time : %.2f"%(end-start))
        return followers
        
        
        

    #Metodi privati
    def _featSearch(self, artist_struct, done_set: list, artist_set:list):
        # nodo di partenza
        artist = artist_struct
        act_dist = artist[2]
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
                if ((feat[k]['id'], feat[k]['name']) not in featurings and feat[k]['name'] != artist[1]):
                    featurings.append((feat[k]['id'], feat[k]['name']))
                # se l'artista x non è già stato processato o se sarà processato prossimamente allora...
                if ((feat[k]['name']) not in [x[1] for x in done_set] and 
                    (feat[k]['name']) not in [x[1] for x in artist_set]):
                    artist_set.append((feat[k]['id'], feat[k]['name'],act_dist+1))
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