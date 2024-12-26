# get a list of all mtg cards to search on api (all cards in vrd history sheet)
# determine rate limit for api to tease
# hit api and store row in memory
# write out to csv 

# generate based on this curl request:
# curl 'https://api.stlotus.org:444/cards/mox%20jet?premier' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Connection: keep-alive' \
#   -H 'DNT: 1' \
#   -H 'Origin: https://stlotus.org' \
#   -H 'Referer: https://stlotus.org/' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-site' \
#   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"'

import requests
import csv
import time
import os
# Import required libraries:
# - requests: For making HTTP requests to the API
# - csv: For reading/writing CSV files
# - time: For adding delays between API calls
# - os: For file operations (currently unused)

# Main script execution:
def get_card_data(card_name):
    url = f'https://api.stlotus.org:444/cards/{card_name}?premier'
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9', 
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://stlotus.org',
        'Referer': 'https://stlotus.org/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors', 
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.get(url, headers=headers)
    return response.json()
import concurrent.futures
import urllib.parse

def process_card(card_name):
    """Process a single card and return the result"""
    try:
        # URL encode the card name
        encoded_name = urllib.parse.quote(card_name)
        card_data = get_card_data(encoded_name)
        print(f"Processed {card_name}")
        return [card_name, card_data]
    except Exception as e:
        print(f"Error processing {card_name}: {str(e)}")
        return None

# Read all card names first
with open('vrd.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    next(reader)  # Skip header
    card_names = [row[0] for row in reader]
# Open output file at the start
output_file = open('results.csv', 'w', newline='')
writer = csv.writer(output_file)
writer.writerow(['card_name', 'data'])

# Process cards in parallel
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Submit all tasks
    future_to_card = {executor.submit(process_card, name): name for name in card_names}
    print(f"Submitting {len(card_names)} cards for processing...")
    # Collect results as they complete
    for future in concurrent.futures.as_completed(future_to_card):
        result = future.result()
        if result:
            writer.writerow(result)
        time.sleep(0.1)  # Small delay to avoid overwhelming the API

print("All cards processed!")

# # Read card names from vrd.csv and write results to results.csv
# with open('vrd.csv', 'r') as input_file, open('results.csv', 'w', newline='') as output_file:
#         reader = csv.reader(input_file)
#         writer = csv.writer(output_file)
        
#         # Write header row
#         writer.writerow(['card_name', 'data'])
        
#         # Process each card
#         for row in reader:
#             card_name = row[0]  # Assuming card name is in first column
#             try:
#                 card_data = get_card_data(card_name)
#                 writer.writerow([card_name, card_data])
#                 print(f"Processed {card_name}")
#                 time.sleep(1)
#             except Exception as e:
#                 print(f"Error processing {card_name}: {str(e)}")

