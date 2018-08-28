# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 23:48:48 2017

@author: Tara
"""
'''
Spotify need authentication even for giving access to information rather than users data
which is called Client Credentials.The Client Credentials flow allows you to get an 
access token by supplying your client credentials (client ID and secret key). This flow is
used in server-to-server authentication. Only endpoints that do not access user information can be accessed.
This file generate access token.
The access token expires every one hour

'''
#import spotipy.util as util  
import spotipy.oauth2 as oauth2

    
class Token_Generator():
 

    client_id= '66525085e7ab49128bcbcbaf4dd7a642'
    client_secret= '3de44a698d5b40d196d9c43f7a76f52c'

         
    def Get_Token(self):
        credentials = oauth2.SpotifyClientCredentials(client_id=self.client_id,client_secret=self.client_secret)
        token = credentials.get_access_token()    
        return token
    
