# ChronoAni - Your Anime Timekeeper

![ChronoAni Screenshot](https://github.com/vv4569/anime-schedule/blob/main/Screenshot%202025-03-21%20162242.png?raw=true)  
*Screenshot of the ChronoAni homepage 

ChronoAni is a simple, anime-themed website built with Flask that helps anime enthusiasts keep track of airing schedules, discover newly added anime, and engage with a community. It fetches real-time data from the [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs/) to display airing schedules and newly added anime, offering a sleek, modern UI with light/dark mode support.

## Features

- **Anime Schedule:** View the airing schedule for any day, with a date picker to select a specific date. The schedule is fetched dynamically from the AniList API.
- **Newly Added Anime:** See the latest anime added to AniList, displayed on the homepage.
- **Dark Mode:** Toggle between light and dark themes, with the preference saved using `localStorage`.
- **Responsive Design:** A clean, glassmorphism-inspired UI with consistent styling across all pages (Home, Schedule, About).
- **Interactive Elements:** Hover effects, animations, and clickable schedule items for a better user experience.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **API:** AniList GraphQL API

## Installation

Follow these steps to set up and run ChronoAni locally.

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package manager)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your_username/anime-schedule.git
   cd anime-schedule
2. **Set Up a Virtual Environment (Optional but Recommended)**
       python3 -m venv venv
       source venv/bin/activate
3. **Install Dependencies**
    ``` pip install flask requests ```
4. **Confirm the Project Structure**
   ```bash
   ├── app.py
   ├── static/
   │   └── rm218-bb-07.jpg  # Background image (download or replace with your own)
   └── templates/
       ├── home.html
       ├── schedule.html
       └── about.html
6. **Run the Application**
      python3 app.py   
   
## Usage

*Home Page (/):*
- Displays a welcome message and a list of newly added anime fetched from AniList.
- Includes a "View Schedule" button to navigate to the schedule page.
  
*Schedule Page (/schedule):*
- Shows the current day (e.g., "Today is March 20, 2025").
- Features a date picker to select a day and view its airing schedule.
- Displays the schedule with anime titles, episode numbers, and airing times (in UTC).
  
*About Page (/about):*
- Provides information about ChronoAni and a contact email.
  
*Dark Mode Toggle:*
- Available on all pages in the navbar.
- Persists across page reloads using localStorage.
