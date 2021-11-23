import csv
import spotipy
import networkx as nx


class ArtistFeatures:
    def __init__(self,artistsIds):
        ArtistFeatures.id = artistsIds
        ArtistFeatures.cc = []
        ArtistFeatures.bc = []
        ArtistFeatures.popularity = []
    
    def add_cc(closeness_centrality_vals):
        for i in ArtistFeatures.id:
            ArtistFeatures.cc[i] = closeness_centrality_vals
    def add_cc(betweeness_centrality_vals):
        for i in ArtistFeatures.id:
            ArtistFeatures.bc[i] = betweeness_centrality_vals
    def add_cc(popularity_vals):
        for i in ArtistFeatures.id:
            ArtistFeatures.cc[i] = popularity_vals
    def create_csv(output_path):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in ArtistFeatures.id:
                row = [ArtistFeatures.id[i], ArtistFeatures.cc[i],
                        ArtistFeatures.bc[i], ArtistFeatures.popularity[i]]
                writer.writerow(row)

            
                                


    