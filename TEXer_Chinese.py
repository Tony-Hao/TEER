# coding=utf-8
import os
import re
import sys

import datetime
from compiler.ast import While

import W_utility.file as ufile
import W_utility.preprocessing as pre
import W_utility.pretreatment as pretreatment
from W_utility.log import ext_print
from kernel.NLP import sentence as NLP_sent


now =u"现在|目前|现"
#rel_day =u"今日|昨日|昨天|明日|今天|今|近期|当日"
rel_dmy =u"今日|昨日|昨天|明日|今天|今|近期|近来|当日|去年|前年|上年|明年|本年|今年|上个月|下个月|本月"
dmy =u"年|月|日|天|周期|星期|周|小时|时|钟头|分钟|秒|秒钟"
num =u"半|一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|二十|三十"
weekday=u"星期一|星期二|星期三|星期四|星期五|星期六|星期日|星期天|周一|周二|周三|周四|周五|周六|周日"
#adj =u"大概|约|前|"
exp1=u"大概|近|约|前|后|第|每|"
#after=u"余前|余|前|后|内|"
exp2=u"余前|余后|余|来|前|后|"
#status=u"前|后|"
#adj1=u"个半|个"
rel_time=u"上午|下午|早上|白天|中午|傍晚|晚上"
def temporal_processing (fin, fout = None, type = "testing",   fin_t = None, rep_enable = False, rep_word = "", event = False, X3 = False):

    # read the input data
    if (fin) is None:
        print ext_print ('no input file found --- interrupting')
        return
    texts = ufile.read_file (fin, 1, False)

    if texts is None or len(texts) <= 0:
        print ext_print ('no text available for processing --- interrupting')
        return

    print ext_print ('start to process temporal information in text file %s' % fin)

    if type == "training":
        tpatts = temporal_training(texts);
        # output pattern result
        if (fout is None) or (fout == ""):
            fout = os.path.splitext(fin)[0] + "_pat" + os.path.splitext(fin)[1]

        ufile.write_file (fout, sorted(tpatts, key=tpatts.get, reverse=True), False)
        print ext_print ('saved trained patterns into: %s' % fout)


    elif type == "testing":
        # read the pattern data
        if (fin_t) is None:
            print ext_print ('no pattern file found --- interrupting')
            return
        tpatts = ufile.read_file (fin_t, 1, False)
        if tpatts is None or len(tpatts) <= 0:
            print ext_print ('no patterns available for processing --- interrupting')
            return

        result = temporal_testing(texts, tpatts, rep_enable, rep_word, event);
        if X3:
            result = using_TimeX3(result)

        # output result
        if (fout is None) or (fout == ""):
            if X3:
                fout = os.path.splitext(fin)[0] + "_TEXer.xml"
            else:
                fout = os.path.splitext(fin)[0] + "_TEXer" + os.path.splitext(fin)[1]

        ufile.write_file (fout, result, False)
        print ext_print ('saved processed results into: %s' % fout)

    print ext_print ('all tasks completed\n')
    return True


# mine patterns from a text file (training data)
def temporal_training (texts, support=2, confidence = 0.6):
    patts = []
    for text in texts:
        sentences = NLP_sent.sentence_splitting(text, 2)
        for sentencex in sentences:
            #sen=re.split(u'，|；',sentencex)
            sen=re.split(u'，|,|。|：|:|；|;|;',sentencex)
            for sentence in sen:
                if re.search(r'(<TI>[^<>]+</TI>)', sentence):
                    sentence = re.sub(r'(<TI>[^<>]+</TI>)', '<TI>', sentence)
                    #[^<>：；，、“” ]
                    init_num = len(patts)

                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>]{1,4}<TI>)') # XX <TI> XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；.，、“”\*\+（） ]{3}<TI>[^<>]{1,4}<TI>)') # XX <TI> XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>]{1,4}<TI>)') # XX XX <TI> XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') #  <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') #  <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') #  <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ])') #  <TI> XX <TI> XX XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>]{1,4}<TI>)') # XX <TI> XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'(<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX <TI> XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'(<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # <TI> XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'(<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # <TI> XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'(<TI>[^<>]{1,4}<TI>[^<>：；:，、“”\*\+\.（） ])') # <TI> XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile(ur'(<TI>[^<>]{1,4}<TI>)') # <TI> XX <TI>
                    patts.extend(p.findall(sentence))

                    if init_num == len(patts):  

                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{4}<TI>)') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{3}<TI>)') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>[^<>：；:，、“”\*\+\.（） ])') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]{2}<TI>)') # XX XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # XX XX <TI>
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # XX <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # XX <TI>
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>[^<>：；:，、“”\*\+\.（） ])') # XX <TI>
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'([^<>：；:，、“”\*\+\.（） ]<TI>)') # XX <TI>
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'(<TI>[^<>：；:，、“”\*\+\.（） ]{4})') # <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'(<TI>[^<>：；:，、“”\*\+\.（） ]{3})') # <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'(<TI>[^<>：；:，、“”\*\+\.（） ]{2})') # <TI> XX
                        patts.extend(p.findall(sentence))
                        p = re.compile(ur'(<TI>[^<>：；:，、“”\*\+\.（） ])') # <TI> XX
                        patts.extend(p.findall(sentence))






    # remove and clean
    c_patts = {}
    for patt in patts:
        if patt in c_patts:
            c_patts[patt] += 1
        else:
            c_patts[patt] = 1

    for key in c_patts.keys():
        if c_patts[key] < support:
            del c_patts[key]

    #return c_patts



    # match with original text to calculate confidence
    final_patts = {}
    for patt in c_patts:
        rpatt = patt.replace("<TI>", '[^<>]{1,20}')
        #rpatt = patt.replace("<TI>", '[\u4e00-\u9fa5_/\.:""a-zA-Z0-9]{1,20}')
        p = re.compile(rpatt)
        match_num = 0
        for text in texts:
            text = text.replace("<TI>","").replace("</TI>","")
            matches = p.findall(text)
            for match in matches:
                if re.search(r'\d', match):
                    match_num += 1
        #confid = (float)(c_patts[patt]/(float)(match_num+c_patts[patt]+0.001))
        confid = (float)(c_patts[patt]/(float)(match_num+0.001))
        final_patts[patt] = confid

    for key, value in final_patts.items():
        if value < confidence:
            del final_patts[key]
        else:
            for k,v in final_patts.items():
                if (k!=key) and (k in key) and (v == value):
                    del final_patts[key]
                    break
    return final_patts



# test the frequent features on a text file
#not_events=["be", "is", "was", "are","were", "like", "likes"]
def temporal_testing (texts, patts, rep_enable, rep_word, event):
    post_texts = []
    #months = month.split("|")
    for text in texts:
        text=pre.strQ2B(text);
        tagged = text;

        tagged = re.sub(r'(?<!(\d|<|>|/|-))(\d{4}[\.|/|-]\d{1,2}[\.|/|-]\d{1,2})(?!(\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1992/2/2, 1992-2-2
        tagged = re.sub(r'(?<!(\d|<|>|/|-))(\d{4}[-]\d{1,2})(?!(\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1992/2, 1992-2
        tagged = re.sub(r'(?<!(\d|<|>|/))(\d{4}[\.|/]\d{1,2})(?!(\d|<|>|/))', r'<TI>\2</TI>', tagged)
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))(\d{4}[年]\d{1,2}[月]\d{1,2}[日|号])(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) #2014年9月1日
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))(\d{4}[年]\d{1,2}[月])(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) #2014年10月
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))(\d{1,2}[月]\d{1,2}[日|号])(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) #5月26日
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))(\d{4}(年))(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1999年
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))((\d{1,2}[：|:]){1,2}\d{1,2})(?!(\w|\d|<|>|/|-))', r'<STI>\2</STI>', tagged)
        tagged = re.sub(ur'(?<!(\w|\d|<|>|/|-))(\d{1,2}点\d{1,2}分)(?!(\w|\d|<|>|/|-))', r'<STI>\2</STI>', tagged)
        tagged = re.sub(r'(?<!(\w|\d|/))('+rel_time+')(?!(\w|\d|<|>|/))', r'<STI>\2</STI>', tagged)
        tagged = re.sub(r'('+u"[^出|发|表]"+')('+now+')(?!(\w|\d|<|>|/))', r'\1<TI>\2</TI>', tagged) # 目前present, current, ....
        tagged = re.sub(r'(?<!(\w|\d|/))('+rel_dmy+')(?!(\w|\d|/))', r'<TI>\2</TI>', tagged) # 今日yesterday.
        tagged = re.sub(r'(?<!(\w|\d|/))('+weekday+')(?!(\w|\d|/))', r'<TI>\2</TI>', tagged)
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(('+exp1+')\d{1,4}('+u"-"+')\d{1,4}('+dmy+'))(?!(\w|\d|<|>|-))', r'<DTI>\2</DTI>', tagged) #1995-2016年 第3-5天
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{1,2}[\.|/|-]\d{1,2})(?!(\w|\d|<|>|/|-))', r'<CTI>\2</CTI>', tagged) #  11/02
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{4}[/-]\d{4})(?!(\w|\d|<|>|/|-))', r'<CTI>\2</CTI>', tagged) # 1999-2010
        #tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{1,2}[/|-]\d{1,2})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) #  11/02
        #tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{4}[/-]\d{4})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1999-2010

        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+u"[第|每]"+')((('+u"半|一|二|两|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|"+')('+u"[、|,|，]"+')){1,5}('+u"半|一|二|两|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|"+')('+dmy+'))(?!(\w|\d|<|>|/))', r'<DTI>\2\3</DTI>', tagged) #第7、8、14天
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+u"[第|每]"+')(((\d{1,3})('+u"[、|,|，]"+')){1,5}(\d{1,3})('+dmy+'))(?!(\w|\d|<|>|/))', r'<DTI>\2\3</DTI>', tagged) #第7、8、14天
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+u"[第|每]"+')(\d{1,3}('+u"[个|]"+'))('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3\4</TI>', tagged) #第8天  第8年
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+u"[第|每]"+')('+u"半|一|二|两|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五"+')('+u"[个|]"+')('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3\4\5</TI>', tagged)#每三个月
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+exp1+')(\d{1,3})('+u"个|个半|"+')('+ dmy+')('+exp2+')(?!(\w|\d|<|>|/))', r'<DTI>\2\3\4\5\6</DTI>', tagged) # 约10天 30天前
        tagged = re.sub(r'(?<!(\d|<|>|/))('+exp1+')('+u"一|二|两|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|半"+')('+u"个|个半|"+')('+ dmy+')('+exp2+')(?!(\w|\d|<|>|/))', r'<DTI>\2\3\4\5\6</DTI>', tagged)#一月 两个周期
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+exp1+')(\d{1,3})('+u"[余|多]"+')('+ dmy+')('+exp2+')(?!(\w|\d|<|>|/))', r'<DTI>\2\3\4\5\6</DTI>', tagged)#5余年

#复合的常见时间表达式
        while(re.search('<TI>[^<>]+</TI>\s?<STI>[^<>]+</STI>',tagged)):
            tagged = re.sub(r'(<TI>)([^<>]+)(</TI>)(\s?)(<STI>)([^<>]+)(</STI>)', r'<TI>\2\4\6</TI>', tagged)
        while(re.search('<STI>[^<>]+</STI>\s?<STI>[^<>]+</STI>',tagged)):
            tagged = re.sub(r'(<STI>)([^<>]+)(</STI>)(\s?)(<STI>)([^<>]+)(</STI>)', r'<TI>\2\4\6</TI>', tagged)
        #tagged = re.sub(r'(<CTI>)([^<>]+)(</CTI>)(-)(<CTI>)([^<>]+)(</CTI>)', r'<TI>\2</TI>\4<TI>\6</TI>', tagged)
        while(re.search('<TI>[^<>]+</TI>('+u"[,|、]"+')<CTI>[^<>]+</CTI>',tagged)):
            tagged = re.sub(r'(<TI>)([^<>]+)(</TI>)('+u"[,|、]"+')(<CTI>)([^<>]+)(</CTI>)', r'<TI>\2</TI>\4<TI>\6</TI>', tagged)





        # exceptions (will lower F1 score)
        error = "cm|CM|KG|kg|%|mg|mm|°C"
        tagged = re.sub(r'<TI>([^<>]+)</TI>(| )('+error+')', r'\1\2\3', tagged) # remove
        tagged = re.sub(r'<CTI>([^<>]+)</CTI>(| )('+error+')', r'\1\2\3', tagged) # remove

        temp2 = re.sub(r'(<TI>[^<>]+</TI>)', '<TI>', tagged)
        #temp2 = re.sub(r'(<STI>[^<>]+</STI>)', '<STI>', tagged)
        #temps2 = temp2.split(u'。|，|；|：')
        temps2=re.split(u'，|,|。|：|:|；|;|;',temp2)


        for i in xrange(len(temps2)):
            if "<CTI>" in temps2[i]:
                sent=[]
                un_posl,un_posr, un_list = [], [],[]
                pattern=re.compile('(<CTI>[^<>]+</CTI>)')
                un_list=pattern.findall(temps2[i])



                sent = pretreatment.segmenter(temps2[i])
                #for np in xrange(len(sent)-1):
                np=0
                while np<len(sent)-2:
                    if "<" in sent[np]:
                        x=np+1
                        while x<len(sent)and (x+1)<len(sent):
                            pat1 = ''.join(sent[np:x+1])
                            if pat1=='<TI>':
                                sent[np]=pat1
                                i=np+1
                                while i<x+1:
                                    sent.pop(np+1)
                                    i=i+1
                                break
                            if pat1 in un_list:
                                sent[np]="<TI>"
                                un_posl.append(np)
                                i=np+1
                                while i<x+1:
                                    sent.pop(np+1)
                                    i=i+1
                                break
                            x=x+1
                    np = np+1


                #temps2[i] = re.sub(r'(<CTI>[^<>]+</CTI>)', r'<TI>', temps2[i])
                #temps2[i] = re.sub(r'(<TI>)', r' <TI> ', temps2[i])

                num = 0
                while num < len(un_posl):
                    x = un_posl[num]
                    found = False
                    cut_min = max((x-4), 0)
                    cut_max = min((x+4), len(sent))
                    for m in range(cut_min, x):
                        for n in range (cut_max, x, -1):
                            pat = ''.join(sent[m:n])
                            if (pat in patts):
                                found = True
                                break
                        if found:
                            break

                    if found:
                        tagged = tagged.replace(un_list[num], un_list[num].replace('CTI>', 'TI>'))
                    num += 1

        tagged = tagged.replace('<CTI>', '').replace('</CTI>', '') # return back to original form if this not a TI

        while tagged.find("<DTI>") > -1:
            cut_min = max((tagged.find("<DTI>")-20), 0)
            cut_max = min((tagged.find("</DTI>", cut_min)+20), len(tagged))
            sub_str = tagged[cut_min:cut_max].lower()
            tagged = tagged.replace('DTI>', 'TI>', 2)

        while tagged.find("<STI>") > -1:
            cut_min = max((tagged.find("<STI>")-20), 0)
            cut_max = min((tagged.find("</STI>", cut_min)+20), len(tagged))
            sub_str = tagged[cut_min:cut_max].lower()
            tagged = tagged.replace('STI>', 'TI>', 2)

        # combine "the" into annotations
        #tagged = tagged.replace("the <TI>", "<TI>the ")


        if (rep_enable): # replacement
            tagged = re.sub('<TI>[^<>]+</TI>', rep_word, tagged)
            while (rep_word + ' ' + rep_word) in tagged:
                tagged = tagged.replace((rep_word + ' ' + rep_word), rep_word)
        post_texts.append(tagged)

    return post_texts






def using_TimeX3(list):

    sub1,sub2 = "<TI>","</TI>"
    id = 0
    for i in xrange(len(list)):
        input = list[i]
        while input.find(sub1) > -1:
            id += 1

            term = input[input.find(sub1)+len(sub1):input.find(sub2)]

            (type, value) = normalize(term)
            input = re.sub(sub1, "<TIMEX3 tid=\"t" + str(id) + "\" Type=\"" + type + "\" Value=\""+value+"\">", input, 1)
            input = re.sub(sub2, "</TIMEX3>", input, 1);

        list[i] = input

    list.insert(0,"<DOC><DOCNO>Generated by TEXer</DOCNO><DOCTYPE SOURCE=\"Free text\"></DOCTYPE><TEXT>")
    list.append("</TEXT></DOC>")
    return list

def normalize(term):
    type = "" #Date, Time, Duration, Set
    if re.search(r'(' + dmy + ')', term) and re.search(ur'[^第]', term):
        type = "Duration"
    elif re.search(ur'[每]', term):
        type = "Set"
    elif re.search(r'('+now+')', term) or re.search(r'('+rel_dmy+')', term):
        type = "Time"
    else:
        type = "Date"

    '''value = ""
    if type == "Time" or "current" in term:
        value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    elif type == "Date":
        if ("today" in term or "tonight" in term):
            value = str(datetime.date.today())
        elif ("yesterday" in term):
            value = str(datetime.date.today() - datetime.timedelta(days=1))
        elif("tomorrow" in term):
            value = str(datetime.date.today() + datetime.timedelta(days=1))
    if value == "":
        value = term
    '''
    value = term
    return (type,value)

import argparse
def _process_args():
    parser = argparse.ArgumentParser(description='')
   #parser.add_argument('-i', default=r"/Users/hat7002/Documents/programs/CDE_Tony/data/CDE_paper/0 Text formats comparison/10 celigiblitiy.txt", help='input file path')
    parser.add_argument('-i', default=r"D:/TEXer/data_demo_Chinese/training.txt", help='input file path')
    parser.add_argument('-o', default=None, help='output file path; set None when you want use default  path')
    parser.add_argument('-m', default="training", help='select training or testing module')
    parser.add_argument('-ip', default=r"D:/TEXer/data_demo_Chinese/training_pattern.txt", help='input trained pattern file')
    parser.add_argument('-r', action='store_true', default=False, help='True:enable replacement (with a specific word or phrase below)')
    parser.add_argument('-w', default='date', help='the label used to replace temporal expressions')
    parser.add_argument('-e', action='store_true', default=False, help='True:identify events')
    parser.add_argument('-x3', action='store_true', default=False, help='True:enable TimeML TIMEX3 represenation')

    return parser.parse_args(sys.argv[1:])

'''
if __name__ == '__main__' :
    print ''
    args = _process_args()
 # temporal_processing ("D:\TEXer\TEXer_temporal - Copy\data\testing.txt","D:\TEXer\TEXer_temporal - Copy\data\tesing_TEXer.txt","testing",None,False," ",False,False)
    temporal_processing (args.i, args.o, args.m,args.ip, args.r, args.w, args.e, args.x3)
    print ''
'''