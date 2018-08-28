# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 22:34:07 2018

@author: Tara
"""

from __future__ import print_function
import sys
from spotify_client import SpotifyClient
sys.path.append('../gexf')
#from gexf import Gexf, GexfImport
import networkx as nx
import numpy as np
import time
from random import randint
import json
import pandas as pd
################################
# general variables
################################
jumping_probability = 0.80
labels=['artistId','name', 'relatedArtists', 'followers', 'popularity','genres']
artist_df = pd.DataFrame.from_records([], columns=labels)
#artist_df.head()
################################
class ArtistGraph():
    def __init__(self):
        self.sc = SpotifyClient()
        self.graph_nx = nx.DiGraph() #networkx graph for storing data
        #self.gexf = Gexf("creator_name","music graph") #gexf graph format for plotting
        #self.graph_gexf = self.gexf.addGraph("directed","unweighted","time")
    
   
    def pick_next_artist(self,previous_artist):

             
        related_artist_list = previous_artist.related
        probability_pick = np.random.random()
        
        if probability_pick < jumping_probability:
            next_artist = np.random.choice(related_artist_list)
        else:
            next_artist= np.random.choice(initial_artist_list)
            
        return next_artist

    def walk_for_seed(self, seed_artist):
        global artist_df
        G = self.graph_nx #create an ampty graph       
        start_time = time.time()
        previous_artist= ag.sc.get_artist_by_id(seed_artist)
        artist_list=[] 
        i=0
                        
        while (int(time.time() - start_time) < 7500):
            try:
                #print("seed_artist")
                if previous_artist.id not in artist_list:
                #if previous_artist.id not in artist_df['artistId']:
                    G.add_node(previous_artist.id , label = previous_artist.name)
                    artist_list.append(previous_artist.id)
                    artist_df=artist_df.append([{"artistId":previous_artist.id,"name":previous_artist.name,
                            "relatedArtists":previous_artist.related,"followers":previous_artist.followers,
                                                 "popularity":previous_artist.popularity,"genres":previous_artist.genres}], ignore_index=True)
                
                    #print("previous:",previous_artist.name)
                    
                next_artist_id = self.pick_next_artist(previous_artist)
                next_artist= self.sc.get_artist_by_id(next_artist_id)
               
                if next_artist_id in previous_artist.related:
                    G.add_edge(previous_artist.id,next_artist.id , label= previous_artist.name+'-'+next_artist.name)
                previous_artist= next_artist  
                
                #break             
                       
                #print("artist in list:",len(artist_list))                        
                
                
            except ValueError:
                print("error happened!")
                #break
            i=i+1          
            if i%50 ==0:
                print(artist_df.shape)
                print("sleep")                
                time.sleep(10)
        
                        
           
        #print(artist_df.head())     
        nx.write_gexf(G, "rw.gexf")        
        with open('artists_list.txt', 'w') as f:
            for artist in artist_list:
                f.write(artist + '\n')
        
        
       
    


if __name__ == '__main__':
    ag = ArtistGraph()
    artist_list = [] #the artist that we crawl 
    with open('seed_id.txt') as f:
        initial_artist_list = f.read().splitlines()   
  
    
    r=randint(1, 70)
    start_artist = initial_artist_list[r-1]  
    
    #seed_artist = ag.sc.get_artist_by_id(start_artist)    
    
    ag.walk_for_seed(start_artist)
    artist_df.to_csv("artists_df.csv")
    print(artist_df.shape)
    print(artist_df.head())
       
        
    

    
