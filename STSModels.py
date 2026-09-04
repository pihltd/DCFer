import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pandas as pd

def stsRequest(url):
    
    headers =  {'accept': 'application/json'}
    try:
        retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount('https://', adapter)
        result = session.get(url=url, headers=headers, timeout=160)
        
        if result.status_code == 200:
            return(result.json())
    except requests.exceptions.HTTPError as e:
        return ("HTTP Error: {e}")


# Get all the models

modelurl = 'https://sts.cancer.gov/v2/models/?skip=0&limit=0' 

modeljson = stsRequest(url=modelurl)

latestlist = []
for entry in modeljson:
    if entry['is_latest_version']:
        latestlist.append({'name': entry['name'], 'version': entry['version'], 'repo': entry['repository']})
        
model_df = pd.DataFrame(latestlist)
print(model_df)