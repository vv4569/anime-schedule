from flask import Flask, render_template
import requests

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
    return render_template('home.html', news=new_media)  # Using 'news' for now, can rename later

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', schedule=anime_schedule)

@app.route('/about')
def about():
    return "<h1>About ChronoAni</h1><p>This is a placeholder for the About page.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)