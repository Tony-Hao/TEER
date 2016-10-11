# coding=utf-8
# TEXer - An Temporal Expression Extrator
# Author: Tony HAO (haotianyong@gmail.com)
# Refer the paper for details http://link.springer.com/chapter/10.1007%2F978-3-642-39844-5_7
# Please cite the paper if you use the code: 
# Tianyong Hao, Alex Rusanov, Chunhua Weng. Extracting and Normalizing Temporal Expressions in Clinical Data Requests from Researchers. Lecture Notes in Computer Science, Volume 8040, 2013, pp 41-51.


from kernel.NLP import sentence as NLP_sent
import W_utility.file as ufile
from W_utility.log import ext_print
import datetime
import sys, os
import re


# Predefined features
numbers = "first|a|one|second|two|third|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion"
order = "st|nd|rd|th"
dmy = "year|years|day|days|week|weeks|month|months|hour|hours|hrs|minute|minutes|mins|min|seconds" # avoid to use 'second' as it may incur erros, 'a second XX'
month = "january|jan|jan.|february|feb|march|mar|april|apr|may|june|july|august|aug|september|sep|october|oct|november|nov|december|dec|dec."
day = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
rel_day = "today|yesterday|tomorrow|tonight"
exp1 = "since|before|after|earlier|later|ago"
exp2 = "this|last|past|previous|recent|next|following|upcoming|preceding"
now = "current|present|now"
adv = "currently|recently|monthly|daily"
sets = "every|twice"


# contain training and testing modules. set parameters to call different modules.
def temporal_processing (fin, fout = None, type = "testing", fin_t = None, rep_enable = False, rep_word = "", event = False, X3 = False):
    
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
def temporal_training (texts, support=2, confidence = 0.2):
    patts = []
    for text in texts:        
        sentences = NLP_sent.sentence_splitting(text, 2)
        for sentence in sentences:
            if re.search(r'(<TI>[^<>]+</TI>)', sentence):                
                sentence = re.sub(r'(<TI>[^<>]+</TI>)', '<TI>', sentence)

                init_num = len(patts)
                p = re.compile('([^<> ]+ [^<> ]+ <TI>[^<>]{1,20}<TI> [^<> ]+)') # XX XX <TI> XX <TI> XX
                patts.extend(p.findall(sentence))
                p = re.compile('([^<> ]+ [^<> ]+ <TI>[^<>]{1,20}<TI>)') # XX XX <TI> XX <TI>
                patts.extend(p.findall(sentence))
                p = re.compile('([^<> ]+ <TI>[^<>]{1,20}<TI> [^<> ]+)') # XX <TI> XX <TI> XX
                patts.extend(p.findall(sentence))
                p = re.compile('([^<> ]+ <TI>[^<>]{1,20}<TI>)') # XX <TI> XX <TI>
                patts.extend(p.findall(sentence))
                p = re.compile('(<TI>[^<>]{1,20}<TI> [^<> ]+)') # <TI> XX <TI> XX
                patts.extend(p.findall(sentence))
                p = re.compile('(<TI>[^<>]{1,20}<TI>)') # <TI> XX <TI>
                patts.extend(p.findall(sentence))
                
                if init_num == len(patts):  

                    p = re.compile('([^<> ]+ [^<> ]+ <TI> [^<> ]+)') # XX XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile('([^<> ]+ [^<> ]+ <TI>)') # XX XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile('([^<> ]+ <TI> [^<> ]+)') # XX <TI> XX
                    patts.extend(p.findall(sentence))
                    p = re.compile('([^<> ]+ <TI>)') # XX <TI>
                    patts.extend(p.findall(sentence))
                    p = re.compile('(<TI> [^<> ]+)') # <TI> XX
                    patts.extend(p.findall(sentence))
                    
                

    # remove and clean
    c_patts = {}
    for patt in patts:
        if patt in c_patts:
            c_patts[patt] += 1
        else:    
            c_patts[patt] = 1
    '''
    for key in c_patts.keys():
        if c_patts[key] < support:
            del c_patts[key]
    '''

    '''
            
    # match with original text to calculate confidence 
    final_patts = {}
    for patt in c_patts:
        rpatt = patt.replace("<TI>", r'.{1,20}')
        #rpatt = patt.replace("<TI>", r'[^<>]{1,20}')
        p = re.compile(rpatt)
        match_num = 0
        for text in texts:
#            text = text.replace("<TI>","").replace("</TI>","")
            matches = p.findall(text)
            for match in matches:
                if "<TI>" in match or re.search(r'\d', match):
                    match_num += 1
        confid = (float)(c_patts[patt]/(float)(match_num+0.001))
        final_patts[patt] = confid
    
    # remove and clean
    for key in final_patts.keys():
        if final_patts[key] < confidence:
            del final_patts[key]

    # remove and clean
    for key, value in final_patts.items():
        if value < confidence:
            del final_patts[key]
        else:
            for k,v in final_patts.items():
                if (k in key) and (v == value):
                    del final_patts[key]
                    break
                        
    return final_patts
    '''
    return c_patts


from nltk import word_tokenize
from nltk import pos_tag
# test the frequent features on a text file
not_events=["be", "is", "was", "are","were", "like", "likes"]
def temporal_testing (texts, patts, rep_enable, rep_word, event):
    post_texts = []
    months = month.split("|")
    for text in texts:
        tagged = text.lower();
        
        if event:
            words = word_tokenize(tagged)
            poss = pos_tag (words)
            tagged = ""
            for pos in poss:
                if len(pos[0]) > 2 and (pos[1] == "VBD" or pos[1]=="VBN" or pos[1] =="VB") and pos[0] not in not_events:
                    tagged += "<EV>"+pos[0] +"</EV>" + " " 
                else:
                    tagged += pos[0] + " "
            tagged = tagged.strip()

        splitter=re.compile('[^\w\d+<>/.]') 
        for singleWord in splitter.split(tagged): 
            if (singleWord in months):
                tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+r' \d{1,2}( - |-| -|- |/)\d{1,2}(, |,| |/)\d{2,4})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December 1-7, 2003   \2����˼��ƥ��ǰ��ڶ�������
                tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+r'( - |-| -|- | |/)\d{1,2}( , |, |,| |/)\d{1,4})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December 1, 2003
                tagged = re.sub('(?<!(\w|\d|<|>|/))(\d{1,2}( - |-| -|- | |/)'+singleWord+r'( , |, |,| | - |-| -|- |/)\d{1,4})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # 2 December 2003
                tagged = re.sub('(?<!(\w|\d|<|>|/))(\d{1,4}( - |-| -|- | |/)'+singleWord+r'( , |, |,| | - |-| -|- |/)\d{1,2})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # 2003 December 2 
                tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+'( - |-| -|- | |/)\d{1,2}(st|nd|rd|th)(, |,| |/)\d{1,4})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December 1st/2nd/3th, 2003
                tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+'( - |-| -|- | |/)\d{1,2}(st|nd|rd|th))(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December 1st/2nd/3th
                tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+r'( , |, |,| | of | - |-| -|- |/)\d{1,4})(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December, 2003 / December of 2003
                tagged = re.sub('(?<!(\w|\d|<|>|/))(\d{1,4}( , |, |,| | of | - |-| -|- |/)'+singleWord+')(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # 2003 December/ December of 2003
                if (singleWord != "may"):
                    tagged = re.sub('(?<!(\w|\d|<|>|/))('+singleWord+r')(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # December
                    
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{1,4}[/-]\d{1,4}[/-]\d{1,4})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1992/2/2, 1992-2-2
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))((19|20)\d{2}[/-]\d{1,2})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1992/2, 1992-2
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{1,2}[/-](19|20)\d{2})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1992/2, 1992-2
        
        # unsure
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))(\d{1,4}[/-]\d{1,4})(?!(\w|\d|<|>|/|-))', r'<CTI>\2</CTI>', tagged) # 1992/2, 1992-2
        tagged = re.sub(r'(?<!(\w|\d|<|>|/|-))((year|)(19|20)\d{2})(?!(\w|\d|<|>|/|-))', r'<TI>\2</TI>', tagged) # 1999
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(the |)('+ now+') (date|time|'+dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3 \4</TI>', tagged) # present date, current day, ....
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+ now+')(?!(\w|\d|<|>|/))', r'<CTI>\2</CTI>', tagged) # present, current, ....
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+ rel_day+')(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # yesterday.
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+ day+')(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # Friday
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+ adv+')(?!(\w|\d|<|>|/))', r'<TI>\2</TI>', tagged) # currently, monthly, darily
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(\d{1,6} (or|and|to|-|) \d{1,6} ('+ dmy+'))(?!(\w|\d|<|>|/))', r'<DTI>\2</DTI>', tagged) # 5 to 6 years, ....
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))('+sets+') ('+exp2+') (\d{1,6}) ('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2 \3 \4 \5</TI>', tagged) # every 30 days
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(the |)('+exp2+') (\d{1,6}) ('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3 \4 \5</TI>', tagged) # (the) 30 days
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(\d{1,6}) ('+ dmy+')(?!(\w|\d|<|>|/))', r'<DTI>\2 \3</DTI>', tagged) # 30 days
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(the |)('+exp2+') ('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3 \4</TI>', tagged) # next year
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(the |)('+exp2+'|) ('+numbers+') ('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3 \4 \5</TI>', tagged) # three years
        tagged = re.sub(r'(?<!(\w|\d|<|>|/))(the |)('+numbers+') ('+ dmy+')(?!(\w|\d|<|>|/))', r'<TI>\2\3 \4</TI>', tagged) # three years
        
        # exceptions (will lower F1 score)
        error = "cm|CM|KG|kg|%|mg|mm"
        tagged = re.sub(r'<TI>([^<>]+)</TI>(| )('+error+')', r'\1\2\3', tagged) # remove
        tagged = re.sub(r'<CTI>([^<>]+)</CTI>(| )('+error+')', r'\1\2\3', tagged) # remove
 
        
        temp2 = re.sub(r'(<TI>[^<>]+</TI>)', '<TI>', tagged)
        temps2 = temp2.split(' ')
        un_pos, un_list = [], []
        for i in xrange(len(temps2)):
            if "<CTI>" in temps2[i]:
                un_pos.append(i)
                un_list.append(temps2[i])
                temps2[i] = "<TI>"
        
        num = 0
        while num < len(un_pos):
            i = un_pos[num]
            found = False
            cut_min = max((i-4), 0)
            cut_max = min((i+4), len(temps2))
            for m in range(cut_min, i): 
                for n in range (cut_max, i, -1):
                    pat = ' '.join(temps2[m:n])
                    if (pat in patts):
                        found = True
                        break
                if found:
                    break

            if found:
                tagged = tagged.replace(un_list[num], un_list[num].replace('CTI>', 'TI>'))
                if m <= un_pos[max(num-1,0)] and max(num-1,0) != num:
                    tagged = tagged.replace(un_list[max(num-1,0)], un_list[max(num-1,0)].replace('CTI>', 'TI>'))
                if un_pos[min(num+1, len(un_pos)-1)] <= n and min(num+1, len(un_pos)-1) != num:
                    tagged = tagged.replace(un_list[min(num+1, len(un_pos)-1)], un_list[min(num+1, len(un_pos)-1)].replace('CTI>', 'TI>'))   
                    num += 1
            
            num += 1

        tagged = tagged.replace('<CTI>', '').replace('</CTI>', '') # return back to original form if this not a TI
        
        while tagged.find("<DTI>") > -1:
            cut_min = max((tagged.find("<DTI>")-20), 0)
            cut_max = min((tagged.find("</DTI>", cut_min)+20), len(tagged))
            sub_str = tagged[cut_min:cut_max].lower()
            if ("age " in sub_str or " age" in sub_str or "aged " in sub_str or "aging " in sub_str or " old" in sub_str):
                tagged = tagged.replace('<DTI>', '', 1).replace('</DTI>', '', 1)
            else:
                tagged = tagged.replace('DTI>', 'TI>', 2)
                
        # combine "the" into annotations 
        #tagged = tagged.replace("the <TI>", "<TI>the ")
        tagged = re.sub(r' the <TI>('+ now+')(<| )', r' <TI>the \1\2', tagged) # present, current, ....
        tagged = re.sub('<TI>([^<>]+)<TI>', r'<TI>\1', tagged)
        tagged = re.sub('</TI>([^<>]+)</TI>', r'\1</TI>', tagged)

        if (rep_enable): # replacement
            tagged = re.sub('<TI>[^<>]+</TI>', rep_word, tagged)
            while (rep_word + ' ' + rep_word) in tagged:
                tagged = tagged.replace((rep_word + ' ' + rep_word), rep_word)
        post_texts.append(tagged)
        
    return post_texts


#output TimeML TIMEX3 standard 
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
    if re.search(r'(-|to|' + dmy + ')', term):             
        type = "Duration"
    elif re.search(r'('+adv+')', term) or re.search(r'('+sets+')', term):
        type = "Set"
    elif re.search(r'('+now+')', term) or "morning" in term or "night" in term or "evening" in term:
        type = "Time"
    else:
        type = "Date"

    value = ""
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
        
    return (type,value)

# main function    

# processing the command line options
import argparse
def _process_args():
    parser = argparse.ArgumentParser(description='')
   #parser.add_argument('-i', default=r"/Users/hat7002/Documents/programs/CDE_Tony/data/CDE_paper/0 Text formats comparison/10 celigiblitiy.txt", help='input file path')
    parser.add_argument('-i', default=r"D:/TEXer/data_demo_English/testing.txt", help='input file path')
    parser.add_argument('-o', default=None, help='output file path; set None when you want use default  path')
    parser.add_argument('-m', default="testing", help='select training or testing module')
    parser.add_argument('-ip', default=r"D:/TEXer/data_demo_English/training_pattern.txt", help='input trained pattern file')
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
    temporal_processing (args.i, args.o, args.m, args.ip, args.r, args.w, args.e, args.x3)
    print ''
'''