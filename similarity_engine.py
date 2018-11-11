import sys
import numpy as np 
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors, KDTree


'''

### Note Feature Data Enginer

This python script takes an input of dataframe with all songs in artist collection and make recommendation of the most similiar song based on acoustic feature using k-nearest neighbour based on an initial selection of a song. Number of ISRC that are of interested are output as a result


Example:
        $ python similarity_engine.py 'ISRC' '#Of Songs To Recommend'
        $ python similarity_engine.py USUM70736132 5 features.csv

Output:
    It returns ISRC, title, duration of n songs that are most similiar to the initial seed song.

'''

FILENAME = '/Users/ecalabuig/projects/abbeyroad/features.csv'

def load_dataset(filename):

    '''
    Extract information of interest from artist's tracks dataframe, return scaled size of each variables and return scaler for rescaling the main output
    
    input: artist file
    output: matrix of dataset scaled for analysis, scaler, dataframe of size

    '''
    df = pd.read_csv(filename)
    df_distance_var = df[['ensemble_type_electronic','ensemble_type_folk_band'\
              ,'ensemble_type_large_jazz_band','ensemble_type_orchestra','ensemble_type_pop_band',\
              'ensemble_type_rock_band','ensemble_type_small','ensemble_type_small_jazz_band',\
              'ensemble_type_solo','ensemble_type_voice_accompaniment','instrumentation_acoustic','instrumentation_acoustic_guitar',\
              'instrumentation_brass','instrumentation_drumset','instrumentation_electric_guitar','instrumentation_electronic'\
              'instrumentation_electronic_drumkit','instrumentation_piano','instrumentation_strings_orchestra',\
               'emotion_aggressive','emotion_easy_going','emotion_happy',\
              'emotion_romantic','emotion_sad','emotion_sentimental','emotion_suspenseful',\
              'emotion_uplifting','vocal_register_female','vocal_register_male',\
                'popularity','spotify_tempo',\
                'spotify_danceability','spotify_energy','spotify_key','spotify_loudness','spotify_mode','spotify_speechiness',\
                'spotify_acousticness','spotify_instrumentalness','spotify_liveness','spotify_valence']]
    df_distance_var= df_distance_var.fillna(df_distance_var.mean())
    scaler = StandardScaler()
    scaler.fit(df_distance_var)
    df_distance_var = scaler.transform(df_distance_var)  

    return(df_distance_var,scaler,df)

df_distance_var, scaler, df = load_dataset(FILENAME)


#def main():
#    '''
#    Take argument from console of initial starting point in recommendation, number of neighbor, artist_collection_file
#    '''
#    seednumber = sys.argv[1]
#    number_of_neighbor = int(sys.argv[2])
#    file = sys.argv[3]
#    return(seednumber,number_of_neighbor,file)


def get_seed_song(seednumber,scaler,df):
    '''
    Extract seed song feature

    Input: seedsong isrc, scalar to normalized the data, dataframe of artist
    Output: seedsong information

    '''
    seed_array = df[df['isrc'] == seednumber] 
    seed_array = seed_array[['ensemble_type_electronic','ensemble_type_folk_band'\
              ,'ensemble_type_large_jazz_band','ensemble_type_orchestra','ensemble_type_pop_band',\
              'ensemble_type_rock_band','ensemble_type_small','ensemble_type_small_jazz_band',\
              'ensemble_type_solo','ensemble_type_voice_accompaniment','instrumentation_acoustic','instrumentation_acoustic_guitar',\
              'instrumentation_brass','instrumentation_drumset','instrumentation_electric_guitar','instrumentation_electronic'\
              'instrumentation_electronic_drumkit','instrumentation_piano','instrumentation_strings_orchestra',\
               'emotion_aggressive','emotion_easy_going','emotion_happy',\
              'emotion_romantic','emotion_sad','emotion_sentimental','emotion_suspenseful',\
              'emotion_uplifting','vocal_register_female','vocal_register_male',\
                'popularity','spotify_tempo',\
                'spotify_danceability','spotify_energy','spotify_key','spotify_loudness','spotify_mode','spotify_speechiness',\
                'spotify_acousticness','spotify_instrumentalness','spotify_liveness','spotify_valence']]
    scaler = scaler
    seed_array = scaler.transform(seed_array)  
    return(seed_array)

def similarity_engine(seed_song,distance_matrix,df,number_of_neighbor=10):

    '''
        k-nearest neighbor to find the most similiar song based on audio feature.

        input: seed_song feature, all_song_feature, initial songdataframe, number of neighbor
        output: isrc list

    '''
    neigh = NearestNeighbors(15, 0.4, algorithm='kd_tree')
    print(distance_matrix.shape)
    neigh.fit(distance_matrix)
    a = (neigh.kneighbors(seed_song[0:1,:], number_of_neighbor, return_distance=False))[0][0:]
    returndf = df.iloc[a,:]
    return(returndf)

def recommend(seed_isrc, number_of_neighbor=50):
    seed_song = get_seed_song(seed_isrc, scaler,  df)
    output = similarity_engine(
        seed_song, df_distance_var, df, number_of_neighbor
    )
    return list(output['isrc'])
