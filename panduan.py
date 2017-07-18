#coding:utf-8  
import numpy as np  
import pandas as pd
import codecs 
import os

def get_score(comment):
    #获取得分词典当中每一个得分的位置
    seg = codecs.open('resources\\程度级别词语（中文）.txt')
    a = seg.readlines()
    i_list = []
    for each in range(len(a)):
        for i in range(1,7):
            if a[each].find(str(i)+'. “')!=-1:
               i_list.append(each)
            else:
                pass
    print(i_list) 
    seg.close
    

    
    #获取得分
    topic_word_file = codecs.open('lda_Result\\topic_word.txt','r','utf-8')
    score_topic_list = []
    for each_topic in topic_word_file.readlines():
        #获取每一个topic当中的7个word，输出成为list，祝词调用
        each_topic = each_topic.replace(' ',',')
        topic_word_list = []
        for count in range(1,8):
            location = each_topic.find(',')
            if count==1:
                topic_word_list.append(each_topic[8:location])
                count = count + 1
            else:
                each_topic = each_topic[:location]+' '+each_topic[location+1:]
                temp = location
                location = each_topic.find(',')
                topic_word_list.append(each_topic[temp+1:location])
                count = count + 1
        print(topic_word_list)
        
        #利用topic进行得分统计
        #查询每一个topic当中每一个word的
        score_word_list = []
        #对每一个word进行计分
        for each_word in topic_word_list:
            #先打开几个基本上用到的词典
            seg = codecs.open('resources\\程度级别词语（中文）.txt')
            neg_comment = codecs.open('resources\\负面评价词语（中文）.txt')
            neg_feel = codecs.open('resources\\负面情感词语（中文）.txt')
            pos_comment = codecs.open('resources\\正面评价词语（中文）.txt')
            pos_feel = codecs.open('resources\\正面情感词语（中文）.txt')
            
#             print(each_word)
            score_word = []
            if comment.find(each_word)!=-1:
                location_word = comment.find(each_word)
                loc_word = comment[location_word-4 if location_word-4>0 else 0:location_word+len(each_word)+4]
#                 print(loc_word)
                #对tpoic附近的情感情况判断
                score_temp = 0
                loc_adj = 0
                adj = ''
                for eeeee in neg_comment.readlines():
                    eeeee = eeeee.replace('\n','').replace('\t','').replace(' ','')
                    if eeeee in loc_word and eeeee!='':
                        score_temp = -1
                        loc_adj = loc_word.find(eeeee)
                        adj = eeeee
                        break
                for eeeee in neg_feel.readlines():
                    eeeee = eeeee.replace('\n','').replace('\t','').replace(' ','')
                    if eeeee in loc_word and eeeee!='':
                        score_temp = -1
                        loc_adj = loc_word.find(eeeee)
                        adj = eeeee
                        break
                for eeeee in pos_comment.readlines():
                    eeeee = eeeee.replace('\n','').replace('\t','').replace(' ','')
                    if eeeee in loc_word and eeeee!='':
                        score_temp = 1
                        loc_adj = loc_word.find(eeeee)
                        adj = eeeee
                        break
                for eeeee in pos_feel.readlines():
                    eeeee = eeeee.replace('\n','').replace('\t','').replace(' ','')
                    if eeeee in loc_word and eeeee!='':
                        score_temp = 1
                        loc_adj = loc_word.find(eeeee)
                        adj = eeeee
                        break
#                 print('找到形容词：'+str(adj))
#                 print('找到形容词loc：'+str(loc_adj))
#                 print('找到形容词score：'+str(score_temp))
                #对topic附近的情感情况计分
                if score_temp!=0:
                    string_adv = comment[loc_adj-4+location_word if loc_adj-4+location_word>0 else 0:loc_adj+len(adj)+4+location_word]
                    a = seg.readlines()
                    panduan = False
                    for aaa in range(len(a)):
        #                     print(str(aaa)+'   '+str(a[aaa]).strip())
                        adv = a[aaa].replace('\n','').replace('\t','').replace(' ','')
                        #找到副词位置
                        if adv in string_adv and adv!='':
#                             print('找到了副词'+adv+':'+string_adv)
                            for i_list_i in range(0,5):
                                if aaa>=i_list[i_list_i] and aaa<i_list[i_list_i+1]:
                                    score_word.append((i_list_i+1)*score_temp)
                                    panduan = True
                                    break
                                elif aaa>=i_list[5]:
                                    score_word.append(6)
                                    panduan = True
                                    break
                                else:
                                    pass
                                print('寻找adv发生错误'+str(aaa).strip()+str(a[aaa]))
                            break
                    if panduan==False:
                        score_word.append(score_temp)
                else:
                    score_word.append(score_temp)
            else:
                score_word.append(0)
            
            seg.close()
            neg_comment.close()
            neg_feel.close()
            pos_comment.close()
            pos_feel.close()
                
            sc = 0
            for eee in score_word:
                sc = sc + eee
            if len(score_word)==0:
                score_word_list.append(0)
            else:
                avg = sc/len(score_word)
                score_word_list.append(avg)
            
#             print('score_word')
#             print(score_word)
        print('score_word_list')
        print(score_word_list)
        
        sc = 0
        for eee in score_word_list:
            sc = sc + eee
        if len(score_word_list)==0:
            score_topic_list.append(0)
        else:
            avg = sc/len(score_word_list)
            score_word_list.append(avg)
            score_topic_list.append(avg)   
    print(score_topic_list)
    topic_word_file.close()
    
    return score_topic_list


def io_comment():
    dir = os.listdir('data_pretreatment')
    for each_file in dir:
        path = 'data_pretreatment\\'+each_file
        f = open(path)
        comment_list = []
        topic0_list = []
        topic1_list = []
        topic2_list = []
        topic3_list = []
        topic4_list = []
        topic5_list = []
        a = f.readlines()
        for i in range(len(a)):
            comment_list.append(a[i])
            topic0_list.append(get_score(a[i])[0])
            topic1_list.append(get_score(a[i])[1])
            topic2_list.append(get_score(a[i])[2])
            topic3_list.append(get_score(a[i])[3])
            topic4_list.append(get_score(a[i])[4])
            topic5_list.append(get_score(a[i])[5])
        data = {'comment':comment_list,'Topic0':topic0_list,'Topic1':topic1_list,'Topic2':topic2_list,'Topic3':topic3_list,'Topic4':topic4_list,'Topic5':topic5_list}
        df = pd.DataFrame(data)
        aaa_path = 'result\\'+str(each_file[:-4])+'.csv'
        print(aaa_path+'加入成功')
        df.to_csv(aaa_path,sep=',')
        

#将csv当中的comment部分变为可以训练的string的每行的csv
def preconsole():
    dir = os.listdir('test')
    for each_file in dir:
        path = 'test\\'+each_file
        new_path = 'pre\\'+each_file[:-4]
        df = pd.read_csv(path)
        df_c = df.loc[:,['comment']]
        dict = df_c.to_dict()
        for i in range(len(df_c)):    
            t = df_c['comment'][i]
            t1 = t.find('[')
            t2 = t.find(']')
            aa = t[t1+1:t2].replace(',','').replace('\'','').replace(' ','')
            print(aa)
            f = open(str(new_path)+'.txt','a')
            f.write(aa+'\n')
            f.close



io_comment()