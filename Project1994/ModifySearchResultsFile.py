from pandas import read_csv
from pandas import DataFrame
from pandas import merge
from requests.sessions import Request
import FunctionsSpotify as FS
from pandas import concat as Concat
import sys
import requests
from pathlib import Path
import csv
''''''
'''to add SearchSource to previous file and write it to new file:'''
# ReadFileName = "AlbumSearchByYearResults.csv"
# WriteFileName = "SpotifySearchResults.csv"
# with open(ReadFileName,'r') as openReadFile:
#     FileDf = read_csv(openReadFile)
#     Df1994 = FileDf[:12125]
#     Df1994["SearchSource"] = "1994"
#     print(Df1994.head())
#     Df1993 = FileDf[12126:]
#     Df1993["SearchSource"] = "1993"
#     print(Df1993.head())
#     Df1994  = Df1994.append(Df1993)
# with open(WriteFileName,'w') as openWriteFile:
#     Df1994.to_csv(openWriteFile, header = True, index=False, line_terminator='\n')
'''to add track info:'''
# consoleprint = sys.stdout
# AlreadyThereTrackIds = []
# TrackInfoHeaders = ["TrackId","TrackName","TrackPop"]
# WriteHeaders = [
# #"TrackId",  #this is the index, so we don't name it as a column
# "TrackName"
# ,"TrackPop"
# ,"AlbumID"
# ,"AlbumName"
# ,"ArtistID"
# ,"ArtistName"
# ,"SearchSource"
# ,"Acousticness"
# ,"AnalysisUrl"
# ,"Danceability"
# ,"DurationMs"
# ,"Energy"
# ,"Instrumentalness"
# ,"Key"
# ,"Liveness"
# ,"Loudness"
# ,"Mode"
# ,"Speechiness"
# ,"Tempo"
# ,"TimeSignature"
# ,"TrackHref"
# ,"SearchType"
# ,"Uri"
# ,"Valence"
# ]
# #ReadFileName = "SpotifyResultsReadFile.csv"
# ReadFileName = "SpotifySearchResults.csv"
# WriteFileName = "SpotifyResultsWriteFile.csv"
# #
# with open(ReadFileName,'r') as openReadFile:
#     ReadFileDf = read_csv(openReadFile)
#     ReadFileDf.drop_duplicates(subset ="TrackId", keep = False, inplace = True)
#     DfLen = len(ReadFileDf)
#     print(DfLen)
# openReadFile.close()

# print("OK, let me check for already written Track IDs")
# if Path(WriteFileName).is_file():
#     with open(WriteFileName,'r') as openWriteFile:
#         reader = csv.reader(WriteFileName)
#         for line in reader:
#             TrackId = line[0]
#             if TrackId not in AlreadyThereTrackIds:
#                 AlreadyThereTrackIds.append(TrackId)
#     openWriteFile.close()
#     sys.stdout = consoleprint

# StartInt = 0
# StopInt = 50

# while StartInt < DfLen:
#     print("Trying " + str(StartInt) + " through " + str(StopInt))
#     TrackInfoList = []
#     SliceDf = ReadFileDf[StartInt:StopInt]
#     RequestDf = SliceDf["TrackId"]
#     RequestList = [track for track in RequestDf if track not in AlreadyThereTrackIds]
#     RequestStr = "%2C".join(RequestList)
#     TracksInfo = FS.GetSeveralTracksInfo(RequestStr)
#     for Track in TracksInfo["tracks"]:
#         TrackId = Track["id"]
#         TrackName = Track["name"]
#         TrackPop = Track["popularity"]
#         TrackInfoList.append([TrackId,TrackName,TrackPop])
#     TrackInfoDf = DataFrame(TrackInfoList, columns = TrackInfoHeaders)
#     TrackInfoDf = TrackInfoDf.set_index("TrackId")
#     SliceDf = SliceDf.set_index("TrackId")
#     FullDf = Concat([TrackInfoDf,SliceDf], axis=1)
#     WriteDf = FullDf[WriteHeaders]
#     with open(WriteFileName,'a') as openWriteFile:
#         WriteDf.to_csv(openWriteFile, header = True if StartInt ==  0 else False, index = True, line_terminator='\n')
#     AlreadyThereTrackIds += RequestList 
#     StartInt += 50
#     StopInt += 50

print("\nYr all set for now!\n")