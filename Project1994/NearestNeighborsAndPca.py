'''imports:'''
from numpy.core.numeric import full
from pandas import DataFrame
from pandas.io.parsers import read_csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from numpy import asarray as AsArray
from numpy import abs as Abs
from numpy import sin as Sin
from numpy import cos as Cos 
from pandas import merge as Merge
from pandas import concat as Concat
# from matplotlib import pylab as plt
# from sklearn.metrics import silhouette_score
# from scipy import stats
from math import pi as Pi

'''variables:'''
readFilePath = "Project1994/SpotifySearchResults.csv"
writeFilePath = "Project1994/TestSongNeighbors.csv"
# writeFilePath = "Project1994/TestNewColumns.csv"

# writeMinorPath = "Project1994/SpotifyResultsMinor.csv"
# writeMajorPath = "Project1994/SpotifyResultsMajor.csv"

##Continuous KNeighbors Columns:
NeighborsCols = [
"Tempo"
#phase 2: divisible by 2 or divisible by 3 or other?
#         OR onehotencode prime factors (4=2, etc.)
,"TimeSignature" 
#Key as categorical?
#encode this as sin and cos of an angle?  to represent circle
#custom distance function to calculate angle for key
#,"Key"
#,"SinKey"
#,"CosKey"
#phase 2: look at mode together with key, to find matches across mode
#circle of 5ths vs. pitch shifting
,"Mode"
]

##Continuous Unsupervised Columns:
UnsupervisedCols = [
"Acousticness"
,"Danceability"
,"Energy"
,"Instrumentalness"
,"Liveness"
,"Loudness"
,"Speechiness"
,"Valence"
]

'''procedures'''
readFile = read_csv(readFilePath,header=0)
AudioDf = DataFrame(readFile)
AudioDf = AudioDf.set_index('TrackId')

'''filter audio dataframe down to Classics OR songs with n popularity and time signature 4'''
AudioDf = AudioDf.loc[ (AudioDf.SearchSource == "Classic")  | ( (AudioDf.TrackPop >= 55) &  (AudioDf.TimeSignature == 4 ) ) ]

'''key ordinal puts keys in order of circle of fifths'''
ordDict = { 0:0,  1:7 , 2:2, 3:9, 4:4, 5:11, 6:6, 7:1, 8:8, 9:3, 10:10, 11:5 }

AudioDf["KeyOrd"] = AudioDf["Key"]
AudioDf.replace({"KeyOrd": ordDict})

'''take sin and cos of key ordinal to make it cyclical:'''
AudioDf["SinKey"] = Sin((AudioDf.KeyOrd / 12) * (2 * Pi))
AudioDf["CosKey"] = Cos((AudioDf.KeyOrd / 12) * (2 * Pi))

'''do I need these if I use ColumnTransformer with passthrough?'''
UnsupervisedDf = AudioDf[UnsupervisedCols]
NeighborsDf = AudioDf[NeighborsCols]
# def NeighborsTrans(RadiusIn,DataFrameIn):
#     Trans = ColumnTransformer(transformers=[('NearestNeighbors'
#                                            , NearestNeighbors(radius=RadiusIn).radius_neighbors(DataFrameIn)
#                                            , NeighborsCols)]
#                                            , remainder='passthrough')
#     DataFrameOut = Trans.fit_transform(DataFrameIn)
#     return DataFrameOut

'''remove outliers '''
##took out this step because I'm taking nearest neighbors anyway
# UnsupervisedNoOutliersDf = UnsupervisedDf[(Abs(stats.zscore(UnsupervisedDf)) < 3).all(axis=1)]

'''scaling:'''
standard_scaler = StandardScaler()
UnsupervisedScaledDf = DataFrame(standard_scaler.fit_transform(UnsupervisedDf),index=UnsupervisedDf.index,columns=UnsupervisedCols)
##if you do remove outliers, use this:
#UnsupervisedScaledDf = DataFrame(standard_scaler.fit_transform(UnsupervisedNoOutliersDf),index=UnsupervisedNoOutliersDf.index,columns=UnsupervisedCols)

'''principal components analysis (PCA) for dimensionality reduction'''
Components = 2
Pca = PCA(Components)
PcaDf = DataFrame(Pca.fit_transform(UnsupervisedScaledDf), index = UnsupervisedScaledDf.index, columns = ['PcaGenre%i' % i for i in range(Components)] )

def GetTrackNeighbors( StartSongTrackId, DataFrameIn, RadiusIn ):
    trackDf = DataFrameIn.loc[DataFrameIn.index == StartSongTrackId]
    GetNeighbors = NearestNeighbors(radius=RadiusIn)
    GetNeighbors.fit(DataFrameIn)
    Nabes = GetNeighbors.radius_neighbors(trackDf, return_distance=False)
    NabesIndex = AsArray(Nabes[0])
    NabeIds = list(DataFrameIn.index[NabesIndex])
    NabesDf = AudioDf.loc[NabeIds]
    ReturnDf = Merge(NabesDf,PcaDf, left_index=True, right_index=True)
    ReturnDf["StartSongTrackId"] = StartSongTrackId
    ##add columns for Start Song:
    fullTrackDf = ReturnDf.loc[ReturnDf.index == StartSongTrackId]
    newColumnsDict = {column: "StartSong" + column for column in list(fullTrackDf.columns.values)}
    newColumns = list("StartSong" + column for column in list(fullTrackDf.columns.values))
    fullTrackDf = fullTrackDf.rename(columns=newColumnsDict)
    fullTrackDict = fullTrackDf.to_dict()
    refDict = {k:v[StartSongTrackId] for k,v in fullTrackDict.items()}
    ReturnDf = ReturnDf.assign(**refDict)
    return ReturnDf

'''test function with test track:'''
# TestTrackId = "69XUpOpjzDKcfdxqZebGiI" ##Destiny's Child "Independent Women, Pt 1"
TestTrackIds = [
                 #"1LuPrOdGp4NSWVsJ2sPJOx" #L'via L'Viaquez
                 "3Vo4wInECJQuz9BIBMOu8i" # Finesse Feat Cardi B
               ]
'''write test track to file for Tableau:'''
'''...and/or print test track to console:'''
with open(writeFilePath,"a") as openWriteFile:
    for TestTrackId in TestTrackIds: 
        TestTrackNeighbors = GetTrackNeighbors(TestTrackId, NeighborsDf, 70 )
        TestTrackNeighbors.to_csv(openWriteFile, header = False, index=True, line_terminator='\n')
        print(TestTrackNeighbors)

'''...and/or print test track to console:'''
# for TestTrackId in TestTrackIds: 
#     TestTrackNeighbors = GetTrackNeighbors(TestTrackId, NeighborsDf, 70 )
#     print(TestTrackNeighbors)

'''split into major and minor Dfs and analyze separately'''
# MajorDf = NeighborsDf.loc[NeighborsDf.Mode == 1]
# MinorDf = NeighborsDf.loc[NeighborsDf.Mode == 0]
'''to merge major and minor DFs with PCA:'''
# MajorPcaDf = Merge(MajorDf,PcaDf, left_index=True, right_index=True)
# MinorPcaDf = Merge(MinorDf,PcaDf, left_index=True, right_index=True)
'''write all tracks in major and minor Dfs to file:'''
# MinorTrackIds = list(set(list(MinorDf.index.values)))
# MajorTrackIds = list(set(list(MajorDf.index.values)))
# ##
# SearchNo = 0
# for TrackId in MinorTrackIds:
#     TrackNeighbors = GetTrackNeighbors(TrackId, MinorDf, 14 )
#     with open(writeFilePath,"a") as openWriteFile:
#         TrackNeighbors.to_csv(openWriteFile, header = True if SearchNo == 0 else False, index=True, line_terminator='\n')
#     SearchNo += 1

# for TrackId in MajorTrackIds:
#     TrackNeighbors = GetTrackNeighbors(TrackId, MajorDf, 14)
#     with open(writeFilePath,"a") as openWriteFile:
#         TrackNeighbors.to_csv(openWriteFile, header = False, index=True, line_terminator='\n')

# for k,v in TestTrackNeighbors.items():
#     print(k,v[TestTrackId])

