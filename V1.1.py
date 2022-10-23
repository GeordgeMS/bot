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

def nn(peer_id,token,a,b,idd,sl):
    captcha=''
    time.sleep(sl)
    while b in tokens[a]:
        time.sleep(0.8)
        ms=fras[random.randint(0,len(fras)-1)]
        if int(idd)!=0:
            ms='@id'+str(idd)+' ('+ms+')'
        req=json.loads(requests.get(f'https://api.vk.com/method/messages.send?message={ms}&peer_id={peer_id}&random_id=0&access_token={token}&v=5.131{captcha}').text)
        if 'error' in req and req['error']['error_code']==14:#error captcha
            captcha=f'&captcha_key={vc.solve(sid=req["error"]["captcha_sid"],s=1)}&captcha_sid={req["error"]["captcha_sid"]}'
    return 0

def timer(a,b,peer,sl,pr):
    captcha=''
    while b in tokens[a]:
        for u in range(5):
            ms=pr+fras[random.randint(0,len(fras)-1)]
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
    while len(tokens[a])>b and tokens[a][b].find(idd[0]+'='+idd[1]+'='+idd[2])!=-1:
        tkns=tokens[a][b].split('=')
        time.sleep(int(idd[2]))
        for ii in range(3,len(tkns),2):
            if len(ids)<=int((ii-3)/2):
                ids.append('-1')
            if tkns[ii+1]!=ids[int((ii-3)/2)]:
                ms=fras[random.randint(0,len(fras)-1)]
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
            if jj1[0]=='2':
                for q in range(int(jj1[3])):
                    Process(target=nn,args=(jj1[1],tokens[a][0],a,'2='+('='.join(jj1[1:4])),jj1[2],q,)).start()
            elif jj1[0]=='3' and jj1[2]!='0':
                Process(target=auto,args=(a,jj+1,['3',jj1[1],jj1[2]])).start()
            elif jj1[0]=='4':
                Process(target=timer,args=(a,'4='+jj1[1]+'='+jj1[2]+'='+jj1[3],jj1[1],jj1[3],jj1[2],)).start()
        while True:
            try:
                event=json.loads(requests.get(f'https://{ser["response"]["server"]}?act=a_check&key={ser["response"]["key"]}&ts={ser["response"]["ts"]}&wait=25&mode=2&version=3').text)
                print(event)
                if 'failed' in event:
                    ser=json.loads(requests.get(f'https://api.vk.com/method/messages.getLongPollServer?access_token={tokens[a][0]}&v=5.131').text)
                if 'updates' in event:
                    ser['response']['ts']=event['ts']
                    for upd in event['updates']:
                        if upd[0]==4 and ((len(upd)>6 and 'from' in upd[6] and int(upd[6]['from'])==myid) or ((len(upd)<=6 or 'from' not in upd[6]) and upd[2]>1)):
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
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Используйте +с [скорость(макс 4)] (id|домен|реплай)!&random_id=0&access_token={tokens[a][0]}&v=5.131')
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
                                    else:
                                        if len(mess)>=3:
                                            try:
                                                up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[2])
                                                up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
                                            except:
                                                pass 
                                    try:
                                        if not '2='+str(upd[3])+'='+str(up)+'='+str(bb) in tokens[a]:
                                            tkns1=tokens[a]
                                            tkns1.append('2='+str(upd[3])+'='+str(up)+'='+str(bb))
                                            tokens[a]=tkns1
                                            text[a]=text[a].replace('\n','')+':2='+str(upd[3])+'='+str(up)+'='+str(bb)+'\n'
                                            with open("settings", "w+") as file1:
                                                file1.write(''.join(text))
                                            for q in range(bb):
                                                Process(target=nn,args=(upd[3],tokens[a][0],a,'2='+str(upd[3])+'='+str(up)+'='+str(bb),up,q,)).start()
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
                                else:
                                    if len(mess)>1:
                                        try:
                                                up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                                up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
                                        except:
                                                    pass 
                                with open("settings") as text:
                                        text=text.readlines()
                                if len(mess)==2 and mess[1]=='all':
                                    tokens[a]=[i for i in tokens[a] if i.find('2=')==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                elif len(mess)==1:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+str(upd[3]))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                else:
                                    tokens[a]=[i for i in tokens[a] if i.find('2='+str(upd[3])+'='+str(up))==-1]
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
                                    if len(mess)>1:
                                        try:
                                            up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                            up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
                                        except:
                                            pass 
                                zd=0
                                if len(mess)>2:
                                    zd=int(mess[2])
                                if text[a].find(':3='+str(up))==-1:
                                            text[a]=text[a].replace('\n','')+':3='+str(up)+'='+str(zd)+'\n'
                                            tkns1=tokens[a]
                                            tkns1.append('3='+str(up)+'='+str(zd))
                                            tokens[a]=tkns1
                                            with open("settings", "w+") as file1:
                                                file1.write(''.join(text))
                                            if zd!=0:
                                                Process(target=auto,args=(a,len(tokens[a])-1,['3',str(up),str(zd)])).start()
                            elif mess[0].lower()=='-а':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                up=0
                                if len(upd)>=8 and 'reply' in upd[7]:
                                    if 'marked_users' in upd[6]:
                                        up = str(upd[6]['marked_users'][0][1][0])
                                    else:
                                        up = str(upd[3])
                                else:
                                    if len(mess)>1:
                                        try:
                                            up=re.sub("@|\[|vk.com/|https:|//|^\s+|\n|\r|\s+$", '', mess[1])
                                            up=json.loads(requests.get(f'https://api.vk.com/method/users.get?user_ids={up}&access_token={tokens[a][0]}&v=5.131').text)['response'][0]['id']
                                        except:
                                            pass 
                                if up!=0:
                                    with open("settings") as text:
                                        text=text.readlines() 
                                    tokens[a]=[i for i in tokens[a] if i.find('3='+str(up))==-1]
                                    text[a]=':'.join(tokens[a])+'\n'
                                    with open("settings", "w+") as file1:
                                        file1.write(''.join(text))
                            elif mess[0].lower()=='+т':
                                requests.get(f'https://api.vk.com/method/messages.delete?peer_id={upd[3]}&message_ids={upd[1]}&delete_for_all=1&access_token={tokens[a][0]}&v=5.131')
                                if len(mess)==1:
                                    requests.get(f'https://api.vk.com/method/messages.send?peer_id={upd[3]}&message=Используйте +т [время(сек)] (шапка)!&random_id=0&access_token={tokens[a][0]}&v=5.131')
                                else:
                                    with open("settings") as text:
                                        text=text.readlines() 
                                    up=''
                                    if len(mess)>=3:
                                        up=mess[2]
                                    try:
                                        if not '4='+str(upd[3])+'='+str(up)+'='+str(mess[1]) in tokens[a]:
                                            tkns1=tokens[a]
                                            tkns1.append('4='+str(upd[3])+'='+str(up)+'='+str(mess[1]))
                                            tokens[a]=tkns1
                                            text[a]=text[a].replace('\n','')+':4='+str(upd[3])+'='+str(up)+'='+str(mess[1])+'\n'
                                            with open("settings", "w+") as file1:
                                                file1.write(''.join(text))
                                            Process(target=timer,args=(a,'4='+str(upd[3])+'='+str(up)+'='+str(mess[1]),upd[3],int(mess[1]),up,).start()
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
                                        file1.write(''.join(text
                        elif upd[0]==4:
                            usr_id=None
                            if len(upd)>6 and 'from' in upd[6] and ''.join(tokens[a]).find(str(upd[6]['from']))!=-1:
                                usr_id=str(upd[6]['from'])
                            elif len(upd)>2 and upd[2]==1 and ''.join(tokens[a]).find(str(upd[3]))!=-1:
                                usr_id=str(upd[3])
                            if usr_id!=None:
                                for tp in range(len(tokens[a])):
                                    if tokens[a][tp].find('3='+str(usr_id))!=-1:
                                            tkns1=tokens[a]
                                            tkns1[tp]=tkns1[tp].split('=')
                                            if int(tkns1[tp][2])==0:
                                                ms=fras[random.randint(0,len(fras)-1)]
                                                captcha=''
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
