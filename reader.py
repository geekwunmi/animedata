from jikanpy import Jikan
import pandas as pd
import time


def getGenresAsString(genres):
    genreNames = []

    for genre in genres:
        genreNames.append(genre["name"])

    return ", ".join(genreNames)


def getProducersFromDict(producers):
    producerNames = []

    for producer in producers:
        name = producer["name"]
        producerNames.append(name)

    return ", ".join(producerNames)

def getStudio(studios):
    studionames = []

    for studio in studios:
        name = studio["name"]
        studionames.append(name)

    return ",".join(studionames)

def getTheme(themes):
    themenames = []

    for theme in themes:
        name = theme["name"]
        themenames.append(name)

    return ", ".join(themenames)

def getDemographic(demographics):
    demographicnames = []

    for demographic in demographics:
        name = demographic["name"]
        demographicnames.append(name)

    return ", ".join(demographicnames)

def getStartDate(startdate):
    date = []

    for start in startdate.keys():
        if start == 'from':
            date.append(startdate[start])
    return date[0]

def getEndDate(enddate):
    date = []

    for end in enddate.keys():
        if end == 'to':
            date.append(enddate[end])
    return date[0]


def fetchData(page: int, limit: int):
    jikan = Jikan()

    print("Fetching data from Jikan... Page:", page)
    result = jikan.search(
        "anime",
        "",
        page,
        {
            "limit": limit,
            "order_by": "score",
            "sort": "desc",
            "start_date": "2020-01-01",
            "type": "tv",
            "status": "complete"
            # "min_score": "6"
        }
    )

    return result


def appendResultToList(animeList: list[any], data: dict[str, any]):
    for item in data:
        anime = {
            "id": item["mal_id"],
            "name": item["title"],
            "season": item["season"],
            # Need to confirm what this is. Is it season as in Summer, Fall, etc. Or season as in number of seasons. Not sure the API provides that.
            "score": item["score"],  # e.g: PG - Children
            "year": item["year"],
            # can be None, maybe ["aired"]["from"] date can be used instead by extracting the year part of the date if "year" is None?
            "link": item["url"],
            "image": item["images"]["jpg"]["image_url"],
            "genre": getGenresAsString(item["genres"]),
            "producers": getProducersFromDict(item["producers"]),
            "members": item["members"],
            "start_date": getStartDate(item["aired"]),
            "end_date": getEndDate(item["aired"]),
            "studios": getStudio(item["studios"]),
            "source": item["source"],
            "themes": getTheme(item["themes"]),
            "duration": item["duration"],
            "rank": item["rank"],
            "popularity": item["popularity"],
            "favorites": item["favorites"],
            "demographics": getDemographic(item["demographics"])
        }
        animeList.append(anime)

    return animeList


def main():
    limit = 20
    page = 1
    requestCount = 0

    # fetch first set of data
    result = fetchData(page, limit)
    requestCount += 1

    if len(result["data"]) == 0:
        print("No data returned from Jikan API...")
        return

    animeList = appendResultToList([], result["data"])

    # get total size of result to determine the number of requests to fetch remaining records
    totalSizeFromApi = result["pagination"]["items"]["total"]
    print("Total size:", totalSizeFromApi, "fetching", limit, "per page")

    # reduce totalSizeFromApi by the limit since we've fetched the first set
    totalSizeFromApi -= limit

    while totalSizeFromApi > 0:
        # increment page and fetch next set
        time.sleep(1)
        page += 1
        result = fetchData(page, limit)
        requestCount += 1

        animeList = appendResultToList(animeList, result["data"])

        # again, reduce the totalSizeFromApi by the limit since we've fetched another set
        totalSizeFromApi -= limit

        if requestCount == 25:
            # pause for a minute in order not to hit the API rate limit and reset requestCount
            print("Sleeping for 60 seconds... zzzzz...")
            time.sleep(60)

            print("Waking up and resuming request...")
            requestCount = 0

    dataFrame = pd.DataFrame(data=animeList)
    pd.set_option("display.max_columns", 20)
    print(dataFrame.head(10))
    dataFrame.to_csv(r"C:\Users\Ade\Desktop\Personal\Python\Project Portfolio\animedashboard\animefile" + str(time.localtime()) + ".csv")

    return


main()