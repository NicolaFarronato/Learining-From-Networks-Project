import csv
import numpy as np
import networkx as nx


class ArtistFeatures:
    #Costruttore
    def __init__(self,inputGraph):
        ArtistFeatures.artistsIds = list(inputGraph.nodes())
        ArtistFeatures._graph = inputGraph
        ArtistFeatures.dictFeatures = {"Artists_Id":self.artistsIds}

    
    #Metodi pubblici   
    def add_Feature(self, feature_name :str , feature_value):
        if len(feature_value) == len(self.artistsIds):
            self.dictFeatures[feature_name] = feature_value
        else:
            print("The feature length is "+len(feature_value)+", but you need "+len(self.artistsIds)+" elements.")

    def create_csv(self,output_path :str):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(self.dictFeatures.keys()))
            valsFeat = list(self.dictFeatures.values())
            for i in range (len(self.artistsIds)):
               writer.writerow([item[i] for item in valsFeat])