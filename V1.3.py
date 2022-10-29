#!/usr/bin/ypython
# -*- coding: utf-8 -*-
import time,re,time,random,json,requests,ctypes,multiprocessing
import vk_captchasolver as vc
from threading import Thread
from multiprocessing import Process 
manager = multiprocessing.Manager()
tokens = manager.list([])
prcess=manager.list([0])
with open ("fras.txt") as fras:
 fras=[i.replace('\n','') for i in fras.readlines()]

def nn(peer_id,a,b,idd,typg,shp,sl):
    captcha=''
    time.sleep(sl)
    tg=0
    shp=shp.replace('&#58;',':')
    shp=shp.replace('&#61;','=')
    while len(tokens)>a and  b in tokens[a]:
      try:
        time.sleep(0.3)
        ms=fras[random.randint(0,len(fras)-1)]
        if typg!='0' and sl==0:
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
      except:
          pass
    prcess[a+1]-=1
    return 0

def timer(a,b,peer,sl,typg,shp,sln):
    captcha=''
    time.sleep(sln*5)
    shp=shp.replace('&#58;',':')
    shp=shp.replace('&#61;','=')
    while len(tokens)>a and b in tokens[a]:
      try:
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
      except:
          pass
    prcess[a+1]-=1
    return 0

def auto(a,b,idd):
    ids=[]
    while len(tokens)>a and len(tokens[a])>b and tokens[a][b].find(idd[0]+'='+idd[1]+'='+idd[2]+'='+idd[3]+'='+idd[4])!=-1:
      try:
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
      except:
          pass
    prcess[a+1]-=1
    return 0

def chktokens():
    global tokens
    while True:
        time.sleep(5)
        with open("settings") as file:
          file=[re.sub("^\s+|\n|\r|\s+$", '', i).split(':') for i in file.readlines()]
        if [i[0] for i in tokens]!=[i[0] for i in file]:
            a=0
            while a<len(tokens) or a<len(file):
                if len(tokens)>a and ''.join(file).find(tokens[a])==-1:
                    tkns1=tokens
                    del tkns1[a]
                    tokens=tkns1
                    tkns1=prcess
                    del tkns1[a+1]
                    prcess=tkns1
                if len(file)>a and ''.join(tokens).find(file[a])==-1:
                    tokens.append(file[a])
                    Process(target=strt,args=(a,file[a][0],)).start()
                    prcess.append(0)
                a+=1
def strt(a,b):
        global tokens
        ser=json.loads(requests.get(f'https://api.vk.com/method/messages.getLongPollServer?access_token={tokens[a][0]}&v=5.131').text)
        myid=json.loads(requests.get(f'https://api.vk.com/method/users.get?access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
        print(myid)
        print('start')
        qq=0
        for jj in range(len(tokens[a][1:])):
            jj1=tokens[a][1:][jj].replace('\n','').split("=")
            if jj1[0]=='2':
                prcess[a+1]+=int(jj1[3])
                for q in range(int(jj1[3])):
                        Process(target=nn,args=(jj1[1],a,'='.join(jj1[:6]),jj1[2],jj1[4],jj1[5],q,)).start()
            elif jj1[0]=='3' and jj1[2]!='0':
                prcess[a+1]+=1
                Process(target=auto,args=(a,jj+1,['3',jj1[1],jj1[2],jj1[3],jj1[4]])).start()
            elif jj1[0]=='4':
                prcess[a+1]+=1
                Process(target=timer,args=(a,'4='+jj1[1]+'='+jj1[2]+'='+jj1[3]+'='+jj1[4],jj1[1],int(jj1[2]),jj1[3],jj1[4],qq,)).start()
                qq+=1
        while len(tokens)>a and tokens[a]==b:
            try:
                event=json.loads(requests.get(f'https://{ser["response"]["server"]}?act=a_check&key={ser["response"]["key"]}&ts={ser["response"]["ts"]}&wait=25&mode=2&version=3').text)
                print(event)
                if 'failed' in event:
                    ser=json.loads(requests.get(f'https://api.vk.com/method/messages.getLongPollServer?access_token={tokens[a][0]}&v=5.131').text)
                if 'updates' in event:
                    ser['response']['ts']=event['ts']
                    for upd in event['updates']:
                        if len(upd)>6 and upd[0]==4 and (('from' in upd[6] and int(upd[6]['from'])==myid) or ('from' not in upd[6] and upd[2]>1)):
                          if '1' in tokens[a]:
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                          if 1<len(upd[5])<=100:
                            mess = upd[5]
                            mess=mess.replace(':','&#58;')
                            mess=mess.replace('=','&#61;')
                            mess=mess.split(' ')
                            if mess[0].lower()=='+д':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                with open("settings") as text:
                                    text=text.readlines() 
                                if text[a].find(tokens[a][0])!=-1:
                                    if not '1' in tokens[a]:
                                        text[a]+=':1\n'
                                        tokens[a].append('1')
                                    while prcess[0]==1:
                                        pass
                                    prcess[0]=1
                                    with open("settings", "w+") as file1:
                                            file1.write(''.join(text))
                                    prcess[0]=0
                            elif mess[0].lower()=='+с':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Используйте +с [скорость(макс 4)] (id|домен|реплай/либо 0) (иная цель, id чата, либо 0 для выбора текущего чата) (1-вкл тайпинг,0-выкл(по умолчанию)) (шапка, можно не указывать), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
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
                                        if int(up)>0:
                                                up='@id'+up
                                        elif int(up)<0:
                                                up='@club'+up[1:]
                                        mess.insert(2,str(up))
                                    else:
                                        if len(mess)>2 and mess[2]!='0':
                                            try:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if 'response' in up:
                                                        up='@id'+str(up['response'][0]['id'])
                                                    else:
                                                        up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up.replace("-",'')}&access_token={tokens[a][0]}&v=5.131').text)
                                                        if 'response' in up:
                                                            up='@club'+str(up['response'][0]['id'])
                                                        else:
                                                            up=0
                                            except:
                                                up=0
                                    perid=str(upd[3])
                                    if len(mess)>3 and mess[3]!='0':
                                        try:
                                          if mess[4].find('c')!=-1:
                                            perid=str(int(mess[4][1:])+2000000000)
                                          else:
                                            perid=mess[4]
                                        except:
                                            pass
                                    typg="0"
                                    if len(mess)>4 and mess[4]!='0':
                                        typg='1'
                                    shp=''
                                    if len(mess)>5:
                                        shp=' '.join(mess[5:])
                                    try:
                                            if not '2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp in tokens[a] and prcess[a+1]+bb<70:
                                                prcess[a+1]+=bb
                                                tkns1=tokens[a]
                                                tkns1.append('2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp)
                                                tokens[a]=tkns1
                                                text[a]=text[a].replace('\n','')+':2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp+'\n'
                                                while prcess[0]==1:
                                                    pass
                                                prcess[0]=1
                                                with open("settings", "w+") as file1:
                                                    file1.write(''.join(text))
                                                prcess[0]=0
                                                for q in range(bb):
                                                    Process(target=nn,args=(perid,a,'2='+perid+'='+str(up)+'='+str(bb)+'='+typg+'='+shp,str(up),typg,shp,q,)).start()
                                            elif prcess[a+1]+bb>=70:
                                                requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка, слишком много действий на аккаунте!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                    except BaseException as e:
                                            print(e)
                                            requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='-с':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                up=0
                                if len(upd)>=8 and 'reply' in upd[7]:
                                        if 'marked_users' in upd[6]:
                                            up = str(upd[6]['marked_users'][0][1][0])
                                        else:
                                            up = str(upd[3])
                                        if int(up)>0:
                                                up='@id'+up
                                        elif int(up)<0:
                                                up='@club'+up[1:]
                                        mess.insert(1,str(up))
                                else:
                                    if len(mess)>1:
                                            try:
                                                if int(mess[1])>0:
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if 'response' in up:
                                                        up='@id'+str(up['response'][0]['id'])
                                                    else:
                                                        up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up.replace("-",'')}&access_token={tokens[a][0]}&v=5.131').text)
                                                        if 'response' in up:
                                                            up='@club'+str(up['response'][0]['id'])
                                                        else:
                                                            up=0
                                            except:
                                                up=0 
                                perid=str(upd[3])
                                if len(mess)>2 and mess[2]!='0':
                                    try:
                                      if mess[4].find('c')!=-1:
                                        perid=str(int(mess[2][1:])+2000000000)
                                      else:
                                        perid=mess[2]
                                    except:
                                        pass
                                with open("settings") as text:
                                        text=text.readlines()
                                if len(mess)==2 and mess[1]=='all':
                                    tokens[a]=[i for i in tokens[a] if i.find('2=')==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==1:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+perid)==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                else:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+perid+'='+str(up))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                while prcess[0]==1:
                                        pass
                                prcess[0]=1
                                with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                                prcess[0]=0
                            elif mess[0].lower()=='+а':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
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
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if 'response' in up:
                                                        up=str(up['response'][0]['id'])
                                                    else:
                                                        up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up.replace("-",'')}&access_token={tokens[a][0]}&v=5.131').text)
                                                        if 'response' in up:
                                                            up='-'+str(up['response'][0]['id'])
                                                        else:
                                                            up=0
                                            except:
                                                up=0
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Используйте +а [id|домен|реплай/либо 0 для выбора всех id] (задержка(с)) (id чата, либо 0 для выбора всех чатов) (1-вкл тайпинг,0-выкл(по умолчанию)), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    zd=0
                                    if len(mess)>2:
                                        zd=int(mess[2])
                                    perid='0'
                                    if len(mess)>3 and mess[3]!='0':
                                        try:
                                          if mess[4].find('c')!=-1:
                                            perid=str(int(mess[4])+2000000000)
                                          else:
                                            perid=mess[4]
                                        except:
                                            pass
                                    typg='0'
                                    if len(mess)>4 and mess[4]!='0':
                                        typg='1'
                                    if text[a].find(':3='+str(up)+'='+perid+'='+str(zd)+'='+typg)==-1 and prcess[a+1]+1<70:
                                                prcess[a+1]+=1
                                                text[a]=text[a].replace('\n','')+':3='+str(up)+'='+perid+'='+str(zd)+'='+typg+'\n'
                                                tkns1=tokens[a]
                                                tkns1.append('3='+str(up)+'='+perid+'='+str(zd)+'='+typg)
                                                tokens[a]=tkns1
                                                while prcess[0]==1:
                                                    pass
                                                prcess[0]=1
                                                with open("settings", "w+") as file1:
                                                    file1.write(''.join(text))
                                                prcess[0]=0
                                                if zd!=0:
                                                    Process(target=auto,args=(a,len(tokens[a])-1,['3',str(up),perid,str(zd),typg])).start()
                                    elif prcess[a+1]+1>=70:
                                                requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка, слишком много действий на аккаунте!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='-а':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
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
                                                    up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                                    up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)
                                                    if 'response' in up:
                                                        up=str(up['response'][0]['id'])
                                                    else:
                                                        up=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={up.replace("-",'')}&access_token={tokens[a][0]}&v=5.131').text)
                                                        if 'response' in up:
                                                            up='-'+str(up['response'][0]['id'])
                                                        else:
                                                            up=0
                                            except:
                                                up=0
                                perid=str(upd[3])
                                if len(mess)>2 and mess[2]!='0':
                                    try:
                                      if mess[2].find('c')!=-1:
                                        perid=str(int(mess[2])+2000000000)
                                      else:
                                        perid=mess[2]
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
                                while prcess[0]==1:
                                        pass
                                prcess[0]=1
                                with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                                prcess[0]=0
                            elif mess[0].lower()=='+т':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Используйте +т [время(сек)] (id чата/чатов,через запятую,0-выбрать текущий чат) (тайпинг 0-выкл,1-вкл) (шапка), если следующие части команды не нужны, можно не указывать их как 0!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    with open("settings") as text:
                                        text=text.readlines() 
                                    shp=''
                                    if len(mess)>4:
                                        shp=' '.join(mess[4:])
                                    perid=[str(upd[3])]
                                    if len(mess)>2 and mess[2]!='0':
                                        try:
                                            perid=[str(int(i[1:])+2000000000) if i.find('c')!=-1 else i for i in mess[2].split(',')]
                                        except:
                                            pass
                                    typg='0'
                                    if len(mess)>3 and mess[3]!='0':
                                        typg='1'
                                    if prcess[a+1]+len(perid)<70:
                                        prcess[a+1]+=len(perid)
                                        for jk in range(len(perid)):
                                            try:
                                                if not '4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp in tokens[a]:
                                                    tkns1=tokens[a]
                                                    tkns1.append('4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp)
                                                    tokens[a]=tkns1
                                                    text[a]=text[a].replace('\n','')+':4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp+'\n'
                                                    while prcess[0]==1:
                                                        pass
                                                    prcess[0]=1
                                                    with open("settings", "w+") as file1:
                                                        file1.write(''.join(text))
                                                    prcess[0]=0
                                                    Process(target=timer,args=(a,'4='+perid[jk]+'='+mess[1]+'='+typg+'='+shp,perid[jk],int(mess[1]),typg,shp,jk,)).start()
                                            except BaseException as e:
                                                print(e)
                                                requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                    elif prcess[a+1]+len(perid)>=70:
                                                requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка, слишком много действий на аккаунте!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='-т':
                                try:
                                    requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                    with open("settings") as text:
                                            text=text.readlines()
                                    if len(mess)==2 and mess[1]=='all':
                                        tokens[a]=[i for i in tokens[a] if i.find('4=')==-1]
                                        text[a]=':'.join(tokens[a])+'\n'
                                    elif len(mess)==1:
                                        tokens[a]=[i for i in tokens[a] if i.find('4='+str(upd[3]))==-1]
                                        text[a]=':'.join(tokens[a])+'\n'
                                    else:
                                        perid=[str(int(i[1:])+2000000000) if i.find('c')!=-1 else i for i in mess[1].split(',')]
                                        for x in perid:
                                          tokens[a]=[i for i in tokens[a] if i.find('4='+x)==-1]
                                        text[a]=':'.join(tokens[a])+'\n'
                                    while prcess[0]==1:
                                        pass
                                    prcess[0]=1
                                    with open("settings", "w+") as file1:
                                            file1.write(''.join(text))
                                    prcess[0]=0
                                except BaseException as e:
                                    print(e)
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                            elif mess[0].lower()=='+и':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={str(upd[3])}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)>1:
                                    for h in range(0,int(mess[1]),18):
                                        if h>0:
                                            time.sleep(1)
                                        requs={"code":'var count='+mess[1]+';if (count>='+str(h)+'+18){count=18;}else{count=count-'+str(h)+';}var r=API.messages.getDialogs({"count":count,"offset":'+str(h)+'}),b="";if ((r!=null) && (r.items.length>0)){ var a=0; while (a!=r.items.length){ var cht="",tit=""; if (r.items[a].message.chat_id!=null){ cht="c"+r.items[a].message.chat_id;tit=r.items[a].message.title;}else if (r.items[a].message.user_id>0){cht=r.items[a].message.user_id; tit=API.users.get({"user_ids":cht}); tit=tit[0].first_name+" "+tit[0].last_name;}else if (r.items[a].message.user_id<0){cht=r.items[a].message.user_id;tit=API.groups.getById({"group_ids":-1*cht}); tit=tit[0].name;} b=b+"id чата: "+cht+" , название чата: "+tit+"\\n"; a=a+1;}}else{b=0;} return b;',
                                            "v":"5.131", 
                                            "access_token":tokens[a][0]}
                                        itg=json.loads(requests.post('https://api.vk.com/method/execute',params=requs).text)
                                        print(itg)
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
                                            requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                        if h>50:
                                            break
                                elif (len(upd)>6 and 'from' in upd[6]):
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/messages.getChat?chat_id={str(int(upd[3])-2000000000)}&access_token={tokens[a][0]}&v=5.131').text)
                                    if 'response' in requs:
                                        requs={"peer_id":upd[3],
                                               "v":"5.131",
                                               "random_id":0,
                                               "access_token":tokens[a][0],
                                               "message":'id этого чата: c'+str(int(upd[3])-2000000000)+' ,название чата: '+requs["response"]["title"]}
                                        requests.post("https://api.vk.com/method/messages.send",params=requs)
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                elif len(upd)>3 and int(upd[3])>0:
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={str(upd[3])}&access_token={tokens[a][0]}&v=5.131').text)
                                    if 'response' in requs:
                                        requs={"peer_id":upd[3],
                                               "random_id":0,
                                               "v":"5.131",
                                               "access_token":tokens[a][0],
                                               "message":'id этого чата: '+str(upd[3])+' ,название чата: '+requs["response"][0]["first_name"]+' '+requs["response"][0]["last_name"]}
                                        requests.post("https://api.vk.com/method/messages.send",params=requs)
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                elif len(upd)>3 and int(upd[3])<0:
                                    requs=json.loads(requests.get(f'https://api.vk.com/method/groups.getById?group_ids={str(upd[3])[1:]}&access_token={tokens[a][0]}&v=5.131').text)
                                    if 'response' in requs:
                                        requs={"peer_id":upd[3],
                                               "random_id":0,
                                               "v":"5.131",
                                               "access_token":tokens[a][0],
                                               "message":'id этого чата:'+str(upd[3])+' ,название чата: '+requs["response"][0]["name"]}
                                        requests.post("https://api.vk.com/method/messages.send",params=requs)
                                    else:
                                        requests.get(f'https://api.vk.com/method/messages.send?peer_id={str(upd[3])}&message=Ошибка!&random_id=0&access_token={tokens[a][0]}&v=5.131')
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
                                                    requests.get(f'https://api.vk.com/method/messages.setActivity?type=typing&peer_id={str(upd[3])}&access_token={tokens[a][0]}&v=5.131')
                                                for te in range(3):
                                                        req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={str(upd[3])}&reply_to={upd[1]}&random_id=0&access_token={tokens[a][0]}&v=5.131{captcha}').text)
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
                        print(prcess)
            except BaseException as e:
                print(e)
                print(f'Ошибка, токен-{str(tokens[a][0])}')
        return 0

if __name__ == "__main__":
    thread = Thread(target=chktokens)
    thread.start()
