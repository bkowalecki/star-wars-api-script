# Star Wars Characters Categorizer

A Python script that fetches data from the Star Wars API (SWAPI) and categorizes characters by species. Results are displayed in your console, grouped by each species name. Characters without a defined species in SWAPI are categorized as **"Unknown."**

## Features

- **Caching**: The script will save character data locally (in `characters.json`) after the intial run so subsequent runs don't have to re-fetch from the API.  
- **Error Handling**: Basic error handling is included; if the API is unreachable or returns a non-200 status, the script raises a runtime error.

## Requirements

- **Python 3.x**
- **Requests** (as listed in `requirements.txt`)

## Installation & Usage

1. **Clone or download** this repository:

    git clone https://github.com/bkowalecki/star-wars-api-script.git

2. **Create and activate** a virtual environment (recommended):

    cd star-wars-api-script  
    python -m venv venv  

   - **Windows**:
        
        venv\Scripts\activate

   - **macOS/Linux**:
        
        source venv/bin/activate

3. **Install dependencies**:

    pip install -r requirements.txt

4. **Run the script**:

    python star_wars_characters.py

## How It Works

1. The script checks if `characters.json` already exists.
    - If **yes**, it loads character data from the file.
    - If **no**, it fetches all characters from the SWAPI `/people/` endpoint (across multiple pages) and saves them into `characters.json`.

2. It then categorizes all characters by their species (if any).

3. Finally, it prints each species category along with the character names belonging to it.

## Notes

- **Unknown Species**: Many SWAPI entries have empty species data, which appear under the **"Unknown"** category. This is due to SWAPI’s dataset, not a bug in the script.
- **Pagination**: The script automatically iterates through all pages of the SWAPI `/people/` endpoint, ensuring you retrieve every available character.
- **Deleting or Refreshing Cached Data**: If you want to force an update from the API, simply **delete** the `characters.json` file. The script will then fetch fresh data.
- **Further Enhancements**:
  - Fetching and displaying homeworld or starship info.
  - Caching species data locally as well.
  - Handling multiple species arrays more robustly (SWAPI typically has just one species, but the API can return multiple).
