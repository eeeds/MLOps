from unicodedata import numeric
from dvc import api 
import pandas as pd 
from io import StringIO
import sys 
import logging

logging.basicConfig(
    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', 
    level = logging.INFO,
    datefmt='%H:%M:%S',
    stream = sys.stdout)
# Instanciar un logger para el script
logger = logging.getLogger(__name__)

logging.info('Fetching data...')
## Connect datasets to DVC's API
movie_data_path = api.get_url('dataset/movies.csv', remote ='myremote')
finantials_data_path = api.get_url('dataset/finantials.csv', remote ='myremote')
full_data_data_path = api.get_url('dataset/full_data.csv', remote ='myremote')
opening_gross_data_path = api.get_url('dataset/opening_gross.csv', remote ='myremote')
## Read them as pandas dataframes
fin_data = pd.read_csv(finantials_data_path)
movie_data = pd.read_csv(movie_data_path)
full_data = pd.read_csv(full_data_data_path)
opening_data = pd.read_csv(opening_gross_data_path)

print(movie_data.columns)
numeric_columns_mask = (movie_data.dtypes==float) | (movie_data.dtypes==int)
numeric_columns = [column for column in numeric_columns_mask.index if numeric_columns_mask[column]]
movie_data = movie_data[numeric_columns+['movie_title']]

fin_data = fin_data[['movie_title', 'production_budget','worldwide_gross']]
fin_movie_data = pd.merge(fin_data, movie_data, on = 'movie_title', how = 'left')
full_movie_data = pd.merge(opening_data, fin_movie_data, on = 'movie_title', how = 'left')

full_movie_data = full_movie_data.drop(['gross', 'movie_title'], axis = 1)

full_movie_data.to_csv('dataset/full_data.csv', index = False)
logger.info('Data fetched and prepared')