#======================================================================================
#备注
#github_repositories_spyder_up
#page_spyder函数
#个人仓库详情爬取，输入个人主页网址 url_1     eg:https://github.com/ptwobrussell
#爬取标签有：name-项目名称 from_url-项目原创与否及项目详细页链接
#about-项目简介 language-项目语言 fork-项目拉取次数 star-项目关注人数
#time最近一次更新时间
#star_pepole函数
#个人原创作品爬取，输入个人主页url_2，非项目页链接
#标签有name-项目名称 url-项目详细页链接 about-项目描述
#langeuage-项目所用语言 star-项目关注人数 fork-项目拉取次数

#---------------------------------------------------------------------------------------
#github_star_spyder
#per_next_page函数
#分页爬取 ，输入个人主页链接url_page  eg:https://github.com/ptwobrussell
#作用分析：获得每一页的链接，并调用page_star_spyder(url)函数

#---------------------------------------------------------------------------------------
#github_programpage_spyder
#contributors贡献者爬取:输入项目详细页链接-->姓名+个人主页
#fork_name项目拉取人数爬取：输入项目详细页链接-->姓名+个人主页

#=======导入库=======================================================================
from github_repositories_spyder_up import page_spyder , star_pepole
from github_star_spyder import per_next_page
from github_programpage_spyder import contributors , fork_name
from pymongo import MongoClient
import re , time

#--------------------------------------------------------------------------------------
#链接数据库
client = MongoClient(host='localhost', port=27017)

url = 'https://github.com/ptwobrussell'
def __main(url):
    #--------样本开始个人主页链接--------------------------------------------------------
    #url = 'https://github.com/ptwobrussell'
    #url_2 = 'https://github.com/ptwobrussell/python-boilerpipe'
    #----------名称------------------------------------------------------------------------
    pattern = re.compile(r'/.+$')
    client_name = re.search(pattern, url).group().replace('github.com', '').replace('/', '')
    #----------数据库---------------------------------------------------------------------
    db = client[client_name]
    page = db['page']
    #-----------函数-----------------------------------------------------------------------
    #page_spyder(url , client_name)#仓库 --> page
    #star_pepole(url , client_name)#原创 --> Original
    #per_next_page(url , client_name)#个人收藏项目 --> star
    for data in page.find():
        time.sleep(10)
        url_2 = data['url']
        contributors(url_2 , client_name)#项目贡献者 --> contributors
        fork_name(url_2 , client_name)#项目fork人 --> fork
__main(url)

