# GB API Cacher v0.1

import requests
import json
from datetime import date, timedelta
import time
from tqdm import trange

# Set first day of GB videos and how many days between now and then
origin = date(2008,7,25)
duration = timedelta(days=5328)

# Where the API pulls will be stored as they are updated
current = {}

# Give http requests a user agent
get_header = {
    'User-Agent': 'gb-auto-archiver',
}

# Insert API Key
apikey = 'API_KEY_HERE'

# Establish rate limit at start (e.g. 0 requests made)
limit = 0

# Open the origin API JSON that contains only the results for the first day (07-25-2008)
c = open('api.json')
current = json.load(c)

# Loop through the duration of days above
dayrange = trange(duration.days + 1)
for d in dayrange:
    dayrange.set_description("Days cached")

    # Increase limit by 1 each time this runs. At 175 it takes an hour break. (200 is max per hour, but playing it safe)
    limit = limit + 1
    
    if limit == 175:
        print('limit reached')
        time.sleep(3600)
        print('limit reset')
        limit = 0

    # Find the end of the current updated list
    current_end = (len(current['results']))

    # Empty the 'new' variable for the next batch of API info
    new = {}

    # Figure out what day we're on and feed that into the API URL
    day = str(origin + timedelta(days=d))
    api_url = f"https://www.giantbomb.com/api/videos/?api_key={apikey}&format=json&field_list=publish_date,video_show,video_categories,name,user,guid,deck,hosts,premium,hd_url,high_url,low_url,url&filter=publish_date:{day};00:00:00|{day};23:59:59"
    
    # Download the API for this loops day and load into the 'new' variable as JSON
    api_request = requests.get(api_url, headers=get_header)
    new = api_request.json()
    
    # Find the amount of additional videos that were pulled from the API
    new_total = len(new['results'])

    # For each of the new videos, append them to the 'current' list
    for i in range(new_total):

        # If the results of the API pull show zero new shows move on to the next loop
        if new['results'] == []:
            continue
        
        # Add the new API info to the end of the current list
        current['results'].append(new['results'][i])
    
    # Write this info back into the API JSON
    with open('api.json', 'w') as updated:
        json.dump(current, updated)

    # Announce progress    
    print(f'{day} added')
    print(f'{d} more days to go!')

    # Pause for 5 seconds before continuing (safety measure to avoid being marked as malicious)
    time.sleep(5)



