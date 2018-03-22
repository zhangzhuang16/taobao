import scrapy
import re
import pymongo
from ..items import TaobaoItem

class WeisuenSpider(scrapy.Spider):

    name = 'taobao_'
    start_url = 'https://s.taobao.com/search?q=%E5%A5%B3%E8%A3%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=staobaoz_20180309&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48'
    detail_urls=[]
    data=[]
    client=pymongo.MongoClient("localhost",27017)
    db=client.taobao
    db=db.nvz


    def start_requests(self):
        for i in range(100):#爬100页数据
            url=self.start_url+'&s='+str(i*44) #每一页只能支持44个展示
            yield scrapy.FormRequest(url=url,callback=self.parse)

    def parse(self, response):
        # 匹配出相关信息
        item=response.xpath('//script/text()').extract()
        pat='"raw_title":"(.*?)","pic_url".*?,"detail_url":"(.*?)","view_price":"(.*?)"'
        urls=re.findall(pat,str(item)) # 列表里面一个个元组
        # print(urls)

        for url in urls:    #解析url并放入数组中
            weburl=self.url_decode(temp=url[1])
            item = TaobaoItem()
            item['name']=url[0]
            item['price']=url[2]
            item['link']=weburl
            s1 = {'name':item['name'],'price':item['price'],'lick' :weburl}
            self.db.insert(s1)
            # self.detail_urls.append(weburl)
            # self.data.append(item)
            yield item
            # 添加文档
            # s1 = {name: 'gj', age: 18}
            # s1_id = stu.insert_one(s1).inserted_id
        # for item in self.detail_urls:#这个可以抓取评论等更多相关信息
        #     yield scrapy.FormRequest(url=item,callback=self.detail)


    def url_decode(self,temp):
        while '\\' in temp:
            index=temp.find('\\')
            st=temp[index:index+7]
            temp=temp.replace(st,'')

        index=temp.find('id')
        temp=temp[:index+2]+'='+temp[index+2:]
        index=temp.find('ns')
        temp=temp[:index]+'&'+'ns='+temp[index+2:]
        index=temp.find('abbucket')
        temp='https:'+temp[:index]+'&'+'abbucket='+temp[index+8:]
        return temp


    def detail(self,response):
        print(response.url)
        #首先判断url来自天猫还是淘宝
        if 'tmall' in str(response.url):
            pass
        else:
            pass
