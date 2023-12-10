# import jikanpy as jik
# import pandas as pd
# import requests as re
#
# # anime = mal.Anime(1)
# # print(anime.score)
#
# # anime_title_df = pd.DataFrame(eval(str(mal.Anime.list)))
# # print(str(mal.AnimeSearchResult("Deadman ")))
#
# mushishi = jik.Jikan().anime(id=457,extension='characters')
#
# # print(mushishi)
# # print(mushishi.keys())
# # print(mushishi.get('data'))
# #
# mushishi_df = pd.DataFrame(mushishi.get('data'))
# # print(mushishi_df.columns)
# # mushishi_df = mushishi_df[['mal_id','title','title_japanese','aired','score']]
# # print(mushishi_df.head())
# jik.Jikan().anime(extension='Ani')
#
# # requests.get()
#
# I have zero hope that this will work but, hey, here's my attempt
#First thing to note: When using the code, ensure that you have the requests library installed (can be installed via pip install requests).

# Hope this helps even a little bit. If not, welp, I tried.

import requests

#Make a request to the API
response = requests.get("https://api.jikan.moe/v3/anime/28223")  # 28223 is the ID for Death Parade


# Parse the JSON response

data = response.json()

# Extract the required information
name = data['title']
score = data['score']
genre = ', '.join(data['genres'][i]['name'] for i in range(len(data['genres'])))
characters = ', '.join(character['name'] for character in data['characters'])
studio = data['studios'][0]['name']
episodes = data['episodes']

# Print the results
print(f"Name: {name}")
print(f"Score: {score}")
print(f"Genre: {genre}")
print(f"Characters: {characters}")
print(f"Studio: {studio}")
print(f"Episodes: {episodes}")


