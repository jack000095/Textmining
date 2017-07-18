# Textmining
Textming and some paper
文件目录：
resources：用到的相关资源
data_source：原始数据，裕洋洗过的
data_pretreatment：周韵丰洗过的，用来跑lda的
ldaresult：lda跑完生成的一些相关的记录
result：最后每条评论得分的结果，已经分为6个topic，命名规则和裕洋的命名规则一样
工作流程：
这个由于我将lda过程和评分计算分开，因此在运行代码时先运行LDAtest.py，然后在运行panduan.py
