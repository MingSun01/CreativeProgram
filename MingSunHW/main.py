import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Step 1: Fetch the webpage content
url = "https://www.hko.gov.hk/tide/eCLKtext2021.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Step 2: Find the relevant data from the page (e.g., tide levels)
    rows = soup.find_all('tr')  # Find all rows in the table

    # Step 3: Parse the data into a dictionary of date -> list of tide levels
    tide_data = defaultdict(list)

    for row in rows[1:]:  # Skip the header row (first <tr> tag)
        cells = row.find_all('td')  # Find all cells in the row

        if len(cells) >= 10:
            # Extract the date (month and day)
            month = cells[0].get_text().strip()
            day = cells[1].get_text().strip()
            date_str = f"2021-{month}-{day}"  # Form the date string (e.g., "2021-01-01")
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Extract the tide heights (skip missing values)
            tide_levels = []
            for i in [3, 5, 7, 9]:  # Indices for tide heights in the <td> elements
                tide_text = cells[i].get_text().strip()
                try:
                    tide_level = float(tide_text)
                    tide_levels.append(tide_level)
                except ValueError:
                    continue  # Skip if it's not a valid float (e.g., missing data)

            if tide_levels:
                tide_data[date].append(sum(tide_levels) / len(tide_levels))  # Calculate daily average

    # Step 4: Limit to the first 5 days
    dates = list(tide_data.keys())[8:16]
    avg_tide_levels = [tide_data[date][0] for date in dates]

    # Step 5: Create a line chart with the average tide level per day
    plt.figure(figsize=(10, 6))
    plt.plot(dates, avg_tide_levels, marker='o', linestyle='-', color='b')

    # Step 6: Customize the chart
    plt.title("2021 Average Tide Levels (From Jan9 to Jan16)", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Tide Level (m)", fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.grid(True)

    # Step 7: Display the plot
    plt.tight_layout()
    plt.show()
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")