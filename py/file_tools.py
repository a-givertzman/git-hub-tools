import json

#
# Reads token from text file
def loadToken(path) -> str:
    try:
        with open(path, 'r') as file:
            token = file.readline()
            # print(f'token: {token}')
            if token:
                return token
            else:
                print(f'token is empty in {path}')
    except Exception as err:
        print(f'{path} - read error: {err}')
    return ''
#
# Reads json file, returns content
def loadJson(path) -> str:
    try:
        with open('src/fetch-repos-exclude.json', 'r') as file:
            jsonValue = json.load(file)
            # print(f'jsonValue: {jsonValue}')
            if jsonValue:
                return jsonValue
            else:
                print(f'excludeJson is empty in {path}')
    except:
        print(f'{path} - not found or empty or has wrong json')
    return None

