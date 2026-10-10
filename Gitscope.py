import os #IMPORTS
import webbrowser
import requests
import customtkinter as ctk
from PIL import Image

root = ctk.CTk()
root.title("GitScope")
root.configure(fg_color="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0") # Sets screen dimensions and height.


# LOGO
logo_image = Image.open(os.path.join(os.path.dirname(__file__), "logo.png")) # Opens the logo image.
logo = ctk.CTkImage(
    light_image=logo_image,
    dark_image=logo_image,
    size=(80, 80)
)


# TITLE AND WELCOME MESSAGE
title_frame = ctk.CTkFrame(root, fg_color="transparent")
title_frame.pack(pady=(10, 0)) #10 pixexls above the title and 0 below it.

title = ctk.CTkLabel(
    title_frame,
    text="GitScope",
    font=("Orbitron", 90),
    text_color="white"
)
title.pack(side="left")

image_label = ctk.CTkLabel(
    title_frame,
    text="",
    image=logo
)
image_label.pack(side="left", padx=10)

intro = ctk.CTkLabel(
    root,
    text="Welcome to GitScope, the ultimate GitHub profile analyzer!",
    font=("Orbitron", 20),
    text_color="white"
)
intro.pack(pady=5)


# LEFT SEARCH PANEL
search_frame = ctk.CTkFrame(
    root,
    width=400,
    height=775,
    fg_color="transparent", # Sets background color.
    border_color="white",
    border_width=2
)
search_frame.place(x=10, y=10)
search_frame.pack_propagate(False) # Makes it so the frame doesn't change size based on the widgets inside it.

search_title = ctk.CTkLabel(
    search_frame,
    text="SEARCH GITHUB",
    font=("Orbitron", 25),
    text_color="white"
)
search_title.pack(pady=(25, 20)) # 25 pixels of space on the top and 20 on the bottom.

description = ctk.CTkLabel(
    search_frame,
    text=(
        "What GitScope can give you:\n\n"
        "- Profile information and links\n\n"
        "- Profile picture URL\n\n"
        "- Public repositories\n\n"
        "- Followers and following counts\n\n"
        "- Account creation date\n\n"
        "- More analytics coming soon!"
    ),
    font=("Arial", 16),
    text_color="white",
    wraplength=350, # Makes the text wrap back around when it reaches 350 pixels wide.
    justify="left"# Justify aligns the lines of text relative to each other.
)
description.pack(pady=20)

username_entry = ctk.CTkEntry(
    search_frame,
    width=320, # Width of the entry box.
    height=45, # Height of the entry box.
    placeholder_text="Enter GitHub username", # Placeholder text that appears when the entry box is empty.
    font=("Arial", 16) # Font of the entry box.
)
username_entry.pack(pady=20)

search_button = ctk.CTkButton(
    search_frame,
    text="ANALYSE PROFILE",
    width=250,
    height=45,
    font=("Orbitron", 16),
    fg_color="#2563EB",
    hover_color="#3B82F6",
    command=lambda: search_github()
)
search_button.pack(pady=10)

status_label = ctk.CTkLabel( # Called down below if no username is entered or if the username is invalid.
    search_frame,
    text="",
    font=("Arial", 14),
    text_color="white",
    wraplength=350
)
status_label.pack(pady=10)


# CENTRE ANALYTICS PANEL
dashboard_frame = ctk.CTkFrame(
    root,
    width=670,
    height=635,
    fg_color="#111111",
    border_color="white",
    border_width=2
)
dashboard_frame.place(x=430, y=150)
dashboard_frame.pack_propagate(False) # Prevents the frame from shrinking to fit its contents.

dashboard_title = ctk.CTkLabel(
    dashboard_frame,
    text="PROFILE ANALYTICS",
    font=("Orbitron", 30),
    text_color="white"
)
dashboard_title.pack(pady=25)


# RIGHT PROFILE PANEL
result_frame = ctk.CTkFrame(
    root,
    width=400,
    height=775,
    fg_color="#111111",
    border_color="white",
    border_width=2
)
result_frame.place(x=1120, y=10)
result_frame.pack_propagate(False)

result_title = ctk.CTkLabel(
    result_frame,
    text="PROFILE DETAILS",
    font=("Orbitron", 25),
    text_color="white"
)
result_title.pack(pady=25)


# CLEAR OLD RESULTS
def clear_results():
    for widget in result_frame.winfo_children(): # Gets all the widgets in the result frame.
        if widget != result_title: # If the widget is not the result title, destroy it.
            widget.destroy()

    for widget in dashboard_frame.winfo_children(): # Gets all the widgets in the dashboard frame.
        if widget != dashboard_title: # If the widget is not the dashboard title, destroy it.
            widget.destroy()


# GITHUB SEARCH AND ALL STATS
def search_github():
    clear_results()

    username = username_entry.get().strip() # Gets the username from the entry box and removes any leading or trailing whitespace.

    if not username: # Checks if a username has been entered since if there is none username comes back as false therefore if not username means if there is no username do this.
        status_label.configure(
            text="Please enter a GitHub username.",
            text_color="red"
        )
        return # Stops the function from running if no username is entered.



    try:
        response = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=10 # If the api takes longer than 10 seconds to respond, it will raise an exception.
        ) 

        if response.status_code == 404:
            status_label.configure(
                text="User not found. Check the username.",
                text_color="red"
            )
            return

        response.raise_for_status() # If the api returns a status code other than 200, it will raise an exception.
        user_data = response.json() # Turns the given data into a python dictionary.

        repos_response = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "sort": "updated"}, # Asks GitHub for up to 100 repositories per page, while "sort": "updated" sorts them by last updated, newest first.
            timeout=10 # If the api takes longer than 10 seconds to respond, it will raise an exception.
        )

        repos_response.raise_for_status() # If the api returns a status code other than 200, it will raise an exception.
        repos = repos_response.json()

        # RIGHT PANEL: PROFILE DETAILS
        profile_details = [
            ("Username", user_data.get("login", "N/A")), # The N/A is shown if the username is not found same goes for everything else here.
            ("Name", user_data.get("name") or "Not provided"),
            ("Followers", user_data.get("followers", 0)),
            ("Following", user_data.get("following", 0)),
            ("Public repositories", user_data.get("public_repos", 0)),
            ("Account created", user_data.get("created_at", "N/A")[:10]),
            ("Profile URL", user_data.get("html_url", "N/A")),
            ("Avatar URL", user_data.get("avatar_url", "N/A"))
        ]

        for label_text, value in profile_details: # Loops through the profile details and creates a label for each one.
            label = ctk.CTkLabel(
                result_frame,
                text=f"{label_text}:\n{value}", # Adds the category and value
                font=("Arial", 14),
                text_color="white",
                wraplength=350, # Wraps the text if it is too long
                justify="center"
            )
            label.pack(pady=8)

            if label_text == "Profile URL":
                label.destroy()

                link_button = ctk.CTkButton(
                    result_frame,
                    text="OPEN GITHUB PROFILE",
                    command=lambda url=value: webbrowser.open(url),
                    fg_color="#2563EB",
                    hover_color="#3B82F6",
                    width=250
                )
                link_button.pack(pady=8)


        # CENTRE PANEL: REPOSITORY ANALYTICS
        total_stars = sum(repo["stargazers_count"] for repo in repos) # Searches for all the stars on the repo list
        total_forks = sum(repo["forks_count"] for repo in repos) # Searches for all the forks on the repo list

        analytics = [
            f"Public repositories: {len(repos)}", # Shows the number of public repositories
            f"Total stars: {total_stars}", # Shows the total number of stars
            f"Total forks: {total_forks}", # Shows the total number of forks
            "",
            "TOP STARRED REPOSITORIES"
        ]

        top_repos = sorted(
            repos,
            key=lambda repo: repo["stargazers_count"], # Sorts repos from most to least stars. Sorted by making a function that returns the number of stars for each repo.
            reverse=True
        )[:5]

        for repo in top_repos:
            analytics.append(
                f'{repo["name"]}  ⭐ {repo["stargazers_count"]}' # Adds stats to a list for showcase.
            )

        analytics.extend(["", "LANGUAGES USED"]) # Same use as append but with multiple items instead of 1

        languages = {}

        for repo in repos:
            language = repo.get("language")

            if language:
                languages[language] = languages.get(language, 0) + 1 # Checks if a language exists, if it does add 1 to the language count for every language in a repo.

        top_languages = sorted(
            languages.items(),
            key=lambda item: item[1],  # Sorts languages by count. [1] is used to get the value since the store has a name; index 0 and a value; index 1.
            reverse=True
        )[:8] # Get the first 8

        if top_languages:
            for language, count in top_languages:
                analytics.append(f"{language}: {count} repositories") # Sends data for display.
        else:
            analytics.append("No language data available.") # If there are no languages print this.

        for item in analytics:      # Displays the data.
            if item == "":
                ctk.CTkLabel( # Display nothing if no data is found.
                    dashboard_frame,
                    text="",
                    height=5
                ).pack()
            elif item in [
                "TOP STARRED REPOSITORIES",        
                "LANGUAGES USED"
            ]:
                ctk.CTkLabel(    
                    dashboard_frame,
                    text=item, # Display the data.
                    font=("Orbitron", 19),
                    text_color="#3B82F6"
                ).pack(pady=(15, 8))
            else:
                ctk.CTkLabel(
                    dashboard_frame,
                    text=item,
                    font=("Arial", 16),
                    text_color="white",
                    wraplength=620
                ).pack(pady=5)

        status_label.configure( # Shows status.
            text="Profile loaded successfully!",
            text_color="#3B82F6"
        )

    except requests.exceptions.Timeout: # If the request times out show an error.
        status_label.configure(
            text="Request timed out. Try again.",
            text_color="red"
        )

    except requests.exceptions.RequestException: # If api couldn't connect show an error
        status_label.configure(
            text="Could not connect to GitHub.",
            text_color="red"
        )


# ENTER KEY SEARCH
username_entry.bind(
    "<Return>", # When enter is pressed
    lambda event: search_github() # Call the search_github function
)

root.mainloop() # Start the program.
