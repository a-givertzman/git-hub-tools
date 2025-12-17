import datetime
from functools import reduce
from dateutil import parser
from file_tools import loadJson, loadToken
from pagination import fetchPaginated
from enum import Enum

#
# Fetching all pull requests from repo of authenticated User
#
# API Documentation
# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
#

class ReportSort(Enum):
    Default = 0
    Date = 1
class ReportGroupBy(Enum):
    User = 1
    Mounth = 2
class ReportSettings:
    def __init__(self, author: list[str], sort: ReportSort, groupBy: ReportGroupBy) -> None:
        self.author = author
        self.sort = sort
        self.groupBy = groupBy
class PullRequest:
    def __init__(self, number: str, state: str, title: str, url: str) -> None:
        self.number = number
        self.state = state
        self.title = title
        self.url = url
    def __str__(self) -> str:
        return f"PR {self.number} ;\t {self.state} ;\t {self.title} ;\t {self.url}"
class Commit:
    def __init__(self, index: int, pr: PullRequest, date: str, comment: str) -> None:
        self.index = index
        self.pr = pr
        self.date = date
        self.comment = comment
    def __str__(self) -> str:
        # print(f"\tPR {pr['number']} ; {pr['state']}; \t title: {pr['title']}; \t url: {pr['html_url']}")
        # print(f"\t\tCommit {i} ; date: {commit['commit']['author']['date']}; \t comment: {commit['commit']['message']}")
        return f"Commit {self.index} ;\t {self.pr.title} ;\t {self.date} ;\t {self.comment}"


if __name__ == '__main__':
    # Report
    report = ReportSettings(
        author=[],  # ['a-givertzman', 'Anton Lobanov']
        sort=ReportSort.Date,
        groupBy=ReportGroupBy.User,
    )
    # Github Request
    visibility = 'all'
    type = 'all'
    sort = 'full_name'
    direction = 'asc'
    page = ''
    since = '2025-06-01T00:00:00Z'
    until = '2025-12-31T00:00:00Z'
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
                        # print(f"commit: {commit}")
                        # print(f"commit['author']: {commit['author']}")
                        if commit['author']:
                            commitAuthor = commit['author']['login']
                        else:
                            commitAuthor = commit['commit']['author']['name']
                        # commit = f"\ti: {i} | {{\"author\": \"{commit['author']['login']}\", \t \"date\": \"{commit['commit']['author']['date']}\"}},"
                        if not report.author or commitAuthor in report.author:
                            # print(f"commit author: {commitAuthor}")
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
                        else:
                            # print(f"skipped commit of author: {commitAuthor}")
                            pass
    # pprint(users)
    if users:
        if report.groupBy == ReportGroupBy.User:
            if report.sort == ReportSort.Date:
                for user, userPrs in users.items():
                    print(f'\nAuthor: {user}')
                    commits: list[Commit] = []
                    for _, userPr in userPrs.items():
                        pr = userPr['pr']
                        if 'commits' in userPr:
                            pr = PullRequest(pr['number'], pr['state'], pr['title'], pr['html_url'])
                            for i, commit in enumerate(userPr['commits']):
                                commits.append(
                                    Commit(
                                        index=i,
                                        pr=pr,
                                        date=commit['commit']['author']['date'],
                                        comment=commit['commit']['message'],
                                    )
                                )
                    commits.sort(key=lambda c: c.date)
                    for c in commits:
                        print(c)
            else:
                for user, userPrs in users.items():
                    print(f'\nAuthor: {user}')
                    for _, userPr in userPrs.items():
                        pr = userPr['pr']
                        if 'commits' in userPr:
                            print(f"\tPR {pr['number']} ; {pr['state']}; \t title: {pr['title']}; \t url: {pr['html_url']}")
                            # print(f"\tPR {pr['number']} | user: {pr['user']['login']}, \t state: {pr['state']}, \t title: {pr['title']}, \t url: {pr['html_url']},")
                            for i, commit in enumerate(userPr['commits']):
                                print(f"\t\tCommit {i} ; date: {commit['commit']['author']['date']}; \t comment: {commit['commit']['message']}")
                                # print(f"\t\tCommit {i} | {{author: {commit['author']['login']}, \t date: {commit['commit']['author']['date']}, \t comment: {commit['commit']['message']}}},")


