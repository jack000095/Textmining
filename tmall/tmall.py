# -*- encoding: utf-8 -*-
import requests
import json
import re
import csv


tagcloudurl = 'https://rate.tmall.com/listTagClouds.htm?callback=jsonp_review_tags&itemId='
commenturl = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&order=3&append=0&content=0&currentPage=1&pageSize=10&tagId=&callback=jsonp457'
class tmall_comment(object):

    def __init__(self,id,seller_id,tagid='',pagenum=2):
        self.tagcloudurl = 'https://rate.tmall.com/listTagClouds.htm?callback=jsonp_review_tags&itemId='
        self.commenturl = 'https://rate.tmall.com/list_detail_rate.htm?order=3&append=0&content=0&pageSize=10&callback=jsonp457'
        self.id = str(id)
        self.seller_id = str(seller_id)
        self.tagid = str(tagid)
        self.all_name = self.id+'_'+self.seller_id
        self.tag_name = self.id+'_'+self.seller_id+'_tag'
        self.pagenum =pagenum

    def get_tag(self):
        # 浠ｇ悊鏈嶅姟鍣�
        proxyHost = "proxy.abuyun.com"
        proxyPort = "9020"

        # 浠ｇ悊闅ч亾楠岃瘉淇℃伅
        proxyUser = "H33177V4O706U12D"
        proxyPass = "ACAF4C21FD5DBEA4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host" : proxyHost,
            "port" : proxyPort,
            "user" : proxyUser,
            "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
        
        r = requests.get(tagcloudurl+self.id, proxies=proxies)
        info = r.text.split('(')[1].split(')')[0]
        json_info =json.loads(info)
        all =[]
        for i in json_info['tags']['tagClouds']:
            data =[]
            data.append(i['id'])
            data.append(i['tag'])
            all.append(data)
        self.write_csv('tag',all)


    def crawl_comment(self,i):
        # 浠ｇ悊鏈嶅姟鍣�
        proxyHost = "proxy.abuyun.com"
        proxyPort = "9020"

        # 浠ｇ悊闅ч亾楠岃瘉淇℃伅
        proxyUser = "H33177V4O706U12D"
        proxyPass = "ACAF4C21FD5DBEA4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host" : proxyHost,
            "port" : proxyPort,
            "user" : proxyUser,
            "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
        
        header ={'method':'GET',
                  'scheme':'https',
                  'accept':'*/*',
                  'user-agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
                  'cookie': '_tb_token_=sVb8rgPGUHpsvXQRb40W; uc3=sg2=VTrlU6ES9GMh1WMUQXQFOWm7B5KuYWW0ELeLPjJpqYg%3D&nk2=GcuM%2Bnf8D2NGvtI%3D&id2=UoYWPsWmpVOLnQ%3D%3D&vt3=F8dBzWESVVAW8HRxkBk%3D&lg2=URm48syIIVrSKA%3D%3D; uss=BYfv0uQRibQjOgnVHj5XmQ9sL4%2F8PbbAFWt5gC%2B158VZ8PpUjQK0%2BZyG6w%3D%3D; lgc=zcshilidiyi; tracknick=zcshilidiyi; cookie2=1cede205086624ef30278b2da045740e; sg=i9b; cookie1=BvHQuACyNempVT95TWgKKqOre2U%2FKEfeQhaSAjXtxYQ%3D; unb=1783761509; t=b28e0d809776672c360827754bdfc4cc; _l_g_=Ug%3D%3D; _nk_=zcshilidiyi; cookie17=UoYWPsWmpVOLnQ%3D%3D; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoW%2BsOfwahH1Lg%3D%3D&tag=8&lng=zh_CN; login=true; cna=iCiUEee3mlwCAW5WR6u4SJgU; pnm_cku822=058UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FSnFPdklyS3FNcSc%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhdZlhhXmVcZlpmUWxOc0l3THVMckd%2FQndKcUx2Q3dZDw%3D%3D%7CVWldfS0RMQ4zCzUVKRIyHG1TPgsiHyMaIwkyDisdaQgmcCY%3D%7CVmhIGCUFOBgkHSIcPAI4DDUVKRApFDQAPQAgHCUcIQE0DzJkMg%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; isg=Ag4O1S3q2ypM328OPxd50f3MX-QQJ9IBYoIBcjhXXpHMm671oB8imbRRpfEM'}

        params = {
                'currentPage':str(i),
                  'itemId': self.id,
                  'sellerId': self.seller_id,
                  'tagId':''}
        r = requests.get(self.commenturl,headers =header,params=params, proxies=proxies)
        info = r.text.split('(')[1].split(')')[0]
        json_info = json.loads(info)

        commentlist = json_info['rateDetail']['rateList']
        data = []
        for i in commentlist:
            slist = []
            slist.append(i['id'])
            slist.append(i['position'])
            slist.append(i['rateContent'])
            slist.append(i['rateDate'])
            slist.append(i['tamllSweetLevel'])
            data.append(slist)
        return data


    def get_allcomment(self):
        self.create(self.all_name,['id','position','rateContent','rateDate','tamllSweetLevel'])
        for i in range(1,self.pagenum+1):
            self.write_csv(self.all_name,self.crawl_comment(i))


    def cra_tag_comment(self,i):
        # 浠ｇ悊鏈嶅姟鍣�
        proxyHost = "proxy.abuyun.com"
        proxyPort = "9020"

        # 浠ｇ悊闅ч亾楠岃瘉淇℃伅
        proxyUser = "H33177V4O706U12D"
        proxyPass = "ACAF4C21FD5DBEA4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host" : proxyHost,
            "port" : proxyPort,
            "user" : proxyUser,
            "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
        
        header = {'method': 'GET',
                  'scheme': 'https',
                  'accept': '*/*',
                  'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
                  'cookie': '_tb_token_=sVb8rgPGUHpsvXQRb40W; uc3=sg2=VTrlU6ES9GMh1WMUQXQFOWm7B5KuYWW0ELeLPjJpqYg%3D&nk2=GcuM%2Bnf8D2NGvtI%3D&id2=UoYWPsWmpVOLnQ%3D%3D&vt3=F8dBzWESVVAW8HRxkBk%3D&lg2=URm48syIIVrSKA%3D%3D; uss=BYfv0uQRibQjOgnVHj5XmQ9sL4%2F8PbbAFWt5gC%2B158VZ8PpUjQK0%2BZyG6w%3D%3D; lgc=zcshilidiyi; tracknick=zcshilidiyi; cookie2=1cede205086624ef30278b2da045740e; sg=i9b; cookie1=BvHQuACyNempVT95TWgKKqOre2U%2FKEfeQhaSAjXtxYQ%3D; unb=1783761509; t=b28e0d809776672c360827754bdfc4cc; _l_g_=Ug%3D%3D; _nk_=zcshilidiyi; cookie17=UoYWPsWmpVOLnQ%3D%3D; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoW%2BsOfwahH1Lg%3D%3D&tag=8&lng=zh_CN; login=true; cna=iCiUEee3mlwCAW5WR6u4SJgU; pnm_cku822=058UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FSnFPdklyS3FNcSc%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhdZlhhXmVcZlpmUWxOc0l3THVMckd%2FQndKcUx2Q3dZDw%3D%3D%7CVWldfS0RMQ4zCzUVKRIyHG1TPgsiHyMaIwkyDisdaQgmcCY%3D%7CVmhIGCUFOBgkHSIcPAI4DDUVKRApFDQAPQAgHCUcIQE0DzJkMg%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; isg=Ag4O1S3q2ypM328OPxd50f3MX-QQJ9IBYoIBcjhXXpHMm671oB8imbRRpfEM'}

        params = {
            'currentPage': str(i),
            'itemId': self.id,
            'sellerId': self.seller_id,
            'tagId': self.tagid}
        r = requests.get(self.commenturl, headers=header, params=params, proxies=proxies)
        info = r.text.split('(')[1].split(')')[0]
        json_info = json.loads(info)
        pagenum = json_info['rateDetail']['paginator']['lastPage']

        commentlist = json_info['rateDetail']['rateList']
        data = []
        for i in commentlist:
            slist = []
            slist.append(i['id'])
            slist.append(i['position'])
            slist.append(i['rateContent'])
            slist.append(i['rateDate'])
            slist.append(i['tamllSweetLevel'])
            data.append(slist)
        return data,pagenum

    def get_tagcomment(self):
        self.create(self.tag_name, ['id', 'position', 'rateContent', 'rateDate', 'tamllSweetLevel'])


        data,page_num =self.cra_tag_comment(1)
        for i in range(1,page_num+1):
            try:
                datalist,page_num = self.cra_tag_comment(i)
                self.write_csv(self.tag_name,datalist)
            except:
                pass




    def create(self,name,title):

        with open(name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(title)



    def write_csv(self,name,list):
        with open(name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(list)






#41124112598
#725677994


#鏀瑰彉搴曚笅杈撳叆鐨勫弬鏁板嵆鍙�
#杩欎竴閮ㄥ垎涓虹埇tag鏍囩 鍜� 鍏ㄩ儴璇勮 渚嬪 tmall_comment(41124112598,725677994,tagid='520',pagenum = 2) 绗竴椤逛负鍟嗗搧id绗簩椤逛负sellerid绗笁椤逛负鎬婚〉鏁�
idlist = ['15901019265','39450691564','8647470943','547433817093']
user_idlist = ['704392951','2094190888','612263230','3108801456']
for mn in range(0,len(idlist)):
    c = tmall_comment(idlist[mn],user_idlist[mn],pagenum = 2)
    c.get_tag()
    c.get_allcomment()
    with open('tag','r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for i in rows:
            print(i)
            #鐖彇甯ag鐨勮瘎璁� 杩欓噷鍙敤鏀瑰彉 绗竴椤逛负鍟嗗搧id绗簩椤逛负sellerid绗笁椤逛笉绠�
            a = tmall_comment(535865854363,2908703327,tagid=i[0])
            a.get_tagcomment()
