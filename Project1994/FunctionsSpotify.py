'''
Created on Oct 1, 2017
@author: noddables
'''
import spotipy.util as util
import requests
'''Start functions'''
def GetToken():
    "This passes username, scope, and environment variables behind the scenes and returns the token."
    username = 'noddables'
    scope    = 'user-library-read'
    Token    = util.prompt_for_user_token(username,scope)
    if Token:
        return Token
    else:
        raise RuntimeError('GetToken Error: No Token')
#
def GetHeaders(Token):
    "This inserts the Token into the Headers template and returns the Headers"
    Headers = {'Accept':'application/json','Authorization':'Bearer ' + Token}
    if Token:
        return Headers
    else:
        raise RuntimeError('GetHeaders Error: No Token')
#
def GetSearchURL(SearchTerm,SearchType):#,SearchLimit=20,SearchOffset=5):
    "This takes in Search Term (e.g., Sleep) and Search Type (e.g., artist) and constructs the Search URL"
    SearchURL = 'https://api.spotify.com/v1/search?q=' + SearchTerm + '&type=' + SearchType
    return SearchURL
#
def GetAlbumSearchURL(ArtistID,AlbumType='album',SearchLimit=20):
    "This takes in the Artist ID and constructs the Search URL to browse Albums by that Artist."
    AlbumSearchURL = ('https://api.spotify.com/v1/artists/' + ArtistID + '/albums?market=US&album_type=' + 
                 AlbumType + '&limit=' + str(SearchLimit))
    return AlbumSearchURL
#
def GetArtistTopTracksSearchURL(ArtistID,Country='US'):
    "This takes in the Artist ID and constructs the Search URL"
    TopTracksURL = "https://api.spotify.com/v1/artists/" + ArtistID + "/top-tracks?country=" + Country
    return TopTracksURL
#
def BrowseAlbumTracksSearchURL(AlbumID,SearchLimit=20):
    AlbumTracksSearchURL = 'https://api.spotify.com/v1/albums/' + AlbumID + '/tracks?limit=' + str(SearchLimit)
    return AlbumTracksSearchURL
#   
def GetTrackAudioFeaturesURL(TrackID):
    TrackAudioFeaturesURL = 'https://api.spotify.com/v1/audio-features/' + TrackID
    return TrackAudioFeaturesURL
#
def OpenSpotifySearch(SearchTerm,SearchType):
    SearchURL = 'https://open.spotify.com/search/' + SearchType + '/' + SearchTerm
    SearchRequest = requests.get(SearchURL)#,headers=Headers)
    #SearchResults = SearchRequest.json()
    return SearchRequest
#
def SubmitSearchRequest(SearchURL,Headers):
    "This submits the GET request to search Spotify and return results in JSON."
    SearchRequest = requests.get(SearchURL,headers=Headers)
    SearchResults = SearchRequest.json()
    return SearchResults
#
def SubmitSearchRequestTest(SearchURL,Headers):
    "This submits the GET request to search Spotify and return results in JSON."
    SearchRequest = requests.get(SearchURL,headers=Headers)
    #SearchResults = SearchRequest.json()
    return SearchRequest
#
def SearchSpotify(SearchTerm,SearchType):
    "This puts the pieces together to search Spotify and return results in JSON."
    SearchURL = GetSearchURL(SearchTerm,SearchType)
    Token = GetToken()
    Headers = GetHeaders(Token)
    Results = SubmitSearchRequest(SearchURL,Headers)
    if Results:
        return Results
    else:
        raise RuntimeError('SearchSpotify Error: No Results')
#
def BrowseArtistNames(ArtistName):#,ResultLimit=20,ResultOffset=5):
    "This puts the pieces together to search Spotify and return results as a list."
    searchurl = GetSearchURL(ArtistName,'artist')#,ResultLimit,ResultOffset)
    Token = GetToken()
    Headers = GetHeaders(Token)
    results = SubmitSearchRequest(searchurl,Headers)
    resultlist = []
    for result in results['artists']['items']:
        resultlist.append(result['name'] + ',' + result['id'])
    return resultlist
#
def BrowseArtistNamesDict(ArtistName,ResultorDisplay='R'):#,ExactMatchOnly='N'):#,ResultLimit=20,ResultOffset=5):
    "This puts the pieces together to search Spotify and return results as a dictionary."
    searchurl = GetSearchURL(ArtistName,'artist')#,ResultLimit,ResultOffset)
    token = GetToken()
    headers = GetHeaders(token)
    results = SubmitSearchRequest(searchurl, headers)
    rescount = 0
    ResultDict = {}
    DisplayDict = {}
    for result in results['artists']['items']:
        rescount = rescount + 1
        resid = result['id']
        resname = result['name']
        DisplayDict[rescount] = resname
        ResultDict[resname] = resid
    if ResultorDisplay == 'R':
        return ResultDict
    elif ResultorDisplay == 'D':
        return DisplayDict
#
def BrowseArtistAlbums(ArtistID,AlbumType='album',SearchLimit=20):
    SearchURL = GetAlbumSearchURL(ArtistID, AlbumType, SearchLimit)
    Token = GetToken()
    Resultlist = []
    Headers = GetHeaders(Token)
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    for SearchResult in SearchResults['items']:
        Resultlist.append(SearchResult['name'] + ',' + SearchResult['id'])
    return Resultlist
#
def BrowseArtistAlbumsDict(ArtistID,ResultorDisplay='R',AlbumType='album',SearchLimit=20):
    SearchURL = GetAlbumSearchURL(ArtistID, AlbumType, SearchLimit)
    Token = GetToken()
    ResultDict = {}
    DisplayDict = {}
    Headers = GetHeaders(Token)
    rescount = 0
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    for result in SearchResults['items']:
        rescount = rescount + 1
        resid = result['id']
        resname = result['name']
        ResultDict[resname] = resid
        DisplayDict[rescount] = resname
    if ResultorDisplay == 'R':
        return ResultDict
    elif ResultorDisplay == 'D':
        return DisplayDict
#
def BrowseAlbumTracksDict(AlbumID,ResultorDisplay='R', SearchLimit=20):
    SearchURL = BrowseAlbumTracksSearchURL(AlbumID, str(SearchLimit))
    ResultDict = {}
    DisplayDict = {}
    Token = GetToken()
    Headers = GetHeaders(Token)
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    rescount = 0
    for SearchResult in SearchResults['items']:
        rescount = rescount + 1
        #track_number = str(SearchResult['track_number'])
        if SearchResult['track_number'] >= 10:
            track_number = str(SearchResult['track_number'])
        else:
            track_number = "0" + str(SearchResult['track_number'])
        trackname = SearchResult['name'] 
        trackid = SearchResult['id']
        DisplayDict[rescount] = track_number + ',' + trackname
        ResultDict[track_number + ',' + trackname] = trackid
    if ResultorDisplay == 'R':
        return ResultDict
    elif ResultorDisplay == 'D':
        return DisplayDict
#
def BrowseAlbumTracks(AlbumID, SearchLimit=20):
    SearchURL = BrowseAlbumTracksSearchURL(AlbumID, str(SearchLimit))
    Resultlist = []
    Token = GetToken()
    Headers = GetHeaders(Token)
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    for SearchResult in SearchResults['items']:
        Resultlist.append(#SearchResult
                           str(SearchResult['track_number']) + ',' 
                           + SearchResult['name'] + ',' 
                           + SearchResult['id'] + ','
                           + SearchResult['artists'][0]['name'] + ','
                           + SearchResult['artists'][0]['id']
                          )
    return Resultlist
#
def GetAlbumTrackIDs(AlbumID):#, SearchLimit=20):
    SearchURL = BrowseAlbumTracksSearchURL(AlbumID)#, str(SearchLimit))
    Resultlist = []
    Token = GetToken()
    Headers = GetHeaders(Token)
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    for SearchResult in SearchResults['items']:
        Resultlist.append(SearchResult['id'])
    return Resultlist
#
def GetArtistTopTracks(ArtistID,ResultorDisplay='R',Country='US'):
    SearchURL = GetArtistTopTracksSearchURL(ArtistID,Country)
    Token = GetToken()
#    ResultList = []
    ResultDict = {}
    DisplayDict = {}
    AlbumDict = {}
    Headers = GetHeaders(Token)
    rescount = 0
    SearchResults = SubmitSearchRequest(SearchURL,Headers)
    for result in SearchResults['tracks']:
        rescount = rescount + 1
        trackid = result['id']
        trackname = result['name']
        albumname = result['album']['name']
        albumid = result['album']['id']
        if rescount >= 10:
            ind = str(rescount)
        else:
            ind = "0" + str(rescount) 
        DisplayDict[ind] = trackname + ' (from ' + albumname + ')'
        ResultDict[trackname + ' (from ' + albumname + ')'] = trackid
        AlbumDict[albumid] = albumname
    if ResultorDisplay == 'R':
        return ResultDict
    elif ResultorDisplay == 'D':
        return DisplayDict
    elif ResultorDisplay == 'A':
        return AlbumDict
#
def GetTrackAudioFeatures(TrackID):
    SearchURL = GetTrackAudioFeaturesURL(TrackID)
    Token = GetToken()
    Headers = GetHeaders(Token)
    SearchResults = SubmitSearchRequest(SearchURL, Headers)
    return SearchResults
#
def GetAlbumAudioFeatures(ArtistSearchInput=''):
    '''imports:'''
    import sys
    from PythonFunctions import FunctionsPython 
    from Project1994 import Variables
    consoleprint = sys.stdout
    '''variables'''
    WriteFilePath = "C:\\Users\\Charlie\\Documents\\BrunoMarsVolta\\BrunoMarsVoltaAudioFeaturesAnalysis.csv"
    '''dicts and lists:'''
    FeaturesList = []
    '''script'''
    if ArtistSearchInput == '':
        ArtistSearchInput = input(Variables.ArtistSearchPrompt)
    ArtistSearchDisp = BrowseArtistNamesDict(ArtistSearchInput,'D')
    ArtistSearchRes = BrowseArtistNamesDict(ArtistSearchInput,'R')
    print ('\n')
    for key,value in ArtistSearchDisp.items():
        print (key, value)
    print ('\n')
    ArtistSearchChoiceNmb = int(input(Variables.ArtistSearchChoicePrompt))
    ArtistName = ArtistSearchDisp[ArtistSearchChoiceNmb]
    ArtistID = ArtistSearchRes[ArtistSearchDisp[ArtistSearchChoiceNmb]]
    print ('You chose ' + ArtistName + ' (Artist ID ' + ArtistID + ')\n')
    print ('Here are their albums:')
    AlbumSearchDisp = BrowseArtistAlbumsDict(ArtistID,'D')#,'single')
    AlbumSearchRes = BrowseArtistAlbumsDict(ArtistID,'R')#,'single')
    for key,value in AlbumSearchDisp.items():
        print ('    ', key, value)
    AlbumSearchChoiceNmb = int(input(Variables.AlbumSearchChoicePrompt))
    AlbumName = AlbumSearchDisp[AlbumSearchChoiceNmb]
    AlbumID = AlbumSearchRes[AlbumSearchDisp[AlbumSearchChoiceNmb]]
    TrackSearchDisp = BrowseAlbumTracksDict(AlbumID,'D')
    TrackSearchRes = BrowseAlbumTracksDict(AlbumID,'R')
    print ('\nYou chose ' + AlbumName + ' (Album ID ' + AlbumID + ')\n')
    print ('Here are the tracks in that album:')
    for w in sorted(TrackSearchDisp,key=TrackSearchDisp.get,reverse=False):
        print ('    ' + TrackSearchDisp[w])
    GetAudioFeaturesInput = input(Variables.GetAudioFeaturesPrompt)
    if FunctionsPython.CleanString(GetAudioFeaturesInput) == 'Y':
        for value in TrackSearchDisp.values():
            TrackName = value
            features = GetTrackAudioFeatures(TrackSearchRes[value])
            FeaturesList.append(
            ArtistName                        + ',' +
            ArtistID                          + ',' +
            AlbumName                         + ',' +
            AlbumID                           + ',' +
            TrackName                         + ',' +
            str(features['id'])               + ',' +
            features['analysis_url']          + ',' +
            str(features['energy'])           + ',' +
            str(features['liveness'])         + ',' +
            str(features['tempo'])            + ',' +
            str(features['speechiness'])      + ',' +
            str(features['acousticness'])     + ',' +
            str(features['instrumentalness']) + ',' +
            str(features['time_signature'])   + ',' +
            str(features['danceability'])     + ',' +
            str(features['key'])              + ',' +
            str(features['duration_ms'])      + ',' +
            str(features['loudness'])         + ',' +
            str(features['valence'])          + ',' +
            str(features['mode'])
            )
        FeaturesList.sort()
        WriteToFileInput = input(Variables.WriteToFilePrompt)
        if FunctionsPython.CleanString(WriteToFileInput) == "Y":
            '''to open write file:'''
            sys.stdout = open(WriteFilePath,'a')
        for n in FeaturesList:
            print (n)
        if FunctionsPython.CleanString(WriteToFileInput) == "Y":
            '''to close write file:'''
            sys.stdout.close()
            '''to go back to console print:'''
            sys.stdout = consoleprint
        print ('\nyr buns r up!')
    else:
        print ('OK, see ya!')
#
def GetAudioFeatures(SearchTrackName=''):
    '''imports'''
    #from Project1994 import FunctionsSpotify
    from PythonFunctions import FunctionsPython
    from Project1994 import Variables
    '''variables'''
    SongChooseNmbPrompt = Variables.ChooseNmbPrompt
    '''script'''
    '''Match Song'''
    if SearchTrackName == '':
        SearchTrackName = input(Variables.TrackSearchSearchPrompt)
    SongSearchRes = SearchSpotify(SearchTrackName,"Track")
    for ResultSong, ResSongID in SongSearchRes.items():
        if FunctionsPython.TheseMatch(FunctionsPython.CleanString(SearchTrackName),FunctionsPython.CleanString(ResultSong)):
            MatchSongName = ResultSong
            MatchSongID = ResSongID
            SongMatch = 'Y'
        else:
            SongMatch = 'N'
        if SongMatch == 'Y':
            print ("perfect match found for " + MatchSongName)
            print ("Is it me you're looking for?:")
            print (GetTrackAudioFeatures(MatchSongID))
        else:
            print ("no perfect match found for " + SearchTrackName)
            ArtistBrowseInput = input(Variables.BrowseTracksPrompt)
            if FunctionsPython.CleanString(ArtistBrowseInput) == 'Y':
                SearchArtistName = input(Variables.ArtistSearchPrompt)
                ArtistSearchRes = BrowseArtistNamesDict(SearchArtistName,'R')
                for ResArtistName, ResArtistID in ArtistSearchRes.items():
                    if FunctionsPython.TheseMatch(SearchArtistName,ResArtistName) == True:
                        MatchArtistID = ResArtistID
                        MatchArtistName = ResArtistName
                        print ("perfect match found for " + MatchArtistName + " (Artist ID " + MatchArtistID + ")")
                        '''Match Song'''
                        SongSearchRes = GetArtistTopTracks(MatchArtistID,'R')
                        SongSearchDisp = GetArtistTopTracks(MatchArtistID,'D')
                        for DispSongOrd, DispSongName in SongSearchDisp.items():
                            print (DispSongOrd, DispSongName)
                        SongChooseNmbInput = input(SongChooseNmbPrompt)
                        SongChooseNmb = FunctionsPython.CleanString(SongChooseNmbInput)
                        if SongChooseNmb == 'A':
                            AlbumBrowseInput = input(Variables.BrowseAlbumPrompt)
                            if FunctionsPython.CleanString(AlbumBrowseInput) == 'Y':
                                GetAlbumAudioFeatures(SearchArtistName)
                        else:
                            try:
                                MatchSongName = SongSearchDisp[SongChooseNmb]
                                MatchSongID = SongSearchRes[SongSearchDisp[SongChooseNmb]]
                                print ("You chose " + MatchSongName + " (match song id " + MatchSongID + ")")
                            except:
                                exit                    
            elif FunctionsPython.CleanString(ArtistBrowseInput) == 'N':
                print ("No song has been identified. Better luck next time!")
                exit