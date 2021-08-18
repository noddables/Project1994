'''
Created on Apr 17, 2021
@author: Charlie
'''
'''imports'''
import FunctionsSpotify as FS
import FunctionsPython
import Variables
import sys
import csv
from pandas import DataFrame
from pathlib import Path
import spotipy
from pandas import concat as Concat 
'''variables'''
import Variables 
consoleprint = sys.stdout
TrackDataList = []
AlreadyThereTrackIds = []
SearchSubmitCount = 0 
#SearchSubmitLimit = 5
FileName = "SpotifyResultsWriteFile.csv"
FilePath = FileName
InfoFile = "TrackInfo.csv"
FeaturesFile = "TrackFeatures.csv"
WriteToFile = input(Variables.WriteToFilePrompt)
CleanWriteToFile = FunctionsPython.CleanString(WriteToFile)
PrintHeaderPrompt = "Print headers (first time printing)?"
PrintHeader = input(PrintHeaderPrompt)
CleanPrintHeader = FunctionsPython.CleanString(PrintHeader)
##
FileDf = DataFrame(columns=Variables.FileHeaders)
Token = FS.GetToken()
Headers = FS.GetHeaders(Token)
##
SearchYear = "2019"
Offset = 750
OffsetStr = str(Offset)
Limit = "50"
SearchURL = FS.GetAlbumsByYearSearchUrl(SearchYear,OffsetStr,Limit)
# print (SearchURL)
''''''
'''procedures'''
if CleanWriteToFile == "Y":
    print("OK, let me check for already written Track IDs")
    if Path(FilePath).is_file():
        with open(FilePath,'r') as openReadFile:
            reader = csv.reader(openReadFile)
            for line in reader:
                TrackId = line[0]
                if TrackId not in AlreadyThereTrackIds:
                    AlreadyThereTrackIds.append(TrackId)
        openReadFile.close()
        sys.stdout = consoleprint
    else:
        pass
    print("OK, done with that\nI'll start gathering and printing results now")
###
while SearchURL:
    FeaturesDf = DataFrame()
    InfoDf = DataFrame()
    featuresList = []
    infoList = []
    Results = FS.SubmitSearchRequest(SearchURL, Headers)
    for Result in Results:
        Next = Results["albums"]["next"]
        print(SearchURL)
        for Item in Results["albums"]["items"]:
            AlbumId = Item["id"]
            AlbumName = Item['name']
            ArtistList = Item['artists']
            ArtistsDict = ArtistList[0]
            ArtistName = ArtistsDict["name"]
            ArtistID = ArtistsDict["id"]
            TrackIds = FS.GetAlbumTrackIDs(AlbumId)
            RequestList = [track for track in TrackIds if track not in AlreadyThereTrackIds]
            RequestStr = "%2C".join(RequestList)
            InfoTracks = FS.GetSeveralTracksInfoResults(RequestStr)
            FeatureTracks = FS.GetSeveralTracksFeaturesResults(RequestStr)
            for features in FeatureTracks["audio_features"]:
                featuresList.append([
                    features['id']
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
            for info in InfoTracks["tracks"]:
                infoList.append([
                    info["id"]
                    ,info["name"]
                    ,info["popularity"]
                    ,AlbumId
                    ,AlbumName
                    ,ArtistID
                    ,ArtistName
                    ,SearchYear
                ])
            # print(infoList)
        FeaturesDf = DataFrame(featuresList,columns=Variables.FeaturesDfColumns)
        FeaturesDf = FeaturesDf.set_index("TrackId")
        InfoDf = DataFrame(infoList,columns=Variables.InfoDfColumns)
        InfoDf = InfoDf.set_index("TrackId")
        ##START failing to join two dataframes:
        FullDf = Concat([InfoDf,FeaturesDf], axis=1)
        #print(FullDf)
        #WriteDf = FullDf[Variables.FileHeaders]
        # InfoDf = InfoDf.append(FeaturesDf)
        # print(InfoDf)
        if CleanWriteToFile == "Y":
            with open(FilePath,'a') as openWriteFile:
                FullDf.to_csv(openWriteFile, header = True if CleanPrintHeader == "Y" and SearchSubmitCount == 0 else False, index=True, line_terminator='\n')
        ##END
        ##START workaround: write one file for info and features
        if CleanWriteToFile == "Y":
            with open(InfoFile,'a') as openInfoFile:
                InfoDf.to_csv(openInfoFile, header = True if CleanPrintHeader == "Y" and SearchSubmitCount == 0 else False, index=True, line_terminator='\n')
            with open(FeaturesFile,"a") as openFeaturesFile:
                FeaturesDf.to_csv(openFeaturesFile, header = True if CleanPrintHeader == "Y" and SearchSubmitCount == 0 else False, index=True, line_terminator='\n')
        else:
            sys.stdout = consoleprint
            print(FeaturesDf.to_string(index =  False))
        AlreadyThereTrackIds += RequestList
    SearchSubmitCount += 1
    SearchURL = Next
# ##
sys.stdout = consoleprint
print("Yr all set for now!")
