import csv
import FunctionsSpotify as FS
from FunctionsPython import CleanString
from pandas import DataFrame
from sys import stdout as Stdout
import time
ClassicFile = "Project1994/ClassicMashupAdjacency.csv"
searchsource = "Classic"
infoList = []
WriteFilePath = "Project1994/SpotifyResultsWriteFile.csv"
consoleprint = Stdout
#
'''search terms from readfile:'''
# with open(ClassicFile,'r') as openReadFile:
#     for row in openReadFile:
#         reader = csv.reader(openReadFile)
#         StartSongs = [row[0] + " " + row[1] for row in reader]
#         MatchSongs = [row[2] + " " + row[3] for row in reader]
#     AllSongs = list(set(StartSongs)) + list(set(MatchSongs))
# openReadFile.close()

'''search terms from handcrafted list:'''
#AllSongs = ["Bootylicious Destiny's Child"]
AllSongs = ["L'via L'Viaquez The Mars Volta"]

for term in AllSongs:
    # try:
    results = FS.SearchSpotify(term,"track")
    trackname = results["tracks"]["items"][0]["name"]
    artistname = results["tracks"]["items"][0]["album"]["artists"][0]["name"]
    popularity = results["tracks"]["items"][0]["popularity"]
    albumname = results["tracks"]["items"][0]["album"]["name"]
    albumid = results["tracks"]["items"][0]["album"]["id"]    
    artistid = results["tracks"]["items"][0]["album"]["artists"][0]["id"]
    trackid = results["tracks"]["items"][0]["id"]
    cleanterm = CleanString(term)
    cleanresult = CleanString(trackname + " " + artistname)
    # except:
    #     pass
    # if cleanterm == cleanresult:
    #     PromptResponse = "Y" 
    # else:
    print("You searched for: " + cleanterm)
    print("You got:          " + cleanresult)
    PromptText = "You want it?"
    PromptResponse = input(PromptText)
    if CleanString(PromptResponse) == "Y":
        features = FS.GetTrackAudioFeatures(trackid)
        infoList.append([
            trackid
            ,trackname
            ,popularity
            ,albumid
            ,albumname
            ,artistid
            ,artistname
            ,searchsource
            #features['id'],
            ,features['acousticness']
            ,features['analysis_url']     
            ,features['danceability']    
            ,features['duration_ms']     
            ,features['energy']      
            ,features['instrumentalness']
            ,features['key']
            ,features['liveness']   
            ,features['loudness']
            ,features['mode']
            ,features['speechiness']    
            ,features['tempo']      
            ,features['time_signature']
            ,features['track_href']
            ,features["type"]
            ,features["uri"]
            ,features['valence']    
            ])
    time.sleep(.5)    # Pause .5 seconds
FeaturesDf = DataFrame(infoList)
FeaturesDf = FeaturesDf.set_index([0])
with open(WriteFilePath,'a') as openWriteFile:
    FeaturesDf.to_csv(openWriteFile, header = False, index=True, line_terminator='\n')
Stdout = consoleprint
print("Yr all set for now!")
