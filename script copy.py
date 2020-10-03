import requests
import dateutil, datetime
import dateutil.parser as parser
from pandas import pandas as pd


def investigate(
    until=None,
    since=None,
    link="https://github.com/fastlane/fastlane",
    branch="master",
):
    owner, repo = link.split("/")[3:5]
    since_url, until_url = time_formater(since, until)
    print("Searching in period: since={} until={}".format(since, until))

    url_commits = "https://api.github.com/repos/{0}/{1}/commits?sha={2}{3}{4}&page=1&per_page=100".format(
        owner, repo, branch, since_url, until_url
    )

    rate_user = rate_user_commits(url_commits)
    print('Table ==Rate of commits\n',rate_user)

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:pr+repo:{0}/{1}+base:{2}".format(
        owner, repo, branch
    )
    num_open_pr, num_closed_pr = get_num_of_tags(url, until, since)
    print("Quantity of PR: open->", num_open_pr, "closed->", num_closed_pr)

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:pr+repo:{0}/{1}+base:{2}".format(
        owner, repo, branch
    )
    old_RP = num_of_old_tags(url)
    print("Quantity of 'old' PR ->", old_RP)

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:issue+repo:{0}/{1}".format(
        owner, repo
    )
    num_open_iss, num_closed_iss = get_num_of_tags(url, until, since)
    print("Quantity of issues: open->", num_open_iss, "closed->", num_closed_iss)

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:issue+repo:{0}/{1}".format(
        owner, repo
    )
    old_iss = num_of_old_tags(url, days=14)
    print("Quantity of 'old' issues ->", old_iss)

def get_num_of_tags(url, until, since):
    if until and since:
        num_sinc_open_pr, num_sinc_closed_pr = start_from_time(
            url=url, time_period=since,
        )
        num_unt_open_pr, num_unt_closed_pr = start_from_time(
            url=url, time_period=until,
        )
        num_open_pr, num_closed_pr = (num_sinc_open_pr-num_unt_open_pr),(num_sinc_closed_pr-num_unt_closed_pr)
    elif since:
        num_open_pr, num_closed_pr = start_from_time(
            url=url, time_period=since
        )
    elif until:
        num_open_pr, num_closed_pr = start_from_time(
            url=url, time_period=until, created="+created:<{}"
        )
    elif not (until and since):
        num_open_pr = get_num__pr(url)
        num_closed_pr = get_num__pr(url, condition='+is:closed')
    return num_open_pr, num_closed_pr


def num_of_old_tags(url, days=30):
    time_period = parser.parse(str(datetime.datetime.now())).date() - dateutil.relativedelta.relativedelta(days=days)
    url = url + "+created:<{}".format(time_period)
    print(url)
    num_open_pr = get_num__pr(url)
    return num_open_pr


# def num_PR(until, since, branch, owner, repo):
#     url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:pr+repo:{0}/{1}+base:{2}".format(
#         owner, repo, branch
#     )
#     if until and since:
#         num_sinc_open_pr, num_sinc_closed_pr = start_from_time(
#             url=url, time_period=since,
#         )
#         num_unt_open_pr, num_unt_closed_pr = start_from_time(
#             url=url, time_period=until,
#         )
#         num_open_pr, num_closed_pr = (num_sinc_open_pr-num_unt_open_pr),(num_sinc_closed_pr-num_unt_closed_pr)
#     elif since:
#         num_open_pr, num_closed_pr = start_from_time(
#             url=url, time_period=since
#         )
#     elif until:
#         num_open_pr, num_closed_pr = start_from_time(
#             url=url, time_period=until, created="+created:<{}"
#         )
#     elif not (until and since):
#         num_open_pr = get_num__pr(url)
#         num_closed_pr = get_num__pr(url, condition='+is:closed')
#     return num_open_pr, num_closed_pr


def start_from_time(url, time_period, created="+created:>{}"):
    time_period = parser.parse(time_period).date()
    url = url + created.format(time_period)
    num_open_pr = get_num__pr(url)
    num_closed_pr = get_num__pr(url, condition='+is:closed')
    print('url', url)
    return num_open_pr, num_closed_pr

def get_num__pr(url, condition='+is:open'):
    num_pr = requests.get(url + condition).json()["total_count"]
    return num_pr

def rate_user_commits(url):
    loop = True
    users = {}
    while loop == True:
        response = requests.get(url)
        users = make_rate(response.json(), users)
        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            loop = False

    top_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
    if len(top_users) >= 30:
        top_users = top_users[:30]
    top_users = pd.DataFrame(top_users, columns=["author", "commits"])
    return top_users


def make_rate(load_json, users):

    for todo in load_json:
        try:
            users[todo["author"]["login"]] += 1
        except KeyError:
            users[todo["author"]["login"]] = 1
        except TypeError:
            pass
    return users


def time_formater(since, until):
    if since:
        since = "&since=" + parser.parse(since).isoformat()
    else:
        since = ""
    if until:
        until = "&until=" + parser.parse(until).isoformat()
    else:
        until = ""
    return since, until


def num_pages(url):

    url = url.split("&")
    del url[url.index("per_page=1")]

    for s in url:
        if "page" in s:
            pages = s.split("page=")

    return int(-(-int(pages[1]) // 100))

if __name__ == "__main__":
    print("Enter date since")
    since = "2020-01-09T00:00:00Z"
    print("Enter date until")
    until = "Sep 30 2020 at 7:40AM"
    investigate( since=since, link='https://github.com/fastlane/fastlane')
    # investigate(until, since)

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'