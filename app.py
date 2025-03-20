from flask import Flask, render_template

app = Flask(__name__)

# Dummy anime schedule data (replace with real data later)
anime_schedule = [
    {"title": "Demon Slayer", "day": "Monday", "time": "20:00"},
    {"title": "One Piece", "day": "Sunday", "time": "09:30"},
    {"title": "My Hero Academia", "day": "Saturday", "time": "17:30"},
]

@app.route('/')
def home():
    return render_template('schedule.html', schedule=anime_schedule)

if __name__ == '__main__':
      app.run(debug=True, port=5001)