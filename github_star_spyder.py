from  bs4 import BeautifulSoup
import requests , pymongo , re

client = pymongo.MongoClient(host='localhost' , port=27017)

url = 'https://github.com/'
url_1 = 'https://github.com/ptwobrussell'


#=======================================================================================
#个人关注仓库爬取，输入url个人主页链接 eg；https://github.com/ptwobrussell
#爬取标签有： name_url-项目详细页链接
#about-项目简介 language-项目语言 fork-项目拉取次数 star-项目关注人数
#time最近一次更新时间
def page_star_spyder(url , _client):
    #------------------链接数据库-------------------
    # pattern = re.compile(r'/.+$')
    # programe_name = re.search(pattern, url).group().replace('github.com', '').replace('/', '').replace(_client, '')
    db = client[_client]
    star_page = db['star']

    url_star = '?tab=stars'
    reques = requests.get(url+url_star)
    soup = BeautifulSoup(reques.text , 'lxml')
    div = soup.find_all(attrs={'class':'col-12 d-block width-full py-4 border-bottom'})

    for div_one in div:
        #项目名称name与name_url相同，没有重复爬取
        name_url = div_one.select('h3 > a')[0].get('href')
        #print('name: {}\n'.format(name_url) , 'url: {}'.format(url + name_url))

        about = div_one.select('div > p')
        if len(about) > 0:
            about = about[0].text.replace('\n' , '')
        #print('About: {}'.format(about))

        language = div_one.find_all(attrs={'itemprop':'programmingLanguage'})
        if(len(language) > 0):
            language = language[0].text.replace('\n' , '').replace(' ' , '')
        #print('programmingLanguage: {}'.format(language))

        fork = div_one.find_all(attrs={'class': 'muted-link mr-3'})
        if (len(fork) > 1):
            star = fork[0].text.replace('\n', '').replace(' ', '')
            fork = fork[1].text.replace('\n', '').replace(' ', '')
        elif (len(fork) > 0):
            star = None
            fork = fork[0].text.replace('\n', '').replace(' ', '')
        #print('star: {}  '.format(star), 'fork: {}'.format(fork))

        time = div_one.select('relative-time')
        if (len(time) > 0):
            time = time[0].text
        else:
            time = None
        #print('update: {}\n'.format(time))

        data_all = {
            'name': name_url,
            'url': name_url,
            'Fork_from': None,
            'From_url': None,
            'About': about,
            'Language': language,
            'star': star,
            'fork': fork,
            'update': time
        }
        star_page.insert(data_all)

    return soup

#==================================================================================
#分页爬取 ，输入个人主页链接url_page  eg:https://github.com/ptwobrussell
#作用分析：获得每一页的链接，并调用page_star_spyder(url)函数
def per_next_page(url_page , _client):
    soup = page_star_spyder(url_page , _client)
    #前一页链接
    pre = soup.find_all(attrs={'rel':'nofollow'} , text='Previous')
    if(len(pre) > 0):
        pre = pre[0].get('href')
    #后一页链接
    nex = soup.find_all(attrs={'rel':'nofollow'} , text='Next')
    if(len(nex) > 0):
        nex = nex[0].get('href')
        per_next_page(nex , _client)

#per_next_page(url_1)

