# **GitScope**

GitScope is a GitHub profile analyser built with Python and CustomTkinter. It uses the GitHub REST API to retrieve profile information and repository data, then presents the results through a graphical interface.

## Features

- **Profile Information** — Displays usernames, names, follower counts, following counts and account creation dates.
- **Repository Statistics** — Calculates total stars and forks across public repositories.
- **Top Starred Repositories** — Identifies and displays the user's most-starred repositories.
- **Language Analysis** — Summarises the programming languages used across public repositories.
- **Direct Profile Access** — Includes a button to open the user's GitHub profile in a web browser.
- **Error Handling** — Handles invalid usernames, connection failures and request timeouts.
- **Graphical Interface** — Organises profile information and analytics into separate panels.

## Technologies Used

- Python
- CustomTkinter
- Requests
- GitHub REST API
- Pillow (PIL)

## Project Files

| File | Purpose |
|---|---|
| `main.py` | Contains the application, API requests, data processing and GUI logic. |
| `logo.png` | Custom logo displayed in the application header. |

## What I Learned

- **API Integration** — Retrieving data from multiple endpoints and using API responses to populate an application.
- **JSON Data Processing** — Extracting information from API responses and working with lists of dictionaries.
- **Data Analysis** — Sorting repositories by star count, counting programming languages and calculating aggregate statistics.
- **Dynamic GUI Generation** — Creating interface elements from data using loops instead of manually writing each widget.
- **Event-Driven Programming** — Connecting buttons, keyboard events and mouse clicks to functions.
- **Error Handling** — Managing HTTP errors, invalid users and network timeouts.
- **Separation of Responsibilities** — Organising the interface into panels and separating result-clearing logic from the main search function.
- **Working with External Resources** — Loading local image assets and opening external URLs through the system browser.

## How to Run

1. Install Python.
2. Install the required libraries:

   ```bash
   pip install requests customtkinter pillow
