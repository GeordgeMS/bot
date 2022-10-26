#!/usr/bin/ypython
# -*- coding: utf-8 -*-
import time,re,time,random,json,requests,ctypes,multiprocessing
import vk_captchasolver as vc
from threading import Thread
from multiprocessing import Process 
manager = multiprocessing.Manager()
tokens = manager.list([])
with open ("fras.txt") as fras:
 fras=[i.replace('\n','') for i in fras.readlines()]

def nn(peer_id,a,b,idd,typg,shp,sl):
    captcha=''
    time.sleep(sl)
    tg=0
    shp=shp.replace('&#58;',':')
    shp=shp.replace('&#61;','=')
    while b in tokens[a]:
        time.sleep(0.8)
        ms=fras[random.randint(0,len(fras)-1)]
        if typg!='0':
            tg+=1
            if tg>2:
                requests.get(f'https://api.vk.com/method/messages.setActivity?type=typing&peer_id={peer_id}&access_token={tokens[a][0]}&v=5.131')
                tg=0
        if idd!='0':
            ms=shp+' '+idd+' ('+ms+')'
        else:
            ms=shp+' '+ms
        req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={peer_id}&random_id=0&access_token={tokens[a][0]}&v=5.131{captcha}').text)
        if 'error' in req and req['error']['error_code']==14:#error captcha
            captcha=f'&captcha_key={vc.solve(sid=req["error"]["captcha_sid"],s=1)}&captcha_sid={req["error"]["captcha_sid"]}'
    return 0

def timer(a,b,peer,sl,typg,shp,sln):
    captcha=''
    time.sleep(sln*5)
    shp=shp.replace('&#58;',':')
    shp=shp.replace('&#61;','=')
    while b in tokens[a]:
        for u in range(5):
            ms=shp+' '+fras[random.randint(0,len(fras)-1)]
            if typg!='0':
                    for zd in range(0,int(0.2*len(ms)),3):
                            requests.get(f'https://api.vk.com/method/messages.markAsRead?peer_id={peer}&access_token={tokens[a][0]}&v=5.131')
                            requests.get(f'https://api.vk.com/method/messages.setActivity?type=typing&peer_id={peer}&access_token={tokens[a][0]}&v=5.131')
                            time.sleep(3)
            req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={peer}&random_id=0&access_token={tokens[a][0]}&v=5.131{captcha}').text)
            if 'error' in req:
                if req['error']['error_code']==14:#error captcha
                    captcha=f'&captcha_key={vc.solve(sid=req["error"]["captcha_sid"],s=1)}&captcha_sid={req["error"]["captcha_sid"]}'
                else:
                    time.sleep(0.3)
            else:
                break
        time.sleep(sl)
    return 0

def auto(a,b,idd):
    ids=[]
    while len(tokens[a])>b and tokens[a][b].find(idd[0]+'='+idd[1]+'='+idd[2]+'='+idd[3]+'='+idd[4])!=-1:
        tkns=tokens[a][b].split('=')
        time.sleep(int(idd[3]))
        for ii in range(3,len(tkns),2):
            if len(ids)<=int((ii-3)/2):
                ids.append('-1')
            if tkns[ii+1]!=ids[int((ii-3)/2)]:
                ms=fras[random.randint(0,len(fras)-1)]
                if idd[4]!='0':
                    for zd in range(0,int(0.2*len(ms)),3):
                            requests.get(f'https://api.vk.com/method/messages.markAsRead?peer_id={tkns[ii]}&access_token={tokens[a][0]}&v=5.131')
                            requests.get(f'https://api.vk.com/method/messages.setActivity?type=typing&peer_id={tkns[ii]}&access_token={tokens[a][0]}&v=5.131')
                            time.sleep(3)
                captcha=''
                for te in range(3):
                    req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={tkns[ii]}&reply_to={tkns[ii+1]}&random_id=0&access_token={tokens[a][0]}&v=5.131{captcha}').text)
                    if 'error' in req and req['error']['error_code']==14:#error captcha
                        captcha=f'&captcha_key={vc.solve(sid=req["error"]["captcha_sid"],s=1)}&captcha_sid={req["error"]["captcha_sid"]}'
                    else:
                        break
                ids[int((ii-3)/2)]=tkns[ii+1]
    return 0

def chktokens():
    global tokens
    while True:
        time.sleep(1)
        with open("settings") as file:
          file=file.readlines()
        if tokens!=file:
            file=file[len(tokens):]
            for tk in range(len(file)):
                tokens.extend([re.sub("^\s+|\n|\r|\s+$", '', file[tk]).split(':')])
                Process(target=strt,args=(tk,)).start()
def strt(a):
        global tokens
        ser=json.loads(requests.get(f'https://api.vk.com/method/messages.getLongPollServer?access_token={tokens[a][0]}&v=5.131').text)
        myid=json.loads(requests.get(f'https://api.vk.com/method/users.get?access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
        print(myid)
        print('start')
        for jj in range(len(tokens[a][1:])):
            jj1=tokens[a][1:][jj].replace('\n','').split("=")
            qq=0
            if jj1[0]=='2':
                for q in range(int(jj1[3])):
                    Process(target=nn,args=(jj1[1],a,'='.join(jj1[:6]),jj1[2],jj1[4],jj1[5],q,)).start()
            elif jj1[0]=='3' and jj1[2]!='0':
                Process(target=auto,args=(a,jj+1,['3',jj1[1],jj1[2],jj1[3],jj1[4]])).start()
            elif jj1[0]=='4':
                Process(target=timer,args=(a,'4='+jj1[1]+'='+jj1[2]+'='+jj1[3]+'='+jj1[4]+'='+jj1[5],jj1[1],int(jj1[2]),jj1[3],jj1[4],qq,)).start()
                qq+=1
        while True:
            try:
                event=json.loads(requests.get(f'https://{ser["response"]["server"]}?act=a_check&key={ser["response"]["key"]}&ts={ser["response"]["ts"]}&wait=25&mode=2&version=3').text)
                print(event)
                if 'failed' in event:
                    ser=json.loads(requests.get(f'https://api.vk.com/method/messages.getLongPollServer?access_token={tokens[a][0]}&v=5.131').text)
                if 'updates' in event:
                    ser['response']['ts']=event['ts']
                    for upd in event['updates']:
                        if upd[0]==4 and ((len(upd)>6 and 'from' in upd[6] and int(upd[6]['from'])==myid) or ((3<len(upd)<=6 or 'from' not in upd[6]) and upd[2]>1)):
                          if '1' in tokens[a]:
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                          if len(upd)>=6:
                            mess = upd[5].split(' ')
                            if mess[0].lower()=='+д':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                with open("settings") as text:
                                    text=text.readlines() 
                                if text[a].find(tokens[a][0])!=-1:
                                    if not '1' in tokens[a]:
                                        text[a]+=':1\n'
                                        tokens[a].append('1')
                                    with open("settings", "w+") as file1:
                                            file1.write(''.join(text))
                            elif mess[0].lower()=='+с':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Используйте +с [скорость(макс 4)] (id|домен|реплай/либо 0) (иная цель, id чата, либо 0 для выбора текущего чата) (1-вкл тайпинг,0-выкл(по умолчанию)) (шапка, можно не указывать), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    with open("settings") as text:
                                        text=text.readlines() 
                                    bb=1
                                    if int(mess[1])>4:
                                        bb=4
                                    elif int(mess[1])>0:
                                        bb=int(mess[1])
                                    up=0
                                    if len(upd)>=8 and 'reply' in upd[7]:
                                        if 'marked_users' in upd[6]:
                                            up = str(upd[6]['marked_users'][0][1][0])
                                        else:
                                            up = str(upd[3])
                                        mess.insert(2,str(up))
                                    else:
                                        if len(mess)>2 and mess[2]!='0':
                                            try:
                                                if int(mess[2])>0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up='@id'+str(up['response'][0]['id'])
                                                    else:
                                                        up=0
                                                elif int(mess[2])<0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up='@club'+str(up['response'][0]['id'])
                                                    else:
                                                        up=0
                                            except:
                                                up=0
                                    perid=upd[3]
                                    if len(mess)>3 and mess[3]!='0':
                                        try
                                            perid=str(int(mess[4])+2000000000)
                                        except:
                                            pass
                                    typg="0"
                                    if len(mess)>4 and mess[4]!='0':
                                        typg='1'
                                    shp=''
                                    if len(mess)>5:
                                        shp=' '.join(mess[5:])
                                        shp=shp.replace(':','&#58;')
                                        shp=shp.replace('=','&#61;')
                                    try:
                                            if not '2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp in tokens[a]:
                                                tkns1=tokens[a]
                                                tkns1.append('2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp)
                                                tokens[a]=tkns1
                                                text[a]=text[a].replace('\n','')+':2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp+'\n'
                                                with open("settings", "w+") as file1:
                                                    file1.write(''.join(text))
                                                for q in range(bb):
                                                    Process(target=nn,args=(perid,a,'2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp,up,typg,shp,q,)).start()
                                    except BaseException as e:
                                            print(e)
                                            requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='-с':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                up=0
                                if len(upd)>=8 and 'reply' in upd[7]:
                                        if 'marked_users' in upd[6]:
                                            up = str(upd[6]['marked_users'][0][1][0])
                                        else:
                                            up = str(upd[3])
                                        mess.insert(1,str(up))
                                else:
                                    if len(mess)>1:
                                            try:
                                                if int(mess[1])>0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up=up['response'][0]['id']
                                                    else:
                                                        up=0
                                                elif int(mess[1])<0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up='-'+str(up['response'][0]['id'])
                                                    else:
                                                        up=0
                                            except:
                                                up=0
                                                    pass 
                                perid=upd[3]
                                if len(mess)>2 and mess[2]!='0':
                                    try
                                        perid=str(int(mess[2])+2000000000)
                                    except:
                                        pass
                                with open("settings") as text:
                                        text=text.readlines()
                                if len(mess)==2 and mess[1]=='all':
                                    tokens[a]=[i for i in tokens[a] if i.find('2=')==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==1:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+perid==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                else:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+perid+'='+str(up))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                            elif mess[0].lower()=='+а':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                with open("settings") as text:
                                    text=text.readlines() 
                                up=0
                                if len(upd)>=8 and 'reply' in upd[7]:
                                        if 'marked_users' in upd[6]:
                                            up = str(upd[6]['marked_users'][0][1][0])
                                        else:
                                            up = str(upd[3])
                                        mess.insert(1,str(up))
                                else:
                                    if len(mess)>1 and mess[1]!='0':
                                            try:
                                                if int(mess[1])>0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up=up['response'][0]['id']
                                                    else:
                                                        up=0
                                                elif int(mess[1])<0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up='-'+str(up['response'][0]['id'])
                                                    else:
                                                        up=0
                                            except:
                                                up=0
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Используйте +а [id|домен|реплай/либо 0 для выбора всех id] (задержка(с)) (id чата, либо 0 для выбора всех чатов) (1-вкл тайпинг,0-выкл(по умолчанию)), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    zd=0
                                    if len(mess)>2:
                                        zd=int(mess[2])
                                    perid='0'
                                    if len(mess)>3 and mess[3]!='0':
                                        try
                                            perid=str(int(mess[4])+2000000000)
                                        except:
                                            pass
                                    typg='0'
                                    if len(mess)>4 and mess[4]!='0':
                                        typg='1'
                                    if text[a].find(':3='+str(up)+'='+perid+'='+str(zd)+'='+typg)==-1:
                                                text[a]=text[a].replace('\n','')+':3='+str(up)+'='+perid+'='+str(zd)+'='+typg+'\n'
                                                tkns1=tokens[a]
                                                tkns1.append('3='+str(up)+'='+perid+'='+str(zd)+'='+typg)
                                                tokens[a]=tkns1
                                                with open("settings", "w+") as file1:
                                                    file1.write(''.join(text))
                                                if zd!=0:
                                                    Process(target=auto,args=(a,len(tokens[a])-1,['3',str(up),perid,str(zd),typg])).start()
                            elif mess[0].lower()=='-а':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                up=0
                                if len(upd)>=8 and 'reply' in upd[7]:
                                    if 'marked_users' in upd[6]:
                                        up = str(upd[6]['marked_users'][0][1][0])
                                    else:
                                        up = str(upd[3])
                                    mess.insert(1,str(up))
                                else:
                                    if len(mess)>1:
                                            try:
                                                if int(mess[1])>0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up=up['response'][0]['id']
                                                    else:
                                                        up=0
                                                elif int(mess[1])<0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if not 'error' in up:
                                                        up='-'+str(up['response'][0]['id'])
                                                    else:
                                                        up=0
                                            except:
                                                up=0
                                perid=upd[3]
                                if len(mess)>2 and mess[2]!='0':
                                    try
                                        perid=str(int(mess[2])+2000000000)
                                    except:
                                        pass
                                with open("settings") as text:
                                        text=text.readlines() 
                                if len(mess)==2 and mess[1]=='all':
                                    tokens[a]=[i for i in tokens[a] if i.find('3=')==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==2:
                                    tokens[a]=[i for i in tokens[a] if i.find('3='+str(up))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)>2:
                                    tokens[a]=[i for i in tokens[a] if i.find('3='+str(up)+'='+perid)==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==1:
                                    tokens[a]=[i for i in tokens[a] if i.find('3=')==-1 and i.find(perid)==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                            elif mess[0].lower()=='+т':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Используйте +т [время(сек)] (id чата/чатов,через запятую,0-выбрать текущий чат) (тайпинг 0-выкл,1-вкл) (шапка), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    with open("settings") as text:
                                        text=text.readlines() 
                                    shp=''
                                    if len(mess)>4:
                                        shp=' '.join(mess[4:])
                                        shp=shp.replace(':','&#58;')
                                        shp=shp.replace('=','&#61;')
                                    perid=[upd[3]]
                                    if len(mess)>2 and mess[2]!='0':
                                        try
                                            perid=[str(int(i)+2000000000) for i in mess[2].split(',')]
                                        except:
                                            pass
                                    typg='0'
                                    if len(mess)>3 and mess[3]!='0':
                                        typg='1'
                                    for jk in range(len(perid)):
                                        try:
                                            if not '4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp in tokens[a]:
                                                tkns1=tokens[a]
                                                tkns1.append('4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp)
                                                tokens[a]=tkns1
                                                text[a]=text[a].replace('\n','')+'4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp+'\n'
                                                with open("settings", "w+") as file1:
                                                    file1.write(''.join(text))
                                                Process(target=timer,args=(a,perid[jk]+'='+mess[1]+'='+typg+'='+shp,perid[jk],int(mess[1]),typg,shp,jk,)).start()
                                        except BaseException as e:
                                            print(e)
                                            requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='-т':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                with open("settings") as text:
                                        text=text.readlines()
                                if len(mess)==2 and mess[1]=='all':
                                    tokens[a]=[i for i in tokens[a] if i.find('4=')==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==1:
                                    tokens[a]=[i for i in tokens[a] if i.find('4='+str(upd[3]))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                else:
                                    tokens[a]=[i for i in tokens[a] if i.find('4='+str(mess[1]))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                            elif mess[0].lower()=='+и':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)>1:
                                    for h in range(0,int(mess[1]),18):
                                        if h>0:
                                            time.sleep(1)
                                        requs={"code":'var count='+mess[1]+';if (count>='+str(h)+'+18){count=18;}else{count=count-'+str(h)+';}var r=API.messages.getDialogs({"count":count,"offset":'+str(h)+'}),b="";if ((r) and (r.items.length>0)){ var a=0; while (a!=r.items.length){ var cht="",tit=""; if (r.items[a].message.chat_id!=null){ cht=r.items[a].message.chat_id;tit=r.items[a].message.title;}else if (r.items[a].message.user_id>0){cht=r.items[a].message.user_id; tit=API.users.get({"user_ids":cht}); tit=tit[0].first_name+" "+tit[0].last_name;}else if (r.items[a].message.user_id<0){cht=r.items[a].message.user_id;tit=API.groups.getById({"group_ids":-1*cht}); tit=tit[0].name;} b=b+"id чата: "+cht+", название чата: "+tit+"\\n"; a=a+1;}}else{b=0;} return b;',
                                            "v":"5.131", 
                                            "access_token":tokens[a][0]}
                                        itg=json.loads(requests.post('https://api.vk.com/method/execute',params=r).text)
                                        if 'response' in itg:
                                            if itg["response"]==0:
                                                break
                                            requs={"peer_id":upd[3],
                                            "random_id":0,
                                            "v":"5.131",
                                            "access_token":tokens[a][0],
                                            "message":itg["response"]}
                                            requests.post("https://api.vk.com/method/messages.send",params=requs)
                                        else:
                                            requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                        if h>50:
                                            break
                                elif (len(upd)>6 and 'from' in upd[6]):
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/messages.getChat?chat_id={str(int(upd[3])-2000000000)}&access_token={tokens[a][0]}&v=5.131'))
                                    if 'response' in requs:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=id этого чата: {(int(upd[3])-2000000000)},название чата: {requs["response"][0]["title"]}&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                elif len(upd)>3 and int(upd[3])>0:
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={upd[3]}&access_token={tokens[a][0]}&v=5.131'))
                                    if not 'error' in requs:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=id этого чата: {upd[3]},название чата: {requs[0]["first_name"]} {requs[0]["last_name"]}&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                elif len(upd)>3 and int(upd[3])<0:
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={upd[3]}&access_token={tokens[a][0]}&v=5.131'))
                                    if not 'error' in requs:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=id этого чата: {upd[3]},название чата: {requs[0]["name"]}&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                        elif upd[0]==4:
                            usr_id=None
                            if len(upd)>6 and 'from' in upd[6]:
                                usr_id=str(upd[6]['from'])
                            elif len(upd)>2 and str(upd[2])=='1':
                                usr_id=str(upd[3])
                            if usr_id!=None:
                                perid=':'.join(tokens[a])
                                perid1=[perid.find(i) for i in ['3=0','3='+str(usr_id)] if perid.find(i)!=-1]
                                if len(perid1)>0:
                                        tkns1=tokens[a]
                                        tp=tkns1.index(perid[perid1[0]:].split(':')[0])
                                        tkns1[tp]=tkns1[tp].split('=')
                                        if tkns1[tp][2]=='0' or tkns1[tp][2]==str(upd[3]):
                                            if int(tkns1[tp][3])==0:
                                                ms=fras[random.randint(0,len(fras)-1)]
                                                captcha=''
                                                if tkns1[tp][4]!='0':
                                                    requests.get(f'https://api.vk.com/method/messages.setActivity?type=typing&peer_id={upd[3]}&access_token={tokens[a][0]}&v=5.131')
                                                for te in range(3):
                                                        req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={upd[3]}&reply_to={upd[1]}&random_id=0&access_token={tokens[a][0]}&v=5.131{captcha}').text)
                                                        if 'error' in req and req['error']['error_code']==14:#error captcha
                                                            captcha=f'&captcha_key={vc.solve(sid=req["error"]["captcha_sid"],s=1)}&captcha_sid={req["error"]["captcha_sid"]}'
                                                        else:
                                                            break
                                            else:
                                                try:
                                                    tkns1[tp][tkns1[tp].index(str(upd[3]),3)+1]=str(upd[1])
                                                except:
                                                    tkns1[tp].extend([str(upd[3]),str(upd[1])])
                                                tkns1[tp]='='.join(tkns1[tp])
                                                tokens[a]=tkns1
                    #peer_id = event.obj['message']['peer_id']
                    # psmt=mess.split(' ')
            except BaseException as e:
                print(e)
                time.sleep(100)
                print(f'Ошибка, токен-{str(tokens[a][0])}')
                break

if __name__ == "__main__":
    thread = Thread(target=chktokens)
    thread.start()
