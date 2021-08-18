'''
Created on Dec 8, 2019
@author: Charlie
'''
AlbumSearchChoicePrompt = "Enter the number of the Album you choose:\n"
#
ArtistBrowsePrompt = 'Please type in an artist name to browse:\n'
ArtistSearchChoicePrompt = "Enter the number of the artist you choose:\n"
ArtistSearchPrompt = "Enter the Artist's Name:\n"
#
BrowseAlbumPrompt = "Browse the Artist's Albums (Y/N/X)?:\n"
BrowseArtistTopTracksPrompt = "Browse the Artist's Top Tracks (Y/N/X)?:\n"
BrowseArtistPrompt = "Want to browse artists? (Y(es, browse)/N(o, proceed)/X(exit)):\n"
BrowsePrompt = "Want to browse? (Y(es, browse)/N(o, proceed)/X(exit)):\n"
BrowseTracksPrompt = "Want to browse tracks? (Y(es, browse)/N(o, proceed)/X(exit)):\n"
#
ChooseNmbPrompt = "Enter the number of your selection or press A to keep going:\n"
#
GetAudioFeaturesPrompt = 'Get audio features for these tracks?:\n'
#
TrackSearchSearchPrompt = "Enter an Track Title:\n"
#
WriteToFilePrompt = "Write the results to the Write File (Y/N)?:\n"
#
DirPath = "C:\\Program Files (x86)\\eclipse64\\workspace\\MusingsProject1994\\"

FileHeaders = [ 
#"TrackId",  #this is the index, so we don't name it as a column
"TrackName"
,"TrackPop"
,"AlbumID"
,"AlbumName"
,"ArtistID"
,"ArtistName"
,"SearchSource"
,"Acousticness"
,"AnalysisUrl"
,"Danceability"
,"DurationMs"
,"Energy"
,"Instrumentalness"
,"Key"
,"Liveness"
,"Loudness"
,"Mode"
,"Speechiness"
,"Tempo"
,"TimeSignature"
,"TrackHref"
,"SearchType"
,"Uri"
,"Valence"
]
FeaturesDfColumns = [
                    "TrackId"                
                    ,"Acousticness"
                    ,"AnalysisUrl"
                    ,"Danceability"
                    ,"DurationMs"
                    ,"Energy"
                    ,"Instrumentalness"
                    ,"Key"
                    ,"Liveness"
                    ,"Loudness"
                    ,"Mode"
                    ,"Speechiness"
                    ,"Tempo"
                    ,"TimeSignature"
                    ,"TrackHref"
                    ,"SearchType"
                    ,"Uri"
                    ,"Valence"
                    ]
InfoDfColumns = ["TrackId"
                ,"TrackName"
                ,"TrackPop"
                ,"AlbumID"
                ,"AlbumName"
                ,"ArtistID"
                ,"ArtistName"
                ,"SearchSource"
                ]