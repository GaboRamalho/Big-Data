# Import required libraries
from bs4 import BeautifulSoup
import requests, openpyxl

# Create an Excel workbook and add a worksheet
file = openpyxl.Workbook()
sheet = file.active
sheet.title = 'IMDB Rank Movies'

# Write headers to the worksheet
sheet.append(['Movie Rank', 'Movie Title', 'Year of release'])

try:
    # Define the headers to mimic a legitimate browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}

    # Make a GET request to the IMDb URL with the specified headers
    source = requests.get('https://imdb.com/chart/top/', headers=headers)
    source.raise_for_status()  # Raise an exception if the request was not successful (e.g., 404 or 403)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(source.text, 'html.parser')

    # Find the <ul> element with the specified class, then find all <h3> elements within it
    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-3f13560f-0 "
                                    "sTTRj compact-list-view ipc-metadata-list--base").find_all('div', class_="sc-b85248f1-0 bCmTgE cli-children")

    # Loop through each movie element
    for movie in movies:

        # Extract movie name
        name = movie.find('a', class_="ipc-title-link-wrapper").h3.text

        # Extract movie rank
        rank = movie.find('a', class_="ipc-title-link-wrapper").get_text(strip=True).split('.')[0]

        # Extract movie year of release
        year = movie.find('div', class_="sc-b85248f1-5 kZGNjY cli-title-metadata").span.text

        # Print and add data to the worksheet
        print(rank, name, year)
        sheet.append([rank, name, year])


except Exception as e:
    print(e)

# Save the Excel file
file.save('IMDB Rank Movies.xlsx')
