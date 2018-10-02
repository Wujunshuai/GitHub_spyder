from bs4 import BeautifulSoup
import requests , json ,jsonpath ,re , pymongo

url_github = 'https://github.com'
url = 'https://github.com/ptwobrussell/gspread'

client = pymongo.MongoClient(host='localhost' , port=27017)

#=============================================================================================================
#保留地址
#贡献者链接
url_contributors = '/graphs/contributors'
#
url_con_data = '/graphs/contributors-data'
#
url_forks = '/network/members'


#=============================================================================================================
#贡献者信息爬取，json文件爬取，输入url_own项目详细页链接
#爬取i_name贡献者姓名 ，i_url贡献者主页连接
def contributors(url_owe , _client):
    print('contributors_begin',url_owe)
    pattern = re.compile(r'/.+$')
    programe_name = re.search(pattern, url_owe).group().replace('github.com', '').replace('/', '').replace(_client , '')
    db = client[_client]
    con_page = db['contributors']
    url_con = url_owe + url_contributors
    url_data = url_owe + url_con_data
    headers = {
        'Accept':'application/json',
        'Referer': url_con,
        'Host':'github.com',
        'x-requested-eith':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'origin':'http://github.com'
    }
    try:
        con_data = requests.get(url_data , headers=headers , timeout=30)
    except:
        print('Erro')
        return 0
    soup = BeautifulSoup(con_data.content , 'lxml')
    soup = soup.text
    #print(soup)
    #try:
    soup = json.loads(soup)
    name = jsonpath.jsonpath(soup , "$..author")
    # except:
    #     name = []
    #     print(url_data)
    for i in name:
        i_name = i.get('login')
        i_url = i.get('avatar')
        #print(i_name , i_url)
        data = {
            'programe_name':programe_name,
            'name':i_name,
            'url':i_url
        }
        con_page.insert(data)
    print('end')



#============================================================================================================
#爬取项目fork人数，输入
#0原创作者、1第一层fork人、2第二层fork人
#name：姓名 url_fork_one: 个人主页
def fork_name(url_f , _client):
    list = []

    pattern = re.compile(r'/.+$')
    programe_name = re.search(pattern, url_f).group().replace('github.com', '').replace('/', '').replace(_client, '')
    url_f = url_f + url_forks
    print('fork_name')
    db = client[_client]
    fork = db['fork']
    try:
        reques = requests.get(url_f , timeout=30)
    except:
        print('Erro , {}'.format(url_f))
        return 0
    soup = BeautifulSoup(reques.text, 'lxml')
    divs = soup.find_all(attrs={'class' : 'repo'})
    for div in divs:
        tree = div.find_all(attrs={'class' : 'network-tree'})
        if(len(tree) == 0):
            names = div.select('a')
            url_fork_one = names[1].get('href')
            pattern = re.compile(r'^/.+/')
            url_fork_one = url_github + re.match(pattern, url_fork_one).group()
            level = 0
            #print('0', url_fork_one)

        elif(len(tree) == 1):
            names = div.select('a')
            url_fork_one = names[1].get('href')
            pattern = re.compile(r'^/.+/')
            url_fork_one = url_github + re.match(pattern , url_fork_one).group()
            level = 1
            #print('1', url_fork_one)
        else:
            names = div.select('a')
            url_fork_one = names[1].get('href')
            pattern = re.compile(r'^/.+/')
            url_fork_one = url_github + re.match(pattern, url_fork_one).group()
            level = 2
            #print('2', url_fork_one)
        data = {
            'level':level,
            'url': url_fork_one
        }
        list.append(data)
    data = {
        'programe_name':programe_name,
        'data':list
    }
    fork.insert(data)
    print('end')


#contributors(url)
#fork_name(url)

