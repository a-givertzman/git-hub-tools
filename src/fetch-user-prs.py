import datetime
from functools import reduce
from pprint import pprint
from dateutil import parser
import requests
import json
from file_tools import loadJson, loadToken
from pagination import fetchPaginated

#
# Fetching all pull requests from repo of authenticated User
#
# API Documentation
# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
#


if __name__ == '__main__':
    visibility = 'all'
    type = 'all'
    sort = 'full_name'
    direction = 'asc'
    page = ''
    since = '2025-07-01T00:00:00Z'
    until = '2025-07-09T00:00:00Z'
    sinceDatetime = parser.parse(since)
    untilDatetime = parser.parse(until) + datetime.timedelta(days=1)
    print(f'from: {sinceDatetime} to {untilDatetime}')

    args = [
        # '?per_page=100',
        # '&page=1',
    ]
    url = f'https://api.github.com/user/repos'
    url = reduce(lambda url, arg: f'{url}{arg}', args, url)
    uToken = loadToken('src/token.key')

    excludeRepos = loadJson('src/fetch-repos-exclude.json') or []
    excludeRepos = list(map(lambda e: e['name'], excludeRepos))

    print(f'\n- Repos to be ignored: {excludeRepos}')


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
            'before': f'{until}',                   # format: YYYY-MM-DDTHH:MM:SSZ
        }
    )

    users = {}
    print('\n- Repositories:')
    for repo in repos:
        if not repo['full_name'] in excludeRepos:
            args = [
                # '?per_page=100',
                # '&page=1',
            ]
            owner = 'a-givertzman'
            repo = repo['name']
            url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
            url = reduce(lambda url, arg: f'{url}{arg}', args, url)

            print(f'\t- {repo}  |  url: {url}')
            userPrs = fetchPaginated(
                url,
                {
                    'Accept': 'application/vnd.github+json',
                    'Authorization': f'Bearer {uToken}',
                    'X-GitHub-Api-Version': '2022-11-28',
                }
            )

            print(f'\t\tPull requests: {len(userPrs)}')

            for i, pr in enumerate(userPrs):
                # print('')
                
                # if not pr['name'] in exclude :
                #     print(f"{{\"number\": \"{pr['number']}\", \t \"state\": \"{pr['state']}\", , \t \"title\": \"{pr['title']}\", \t \"url\": \"{pr['html_url']}\"}},")
                
                commits_url = pr['commits_url']
                commits = fetchPaginated(
                    commits_url,
                    {
                        'Accept': 'application/vnd.github+json',
                        'Authorization': f'Bearer {uToken}',
                        'X-GitHub-Api-Version': '2022-11-28',
                    }
                )

                prNumber = pr['number']
                # pr = f"{{\"number\": \"{pr['number']}\", \t \"state\": \"{pr['state']}\", , \t \"title\": \"{pr['title']}\", \t \"user\": \"{pr['user']['login']}\", \t \"url\": \"{pr['html_url']}\"}},"
                foundCommits = []
                for i, commit in enumerate(commits):
                    commitDatetime = parser.parse(commit['commit']['author']['date'])
                    if sinceDatetime < commitDatetime < untilDatetime:
                        foundCommits.append(commit)
                        commitAuthor = commit['author']['login']
                        # commit = f"\ti: {i} | {{\"author\": \"{commit['author']['login']}\", \t \"date\": \"{commit['commit']['author']['date']}\"}},"
                        if commitAuthor in users:
                            if prNumber in users[commitAuthor]:
                                users[commitAuthor][prNumber]['commits'].append(commit)
                            else:
                                users[commitAuthor][prNumber] = {
                                    'pr': pr,
                                    'commits': [commit],
                                }
                        else:
                            users[commitAuthor] = {
                                prNumber: {
                                    'pr': pr,
                                    'commits': [commit],
                                },
                            }
    # pprint(users)
    if users:
        for user, userPrs in users.items():
            print(f'\nAuthor: {user}')
            for _, userPr in userPrs.items():
                pr = userPr['pr']
                if 'commits' in userPr:
                    print(f"\tPR {pr['number']} | {pr['state']}, \t title: {pr['title']}, \t url: {pr['html_url']},")
                    # print(f"\tPR {pr['number']} | user: {pr['user']['login']}, \t state: {pr['state']}, \t title: {pr['title']}, \t url: {pr['html_url']},")
                    for i, commit in enumerate(userPr['commits']):
                        print(f"\t\tCommit {i} | date: {commit['commit']['author']['date']}, \t comment: {commit['commit']['message']},")
                        # print(f"\t\tCommit {i} | {{author: {commit['author']['login']}, \t date: {commit['commit']['author']['date']}, \t comment: {commit['commit']['message']}}},")


