from flask import Flask, render_template
import requests
import time
from datetime import datetime, timezone

app = Flask(__name__)

# Dummy anime schedule data (unchanged)
anime_schedule = [
    {"title": "Demon Slayer", "day": "Monday", "time": "20:00"},
    {"title": "One Piece", "day": "Sunday", "time": "09:30"},
    {"title": "My Hero Academia", "day": "Saturday", "time": "17:30"},
]

# Function to fetch newly added anime/manga from AniList
def get_newly_added_media(media_type="ANIME", limit=5):
    query = """
    query ($page: Int, $perPage: Int, $type: MediaType) {
        Page(page: $page, perPage: $perPage) {
            media(sort: ID_DESC, type: $type) {
                id
                title {
                    romaji
                    english
                }
                startDate {
                    year
                    month
                    day
                }
                type
            }
        }
    }
    """
    variables = {
        "page": 1,
        "perPage": limit,
        "type": media_type  # "ANIME" or "MANGA"
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json()
        return data["data"]["Page"]["media"]
    return []

@app.route('/')
def home():
    # Fetch newly added anime (you can change to "MANGA" if preferred)
    new_media = get_newly_added_media(media_type="ANIME", limit=5)
    return render_template('home.html', news=new_media)  

# Function to fetch airing schedule for a specific day
def get_airing_schedule(date_str="2025-03-20"):
    # Convert the date to a timestamp range (start and end of the day in UTC)
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_time = int(target_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc).timestamp())
    end_time = int(target_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc).timestamp())

    query = """
    query ($start: Int, $end: Int) {
        Page(page: 1, perPage: 50) {
            airingSchedules(airingAt_greater: $start, airingAt_lesser: $end) {
                airingAt
                episode
                media {
                    title {
                        romaji
                        english
                    }
                }
            }
        }
    }
    """
    variables = {
        "start": start_time,
        "end": end_time
    }
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json()
        schedules = data["data"]["Page"]["airingSchedules"]
        # Format the schedule data
        formatted_schedule = []
        for schedule in schedules:
            airing_time = datetime.fromtimestamp(schedule["airingAt"], tz=timezone.utc)
            formatted_schedule.append({
                "title": schedule["media"]["title"]["english"] or schedule["media"]["title"]["romaji"],
                "episode": schedule["episode"],
                "time": airing_time.strftime("%H:%M UTC")
            })
        return formatted_schedule
    return []

@app.route('/schedule')
def schedule():
    # Fetch the airing schedule for March 20, 2025
    anime_schedule = get_airing_schedule(date_str="2025-03-20")
    return render_template('schedule.html', schedule=anime_schedule)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)