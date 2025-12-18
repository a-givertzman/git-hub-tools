from functools import reduce
from file_tools import loadJson, loadToken
from pagination import fetchPaginated

#
# Fetching all repositories for authenticated User
#
# API Documentation
# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
#

if __name__ == '__main__':
    args = [
        # '?per_page=100',
        # '&page=1',
    ]
    url = f'https://api.github.com/user/repos'
    url = reduce(lambda url, arg: f'{url}{arg}', args, url)

    uToken = loadToken('src/token.key')

    visibility = 'all'
    type = 'all'
    sort = 'full_name'
    direction = 'asc'
    page = ''
    since = ''
    before = ''

    exclude = loadJson('src/fetch-repos-exclude.json') or []
    exclude = list(map(lambda e: e['name'], exclude))

    print(f'exclude: {exclude}')

    repos = fetchPaginated(
        url,
        {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {uToken}',
            'X-GitHub-Api-Version': '2022-11-28',
            'visibility': 'all',                    # all, public, private  |  Default: all
            'type': f'{type}',                      # all, owner, public, private, member  |  Default: all
            'sort': f'{sort}',                      # created, updated, pushed, full_name  |  Default: full_name
            'direction': f'{direction}',            # asc, desc  |  Default: asc
            'per_page': '100',                      # Default: 30, max: 100
            'page': f'{page}',                      # Default: 1
            'since': f'{since}',                    # format: YYYY-MM-DDTHH:MM:SSZ
            'before': f'{before}',                  # format: YYYY-MM-DDTHH:MM:SSZ
        }
    )

    print(f'Repositories: {len(repos)}')

    for i, repo in enumerate(repos):
        # print('')
        # if repo['private'] :
        #     print(i, f"{repo['name']} \t| \tprivate: {repo['private']}")
        
        if not repo['name'] in exclude :
            print(f"{{\"private\": \"{repo['private']}\", \t \"name\": \"{repo['full_name']}\", \t \"url\": \"{repo['html_url']}\"}},")
        
        # print(f"{{\"private\": \"{repo['private']}\", \t \"name\": \"{repo['full_name']}\", \t \"url\": \"{repo['html_url']}\"}},")
        # print(i, f"private: {repo['private']} \t {repo['name']} \t url: '{repo['html_url']}'| \t")