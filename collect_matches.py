import requests
import csv
import time

API_KEY = "RGAPI-41f3f2a6-86f2-4ba6-9635-de35daeac352" # API는 24시간마다 변경해야함!

HEADERS = {"X-Riot-Token": API_KEY}

PLATFORM_HOST = "https://kr.api.riotgames.com"
REGIONAL_HOST = "https://asia.api.riotgames.com"

TIERS = ["BRONZE", "SILVER", "GOLD"]
DIVISIONS = ["I", "II", "III", "IV"]

USER_LIMIT_PER_DIVISION = 10
MATCH_LIMIT_PER_USER = 10

def request_json(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 429:
        print("Rate limit. Waiting...")
        time.sleep(120)
        return request_json(url)

    if response.status_code != 200:
        print("ERROR", response.status_code, url)
        return None

    time.sleep(1)
    return response.json( )

def get_league_entries(tier, division):
    url = "{}/tft/league/v1/entries/{}/{}?page=1".format(
            PLATFORM_HOST,
            tier,
            division
    )
    return request_json(url)


def get_match_ids(puuid):
    url = "{}/tft/match/v1/matches/by-puuid/{}/ids?count={}".format(
          REGIONAL_HOST,
          puuid,
          MATCH_LIMIT_PER_USER
    )
    return request_json(url)

def get_match_detail(match_id):
    url = "{}/tft/match/v1/matches/{}".format(
         REGIONAL_HOST,
         match_id
    )
    return request_json(url)

rows = []
visited_matches = set()

for tier in TIERS:
    for division in DIVISIONS:
        print("Collecting", tier, division)

        entries = get_league_entries(tier, division)

        if entries is None:
            continue


        for entry in entries[:USER_LIMIT_PER_DIVISION]:

            puuid = entry.get("puuid")

            if puuid is None:
                continue
            match_ids = get_match_ids(puuid)

            for match_id in match_ids:

                if match_id in visited_matches:
                    continue

                visited_matches.add(match_id)

                match = get_match_detail(match_id)

                if match is None:
                    continue

                info = match["info"]

                for p in info["participants"]:

                    units = []
                    items = []

                    champ_details = []
                    champ_items = []

                    for unit in p.get("units", []):

                        champ = unit.get("character_id", "")
                        star = unit.get("tier", "")

                        units.append(champ)

                        champ_details.append(
                            champ + ":" + str(star)
                        )

                        unit_items = unit.get("itemNames", [])

                        if len(unit_items) > 0:
                            champ_items.append(
                                champ + ":" + str(star) + ":" + ",".join(unit_items)
                            )

                        for item in unit_items:
                            items.append(item)

                    augments = p.get("augments", [])

                    rows.append({
                        "match_id": match_id,
                        "tier": tier,
                        "division": division,
                        "placement": p.get("placement", ""),
                        "top4": 1 if p.get("placement", 9) <= 4 else 0,
                        "level": p.get("level", ""),
                        "units": "|".join(units),
                        "champ_details": "|".join(champ_details),
                        "champ_items": "|".join(champ_items),
                        "augments": "|".join(augments),
                        "items": "|".join(items)

                    })

with open(
    "tft_match_records.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames =[
            "match_id",
            "tier",
            "division",
            "placement",
            "top4",
            "level",
            "units",
            "champ_details",
            "champ_items",
            "augments",
            "items"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("CSV completed")
print("Rows:", len(rows))
print("Matches:", len(visited_matches))
