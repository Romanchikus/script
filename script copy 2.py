# import requests
# import json
# import dateutil.parser as parser
# from pandas import pandas as pd

# def investigate( until,since=None, link="https://api.github.com/repos/django/django",branch='master') :
#     since, until = parser.parse(since).isoformat(), parser.parse(until).isoformat()
#     print('Searching in period: since={} until={}'.format(since, until))
#     # print('Searching in period: since={} until={}'.format(since.date(), until.date()))
#     # since, until = since.isoformat(), until.isoformat()
#     if since: since= '&since='+since
#     if until: until= '&until='+until
#     # num_of_comm_url = 'https://api.github.com/repos/fastlane/fastlane/pulls?base=master&since=2010-08-01T00:00:00+00:00&until=2020-09-28T07:40:00&page=1&per_page=1&state=closed'
#     # num_of_comm = requests.get(num_of_comm_url)

#     # num_of_comm1 = num_of_comm.links
#     # print("links: ", dir(num_of_comm1))
#     # print("links: ", num_of_comm1["last"]['url'])
#     # print("links: ", num_of_comm1)
#     # print("links: ", num_of_comm1)
#     url_comm1 = 'https://api.github.com/repos/django/django/commits?page=1&per_page=100'
#     num_of_comm = 'https://api.github.com/repos/fastlane/fastlane/pulls?base=master&since=2010-08-01T00:00:00+00:00&until=2020-09-28T07:40:00&page=61&per_page=100&state=closed'
#     num_of_comm1 = requests.get(url_comm1).json
#     print("json: ", dict(num_of_comm1))
#     print("json: ", num_of_comm1['text'])
#     # print("234: ", bool('prev' in num_of_comm1.links) )
#     users = {}
#     for todo in num_of_comm1.json:
#         try:
#             users[todo['author']['login']] +=1
#         except KeyError:
#             users[todo['author']['login']] = 1
#         except TypeError:
#             pass
#     top_users = sorted(users.items(), 
#                    key=lambda x: x[1], reverse=True)
#     if len(top_users)>=30: top_users=top_users[:30]
#     # top_users = pd.DataFrame(top_users, columns=['author','commits'])
#     print(top_users)






#     # def num_pages(num_of_comm1):
#     #     num_of_comm1=num_of_comm1.split('&')
#     #     del num_of_comm1[num_of_comm1.index('per_page=1')]
#     #     for s in num_of_comm1:
#     #         if "page" in s:
#     #             page=s.split('page=')
#     #     return page[1]






# if __name__ == '__main__':
#     print("Enter date since")
#     since= '2010-11-01T00:00:00Z'
#     print("Enter date until")
#     until = 'Jun 28 2020 at 7:40AM'
#     investigate(since, until)
import dateutil.parser as parser
def investigate( until,since=None, link="https://api.github.com/repos/django/django",branch='master') :
    # since, until = parser.parse(since).isoformat(), parser.parse(until).isoformat()
    print('Searching in period: since={} until={}'.format(since, until))
    if since: 
        since= '&since='+ parser.parse(since).isoformat() 
    else: 
        since= ''
    if until: 
        until= '&until='+ parser.parse(until).isoformat() 
    else: 
        until= ''
    params = {'since': since, 'until': until, 'branch': branch}
    num_of_comm_url = '{0}/commits?sha={1}{2}{3}&page=1&per_page=1'.format(link,branch,since,until)
    print(num_of_comm_url)

if __name__ == '__main__':
    print("Enter date since")
    since= '2010-11-01T00:00:00Z'
    print("Enter date until")
    until = ''
    investigate(since, until)