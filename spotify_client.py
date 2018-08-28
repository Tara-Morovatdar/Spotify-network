# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 22:07:39 2018

@author: Tara
"""

import time
from token_generator import Token_Generator
import requests
tok= Token_Generator()        
start_token=tok.Get_Token()
elapsed_time= time.time()
#print("start time:", start_time)
def get_token():
    
    global start_token
    global elapsed_time
    #elapsed_time= int(time.time()- elapsed_time)
    if ((int(time.time()- elapsed_time) > 3000) ) :
        
        print(start_token)
        time.sleep(5)
        print("Wake up")
        t= Token_Generator()        
        start_token=t.Get_Token()
        token= start_token
        #flag=False
        elapsed_time= time.time()
        print(token)    
    else:
        token=start_token                   
    #print("elapsed time",time.time()-start_time)         
    return token


class Artist():
    def __init__(self,id, name, related, followers, popularity,genres):
        self.id = id
        self.name = name
        self.related = related
        self.followers = followers
        self.popularity = popularity
        self.genres= genres
class SpotifyClient():
    api_url = 'http://api.spotify.com/v1'
    
        
    def get_artist_by_name(self, artist_name):        
        
        params = (
                ('q', artist_name),
                ('type', 'artist'),
                ('limit', '1'),
                )
        header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+ get_token(),
        }
        
        request=requests.get('http://api.spotify.com/v1/search', headers=header, params=params)
        res_json = request.json()
        #print (res_json)  
        res_json=res_json['artists']['items'][0]
        try:
           
            artist= self.get_artist_from_json(res_json)
        except KeyError:
            print ('Could not find artist:',artist_name)
            return None
        return artist
   
    def get_artist_by_id(self, artist_id):
        
        header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+ get_token(),
        }
        
        request=requests.get('http://api.spotify.com/v1/artists/'+artist_id, headers=header)
        #print(header['Authorization'])
        res_json = request.json()
        try:
            artist = self.get_artist_from_json(res_json)
        except KeyError:
            print(res_json)            
            
            print ('Could not find artist:',  artist_id)
            time.sleep(5)               
                        
            self.get_artist_by_id(artist_id) 
            
        return artist

    def get_artist_from_json(self, rec):
        Id = rec['id']
        name = rec['name']
        followers = rec['followers']['total']
        popularity = rec['popularity']
        genres=rec['genres']
        related = self.get_related_artists(Id)
        #print(Id, name, related, followers, popularity)
        #print("processing artist:", name)
        return Artist(Id, name, related, followers, popularity,genres)
        

    def get_related_artists(self, artist_id):
        
        header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+ get_token(),
        }
        
        
        request=requests.get('http://api.spotify.com/v1/artists/'+ artist_id+'/related-artists', headers=header)
        res_json= request.json()  
        related_ids = [a['id'] for a in res_json['artists']]
        related_ids= related_ids[0:5]
        return related_ids
