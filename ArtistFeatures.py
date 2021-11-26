import csv
import numpy as np
import networkx as nx


class ArtistFeatures:
    def __init__(self,artistsIds):
        ArtistFeatures.id = artistsIds
        ArtistFeatures.cc = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.bc = ['nan' for i in range(len(artistsIds))]
        ArtistFeatures.popularity = ['nan' for i in range(len(artistsIds))]
    
    def add_cc(self,closeness_centrality_vals):
        del ArtistFeatures.cc[:]
        for i in ArtistFeatures.id:
            ArtistFeatures.cc.append(closeness_centrality_vals.get(i))
    def add_bc(self,betweeness_centrality_vals):
        del ArtistFeatures.bc[:]
        for i in ArtistFeatures.id:
            ArtistFeatures.bc.append(betweeness_centrality_vals.get(i))
    def add_pv(self,popularity_vals):
        del ArtistFeatures.popularity[:]
        ArtistFeatures.cc = popularity_vals
    def create_csv(self,output_path):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Id','Closeness_centrality','Betweeness_centrality','Popularity_score'])
            for i in range(0,len(ArtistFeatures.id)-1):
               r = [ArtistFeatures.id[i],ArtistFeatures.cc[i], ArtistFeatures.bc[i], ArtistFeatures.popularity[i]]
               writer.writerow(r)

            
                                


    