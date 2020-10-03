""" Please, enter parameters to console like in examples: 
    -l https://github.com/fastlane/fastlane -s 2020-08-09T00:00:00Z
    -l https://github.com/fastlane/fastlane -s 2020-01-09T00:00:00Z -u 'Sep 30 2020 at 7:40AM' """

import argparse
import requests
import dateutil, datetime
import dateutil.parser as parser


def investigate(
    until=None,
    since=None,
    link="https://github.com/fastlane/fastlane",
    branch="master",
):
    owner, repo = link.split("/")[3:]
    since_url, until_url = time_formater(since, until)
    print(
        "\x1b[6;31;47m"
        + "Search throughout: since={} until={}".format(since, until, "blue")
        + " on github.com repository "
        + link
        + "\x1b[0m"
    )

    url_commits = "https://api.github.com/repos/{0}/{1}/commits?sha={2}{3}{4}&page=1&per_page=100".format(
        owner, repo, branch, since_url, until_url
    )

    rate_user = rate_user_commits(url_commits)
    print("\x1b[3;30;44m" + "==Rate of commits==", "\x1b[0m")
    print_table(rate_user)

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:pr+repo:{0}/{1}+base:{2}".format(
        owner, repo, branch
    )
    num_open_pr, num_closed_pr = get_num_of_tags(url, until, since)
    print(
        "\x1b[1;32;40m" + "Quantity of PR: open->",
        num_open_pr,
        "closed->",
        num_closed_pr,
        "\x1b[0m",
    )

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:pr+repo:{0}/{1}+base:{2}".format(
        owner, repo, branch
    )
    old_RP = num_of_old_tags(url)
    print("\x1b[1;32;40m" + "Quantity of 'old' PR ->", old_RP, "\x1b[0m")

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:issue+repo:{0}/{1}".format(
        owner, repo
    )
    num_open_iss, num_closed_iss = get_num_of_tags(url, until, since)
    print(
        "\x1b[1;32;40m" + "Quantity of issues: open->",
        num_open_iss,
        "closed->",
        num_closed_iss,
        "\x1b[0m",
    )

    url = "https://api.github.com/search/issues?page=1&per_page=1&q=is:issue+repo:{0}/{1}".format(
        owner, repo
    )
    old_iss = num_of_old_tags(url, days=14)
    print("Quantity of 'old' issues ->", "\x1b[2;30;41m", old_iss, "\x1b[0m")


def get_num_of_tags(url, until, since):
    if until and since:
        num_sinc_open_pr, num_sinc_closed_pr = start_from_time(
            url=url,
            time_period=since,
        )
        num_unt_open_pr, num_unt_closed_pr = start_from_time(
            url=url,
            time_period=until,
        )
        num_open_pr, num_closed_pr = (num_sinc_open_pr - num_unt_open_pr), (
            num_sinc_closed_pr - num_unt_closed_pr
        )
    elif since:
        num_open_pr, num_closed_pr = start_from_time(url=url, time_period=since)
    elif until:
        num_open_pr, num_closed_pr = start_from_time(
            url=url, time_period=until, created="+created:<{}"
        )
    elif not (until and since):
        num_open_pr = get_num__pr(url)
        num_closed_pr = get_num__pr(url, condition="+is:closed")
    return num_open_pr, num_closed_pr


def num_of_old_tags(url, days=30):
    time_period = parser.parse(
        str(datetime.datetime.now())
    ).date() - dateutil.relativedelta.relativedelta(days=days)
    url = url + "+created:<{}".format(time_period)
    num_open_pr = get_num__pr(url)
    return num_open_pr


def start_from_time(url, time_period, created="+created:>{}"):
    time_period = parser.parse(time_period).date()
    url = url + created.format(time_period)
    num_open_pr = get_num__pr(url)
    num_closed_pr = get_num__pr(url, condition="+is:closed")
    return num_open_pr, num_closed_pr


def get_num__pr(url, condition="+is:open"):
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


def print_table(list_users):
    for i, d in enumerate(list_users):
        line = "|".join(str(x).ljust(16) for x in d)
        print(line)


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


if __name__ == "__main__":
    parse_obj = argparse.ArgumentParser(description="Git script")
    parse_obj.add_argument(
        "-l",
        action="store",
        type=str,
        dest="link",
        default="https://github.com/fastlane/fastlane",
    )
    parse_obj.add_argument("-s", action="store", type=str, dest="since", default=None)
    parse_obj.add_argument("-u", action="store", type=str, dest="until", default=None)
    parse_obj.add_argument(
        "-b", action="store", type=str, dest="branch", default="master"
    )
    args = parse_obj.parse_args()
    link, since, until, branch = args.link, args.since, args.until, args.branch
    investigate(link=link, since=since, until=until, branch=branch)
