import json
from pprint import pprint
import requests


#
# Return data if it is an array
def parseData(data):
    if isinstance(data, list):
        return data
    elif (not data):
        return []
    else:
        pprint('Unknown data:')
        pprint(data)
        return []
    # Otherwise, the array of items that we want is in an object
    # Delete keys that don't include the array of items
    # del data['incomplete_results']
    # del data['repository_selection']
    # del data['total_count']
    # # Pull out the array of items
    # namespaceKey = data.keys()[0]
    # data = data[namespaceKey]
    return data

#
# Fetching data from all pages
def fetchPaginated(url, headers):
    nextPage = True
    data = []
    while nextPage:
        response = requests.get(url, headers=headers)
        nextPage = 'next' in response.links
        if nextPage:
            url = response.links['next']['url']
        responseText = json.loads(response.text)
        # print(f'responseText: {responseText}')
        parsedData = parseData(responseText)
        data = data + parsedData
    return data
