import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

# Step 1: Fetch the webpage content
url = "https://www.hko.gov.hk/tide/eCLKtext2022.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Step 2: Find the relevant data from the page
    rows = soup.find_all('tr')  # Find all rows in the table

    # Step 3: Parse the data into lists of dates and first height values
    dates = []
    first_heights = []

    for row in rows[1:]:  # Skip the header row (first <tr> tag)
        cells = row.find_all('td')  # Find all cells in the row

        if len(cells) >= 10:
            # Extract the date (month and day)
            month = cells[0].get_text().strip()
            day = cells[1].get_text().strip()
            date_str = f"2022-{month}-{day}"  # Form the date string (e.g., "2022-01-09")
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Extract the first tide height value
            first_height_text = cells[3].get_text().strip()  # First height value in <td> element
            try:
                first_height = float(first_height_text)
                dates.append(date)
                first_heights.append(first_height)
            except ValueError:
                continue  # Skip if it's not a valid float (e.g., missing data)

    # Step 4: Limit the data to the first 6 days
    dates = dates[11:21]
    first_heights = first_heights[11:21]

    # Step 5: Create a histogram with the date as the x-axis and first height value as the y-axis
    plt.figure(figsize=(12, 6))
    plt.bar(dates, first_heights, color='b', width=1.0)  # Use bar chart for histogram-like visualization

    # Step 6: Customize the chart
    plt.title("Tide Heights (Before 8AM) From Jan11 to Jan21", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Tide Height (m)", fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.grid(axis='y')

    # Step 7: Display the plot
    plt.tight_layout()
    plt.show()
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")