import requests
import json
import os

def fetch_all_characters():
    """
    Fetches all characters from the Star Wars API (SWAPI).

    Returns a list of character objects.

    """
    characters = []                                  # List to hold all character data
    character_url = 'https://swapi.dev/api/people/'  # initial page
    while character_url:                             # While there are more pages
        data = get_json(character_url)               # Parse the JSON response
        characters.extend(data["results"])           # Add the character objects to our list
        character_url = data["next"]                 # Get the URL of the next page
    return characters                                # Return the list of characters

def get_species_data(species_url, cache):
    """
    Given a species URL, fetch the species data (name, classification, etc).

    Return that data (probably as a dict).

    """

    if species_url in cache:        # Check if we already have this species data
        return cache[species_url]   # If we have it, return it
    
    data = get_json(species_url)    # If not, parse the JSON response
    cache[species_url] = data       # Cache the data for future use
    return data                     # Return the species data

def categorize_characters(characters):
    """
    Given a list of character dicts, categorize them by species.

    Return a dictionary {species_name: [list_of_character_names]}.

    """

    categories = {}     # Dictionary to hold categories
    species_cache = {}  # Cache for species data
    
    # Iterate over each character
    for char in characters:

        # Each character may have multiple species URLs, but often just one
        species_urls = char.get('species', [])
        
        # If there are no species URLs, treat it as 'Unknown'
        if len(species_urls) == 0:
            category_name = 'Unknown'

        # If there is at least one species URL
        else:
            # Take the first species URL (assuming it's the most relevant)
            species_url = species_urls[0]
            # Fetch species data, using cache to avoid redundant request
            species_data = get_species_data(species_url, species_cache)
            
            # Get the species name from the data
            # If the species data is empty, treat it as 'Unknown'
            category_name = species_data.get('name', 'Unknown')
        
        # If the category doesn't exist, create it
        # Append the character name to the category list
        if category_name not in categories:
            categories[category_name] = []
        categories[category_name].append(char['name'])
    
    return categories

def get_json(url):
    """
    Helper to GET JSON from a URL, for error handling.
    
    Returns the parsed JSON response.

    """
    # Make a GET request to the URL
    # If the response is not 200, raise an error
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching from {url}. Status code: {response.status_code}")
    return response.json()

def fetch_all_characters_cached(filename="characters.json"):
    """
    # Caching function for fetching all characters from the SWAPI.

    # Returns a (cached) list of character objects.
    """

    # If we already have the file, load from it
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    
    # Otherwise, fetch from API as normal
    characters = fetch_all_characters()
    # Save to file for next time
    with open(filename, "w") as f:
        json.dump(characters, f, indent=4)
    
    return characters

def main():
    """
    The main entry point of our script:
    1) Fetches all characters
    2) Categorizes them
    3) Displays the output

    """
    # Fetch all characters from SWAPI or local cache
    print("Fetching data from SWAPI...")
    all_characters = fetch_all_characters_cached()
    print(f"Fetched {len(all_characters)} characters.")

    # Categorize characters by species
    print("Categorizing characters by species...")
    categories = categorize_characters(all_characters)
    
    # Display the results
    print("Displaying results:")
    for category, names in categories.items():
        print(f"\nCategory: {category}")
        for name in names:
            print(f"- {name}")

if __name__ == "__main__":
    main()