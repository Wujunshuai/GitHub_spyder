from bs4 import BeautifulSoup
import requests , pymongo , re

url = 'http://github.com'
url_1 = 'https://github.com/ptwobrussell?tab=repositories'
url_2 = 'https://github.com/ptwobrussell'

client = pymongo.MongoClient(host='localhost' , port=27017)

#===============================================================================================================
#个人仓库详情爬取，输入个人主页网址 url_1     eg:https://github.com/ptwobrussell
#爬取标签有：name-项目名称 from_url-项目原创与否及项目详细页链接
#about-项目简介 language-项目语言 fork-项目拉取次数 star-项目关注人数
#time最近一次更新时间
def page_spyder(url_1 , client_name):
    #链接数据库
    db = client[client_name]
    page = db['page']
    #爬虫主体
    add_url = '?tab=repositories'
    reques = requests.get(url_1+add_url)
    soup = BeautifulSoup(reques.text , 'lxml')
    url_one = soup.select(' ul > li > div > h3 > a')
    div = soup.find_all(attrs={'class':'col-12 d-block width-full py-4 border-bottom public fork'})
    div_self = soup.find_all(attrs={'class':'col-12 d-block width-full py-4 border-bottom public source'})
    for div_one in div+div_self:
        name = div_one.select('h3 > a')
        if(len(name) > 0):
            url_one = name[0].get('href')
            name = name[0].text.replace('\n' , '').replace(' ' , '')

        fork_from = div_one.select('span > a')
        if(len(fork_from) > 0):
            from_url = fork_from[0].get('href')
        else:
            from_url = 'himslef'


        about = div_one.select('div > p')
        if(len(about) > 0):
            about = about[0].text.replace('\n' , '')


        language = div_one.find_all(attrs={'itemprop':'programmingLanguage'})
        if(len(language) > 0):
            language = language[0].text.replace('\n' , '').replace(' ' , '')


        fork = div_one.find_all(attrs={'class': 'muted-link mr-3'})
        if (len(fork) > 1):
            star = fork[0].text.replace('\n', '').replace(' ', '')
            fork = fork[1].text.replace('\n', '').replace(' ', '')
        elif (len(fork) > 0):
            star = None
            fork = fork[0].text.replace('\n', '').replace(' ', '')


        time = div_one.select('relative-time')
        if (len(time) > 0):
            time = time[0].text
        else:
            time = None
        #合并字典，存入数据库
        data_all = {
           'name': name,
           'url': url + url_one,
           'Fork_from': from_url,
           'From_url': url + url_one,
           'About': about,
           'Language': language,
           'star': star,
           'fork': fork,
           'update': time}
        page.insert(data_all)
        print('page_spyder_ok')

#================================================================================#
#个人原创作品爬取，输入个人主页url_2，非项目页链接
#标签有name-项目名称 url-项目详细页链接 about-项目描述
#langeuage-项目所用语言 star-项目关注人数 fork-项目拉取次数
def star_pepole(url_s , client_name):
    #链接数据库
    db = client[client_name]
    Original = db['Original']
    reques = requests.get(url_s)
    soup = BeautifulSoup(reques.text , 'lxml')
    divs = soup.find_all(attrs={'class':'pinned-repo-item-content'})
    for div in divs:

        div_name = div.select('span > a')
        name = div_name[0].get_text().replace('\n' , '').replace(' ' , '')
        url = div_name[0].get('href')

        about = div.select('p')
        about = about[0].get_text().replace('\n' , '')

        fork_star = div.find_all(attrs={'class':'mb-0 f6 text-gray'})
        #有问题，会输出包括fork数和star数
        #language = fork_star[0].find(attrs={'class':'repo-language-color pinned-repo-meta'})
        #language = language.find_previous('p').get_text()
        star = fork_star[0].find_all(attrs={'aria-label':'stars'})
        star = star[0].find_previous('a')
        star = star.get_text().replace('\n' , '').replace(' ' , '')
        fork = fork_star[0].find_all(attrs={'aria-label':'forks'})
        fork = fork[0].find_previous('a')
        fork = fork.get_text().replace('\n' , '').replace(' ' , '')
        data_all = {
            'name': name,
            'url': url,
            'Fork_from': None,
            'From_url': None,
            'About': about,
            'Language': None,
            'star': star,
            'fork': fork,
            'update': None
        }
        Original.insert(data_all)
        print('star_pepole_ok')

    
#page_spyder(url_1)
#star_pepole(url_2)