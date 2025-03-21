from flask import Flask, render_template, request
import requests
import time
from datetime import datetime, timezone

app = Flask(__name__)

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
def get_airing_schedule(date_str):
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

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    current_day = datetime.today().strftime("%Y-%m-%d")
    current_day_display = datetime.strptime(current_day, "%Y-%m-%d").strftime("%B %d, %Y") 

    # Get the selected date from the form (if submitted), otherwise default to current day
    selected_date = request.form.get('schedule_date', current_day)

    # Fetch the airing schedule for the selected date
    anime_schedule = get_airing_schedule(date_str=selected_date)
    selected_date_display = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%B %d, %Y")

    return render_template('schedule.html', 
                          schedule=anime_schedule, 
                          current_day=current_day_display, 
                          selected_date=selected_date, 
                          selected_date_display=selected_date_display)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)