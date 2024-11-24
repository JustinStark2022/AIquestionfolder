import requests
from bs4 import BeautifulSoup
import pandas as pd

def decode_secret_message(doc_url):
    """
    Extracts table data from a Google Doc URL, constructs a 2D grid of characters,
    and prints the decoded secret message.

    :param doc_url: URL of the Google Doc (published to the web)
    """
    try:
        # Fetch the document content as HTML
        response = requests.get(doc_url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all rows in the table
        rows = soup.find_all("tr")
        if not rows:
            raise ValueError("No table rows found in the document.")

        # Extract header and data rows
        headers = [header.text.strip() for header in rows[0].find_all("td")]
        data = [
            [cell.text.strip() for cell in row.find_all("td")]
            for row in rows[1:]
        ]

        # Create a DataFrame from the parsed data
        df = pd.DataFrame(data, columns=headers)

        # Ensure required columns are present
        required_columns = {'x-coordinate', 'Character', 'y-coordinate'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing columns: {required_columns - set(df.columns)}")

        # Convert coordinate columns to integers
        df['x-coordinate'] = pd.to_numeric(df['x-coordinate'], errors='coerce')
        df['y-coordinate'] = pd.to_numeric(df['y-coordinate'], errors='coerce')

        # Determine grid size
        max_x = int(df['x-coordinate'].max())
        max_y = int(df['y-coordinate'].max())

        # Initialize the grid with spaces
        grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Populate the grid with characters
        for _, row in df.iterrows():
            x, y, char = int(row['x-coordinate']), int(row['y-coordinate']), row['Character']
            grid[y][x] = char

        # Print the grid
        for row in grid:
            print("".join(row))

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
decode_secret_message(doc_url)
