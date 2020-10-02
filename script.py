import requests
import json
import dateutil.parser as parser
from pandas import pandas as pd

def investigate(until,since=None, link="https://api.github.com/repos/django/django",branch='master') :

    since, until = time_formater(since, until)
    print('Searching in period: since={} until={}'.format(since, until))
    # params = {'since': since, 'until': until, 'branch': branch}
    # params_paginate =params.copy()
    # params_paginate['page']= 1
    # params_paginate['per_page']= 1
    url_commits = '{0}/commits?sha={1}{2}{3}&page=1&per_page=100'.format(link,branch,since,until)
    rate_user =  rate_user_commits(url_commits)


    num_closed_pr_url = '{0}/pulls?sha={1}{2}{3}&page=1&per_page=1&state=closed'.format(link,branch,since,until)
    num_open_pr_url = '{0}/pulls?sha={1}{2}{3}&page=1&per_page=1&state=open'.format(link,branch,since,until)

    num_closed_pr = num_pages(requests.get(num_closed_pr_url).links["last"]['url'])
    num_open_pr = num_pages(requests.get(num_open_pr_url).links["last"]['url'])
    print('Quantity of PR: open->',num_open_pr,'closed->',num_closed_pr)



    # print("url: ", num_of_comm)

    # request_text=requests.get(url).text
    # commits_rate(json.loads(request_text))

    # url = '{0}/pulls?base={1}&since={2}&until={3}&page=1&per_page=100'.format(link,branch,since,until)
    # https://api.github.com/repos/fastlane/fastlane/pulls?sha=master&since=&until=&page=1&per_page=1&state=closed

def rate_user_commits(url):
    loop=True
    users = {}
    while loop==True:
        response = requests.get(url)
        users = make_rate(response.json(), users)
        if 'next' in response.links:
            url = response.links["next"]['url']
        else:
            loop=False

    top_users = sorted(users.items(), 
                   key=lambda x: x[1], reverse=True)
    if len(top_users)>=30: top_users=top_users[:30]
    top_users = pd.DataFrame(top_users, columns=['author','commits'])  
    print(top_users)
    return top_users  


def make_rate(load_json, users):
    
    for todo in load_json:
        try:
            users[todo['author']['login']] +=1
        except KeyError:
            users[todo['author']['login']] = 1
        except TypeError:
            pass
    return users
    
def num_pages(url):

        url=url.split('&')
        del url[url.index('per_page=1')]

        for s in url:
            if "page" in s: pages=s.split('page=')
        
        return int(-(-int(pages[1]) // 100))

def time_formater(since, until):
    if since:
        since= '&since='+ parser.parse(since).isoformat() 
    else: 
        since= ''
    if until: 
        until= '&until='+ parser.parse(until).isoformat() 
    else: 
        until= ''
    return since, until


if __name__ == '__main__':
    print("Enter date since")
    since= '2020-08-01T00:00:00Z'
    print("Enter date until")
    until = 'Nov 28 2020 at 7:40AM'
    investigate(until, since)
