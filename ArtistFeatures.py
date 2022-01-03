import csv
import numpy as np
import networkx as nx


class ArtistFeatures:
    def __init__(self,artistsIds :str):
        ArtistFeatures.id = artistsIds
        ArtistFeatures.cc = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.bc = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.clustering_coef = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.popularity = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.num_albums = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.num_tracks = ['nan' for i in range(len(artistsIds))]
    
    def add_cc(self,closeness_centrality_vals):
        del ArtistFeatures.cc[:]
        for i in ArtistFeatures.id:
            ArtistFeatures.cc.append(closeness_centrality_vals.get(i))
    def add_bc(self,betweeness_centrality_vals):
        del ArtistFeatures.bc[:]
        for i in ArtistFeatures.id:
            ArtistFeatures.bc.append(betweeness_centrality_vals.get(i))
    def add_clustering_coef(self,clustering_coeff_vals):
        del ArtistFeatures.clustering_coef[:]
        for i in ArtistFeatures.id:
            ArtistFeatures.clustering_coef.append(clustering_coeff_vals.get(i))
    def add_pv(self,popularity_vals):
        del ArtistFeatures.popularity[:]
        ArtistFeatures.popularity = popularity_vals

    def add_numAlbums(self,nums_albums):
        del ArtistFeatures.num_albums[:]
        ArtistFeatures.num_albums = nums_albums
    
    def add_numTracks(self,nums_tracks):
        del ArtistFeatures.num_tracks[:]
        ArtistFeatures.num_tracks = nums_tracks


    def create_csv(self,output_path :str):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Id','Popularity_score','Closeness_centrality','Betweeness_centrality','Clustering_Coefficient',
                             'Num_Albums','Num_Tracks'])
            for i in range(0,len(ArtistFeatures.id)-1):
               r = [ ArtistFeatures.id[i], ArtistFeatures.popularity[i], ArtistFeatures.cc[i], 
                    ArtistFeatures.bc[i], ArtistFeatures.clustering_coef[i], ArtistFeatures.num_albums[i],
                    ArtistFeatures.num_tracks[i]]
               writer.writerow(r)

            
                                


    