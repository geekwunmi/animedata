from jikanpy import Jikan
import pandas as pd
import time

def getGenresAsString(genres):
  genreNames = []

  for genre in genres:
    genreNames.append(genre["name"])

  return ", ".join(genreNames)

def getProducersFromDict(producers): # this isn't work yet lolz i dont know how to maniplate dictionaries and sstrongs yet
  for index,producer in enumerate(producers) :
    if index == "name":
      return producer
    else:
      pass

def main():
  animeList = []

 # there's a rate limit of 30 requests/minute and 2 requests/second

  jikan = Jikan()

  # fetch values from API
  print("Fetching data from Jikan...")
  result = jikan.search(
    "anime",
    "",
    1,
    {
      "limit": 20,
      "order_by": "score",
      "sort": "desc",
      "start_date": "2020-01-01",
      "type":"tv",
      "status":"complete"
    }
  )

  print("Got", len(result["data"]), "records...")

  if len(result["data"]) != 0:
    print("Extracting and formating data...")

    # loop through each item and extract: Name, season, rating, genre, year, etc...
    for item in result["data"]:
      anime = {
        "id": item["mal_id"],
        "name": item["title"],
        "season": item["season"], # Need to confirm what this is. Is it season as in Summer, Fall, etc. Or season as in number of seasons. Not sure the API provides that.
        "score": item["score"], # e.g: PG - Children
        "year": item["year"], # can be None, maybe ["aired"]["from"] date can be used instead by extracting the year part of the date if "year" is None?
        "link": item["url"],
        "image": item["images"]["jpg"]["image_url"],
        "genre": getGenresAsString(item["genres"]),
        "producers":getProducersFromDict(item["producers"])
        # "moreinfo":item["moreinfo"]
      }

      animeList.append(anime)

  # load into dataframe and generate excel
  currentTimeStamp = time.time()
  sheetName = "animeList" + str(currentTimeStamp) + ".xlsx"
  dataFrame = pd.DataFrame(data=animeList)

  pd.set_option("display.max_columns",10)
  print(dataFrame.head(10))

  # dataFrame.to_excel(sheetName, index=False)

  # print("Data exported into", sheetName)
main()

