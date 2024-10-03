import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

url = "https://www.hko.gov.hk/tide/eCLKtext2021.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the relevant data from the page 
    rows = soup.find_all('tr') 

    # Parse the data into a dictionary of date
    tide_data = defaultdict(list)

    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')  

        if len(cells) >= 10:
            # Extract the date
            month = cells[0].get_text().strip()
            day = cells[1].get_text().strip()
            date_str = f"2021-{month}-{day}" 
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Extract the tide heights
            tide_levels = []
            for i in [3, 5, 7, 9]:  # Indices for tide heights row
                tide_text = cells[i].get_text().strip()
                try:
                    tide_level = float(tide_text)
                    tide_levels.append(tide_level)
                except ValueError:
                    continue  
            if tide_levels:
                tide_data[date].append(sum(tide_levels) / len(tide_levels))  # Calculate daily average

    # show 28 days' data
    start_date = 1
    end_date = 25
    dates = list(tide_data.keys())[start_date -1:end_date -1]
    avg_tide_levels = [tide_data[date][0] for date in dates]

    # Create a line chart with the average tide level per day
    plt.figure(figsize=(10, 6))
    plt.plot(dates, avg_tide_levels, marker='o', linestyle='-', color='b')

    # The chart
    plt.title(f"2021 Average Tide Levels (From Jan{start_date} to Jan{end_date})", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Tide Level (m)", fontsize=12)
    plt.xticks(rotation=45, ha='right')  
    plt.grid(True)

    # Display
    plt.tight_layout()
    plt.show()
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")