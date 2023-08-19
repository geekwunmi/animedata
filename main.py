import jikanpy as jik
import pandas as pd

# anime = mal.Anime(1)
# print(anime.score)

# anime_title_df = pd.DataFrame(eval(str(mal.Anime.list)))
# print(str(mal.AnimeSearchResult("Deadman ")))

mushishi = jik.Jikan().anime(id=457,extension='characters')

# print(mushishi)
# print(mushishi.keys())
# print(mushishi.get('data'))
#
mushishi_df = pd.DataFrame(mushishi.get('data'))
# print(mushishi_df.columns)
# mushishi_df = mushishi_df[['mal_id','title','title_japanese','aired','score']]
# print(mushishi_df.head())
jik.Jikan().anime(extension='Ani')





