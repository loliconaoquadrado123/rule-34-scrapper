import requests
from pyquery import PyQuery as pq
import time
import logging
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
    }
folder='in/'
def main(tags='2d',amount=50,offset=0):
    baseUrl='https://rule34.xxx/index.php'
    url='https://rule34.xxx/index.php?page=post&s=list'

    imageSrcs=[]
    x=0
    while len(imageSrcs)<amount:
        srcList=[]
        done=False
        while done==False:
            try:
                filledUrl=f'{url}&tags={tags.replace(' ','+')}&pid={str(offset+amount*x+1)}'
                response=requests.get(filledUrl,headers=headers)
                if response.status_code==429:
                    print(response.status_code)
                    #print(response.headers)
                    print('\nrate limited. trying again soon')
                    time.sleep(3)
                else:
                    done=True
            except:
                print('\nerror. trying again soon')
                time.sleep(3)
                done=False
        print(f'reading page {x} of {int((amount/42))+(amount%42>0)}. status code: {response.status_code}')
        d=pq(response.text)
        h=d('.image-list')
        h=h('img')
        h=h.parent()
        if len(h)==0 and x==0:
            print('error, no matchs found')
            return 0
        if(len(h)==0):
            print('not enough search results. returning what we have')
            break

        print('Fetching links to the image posts from the search results')
        for i in range(len(h)):
            item=h[i]
            src=baseUrl+item.attrib['href']
            srcList.append(src)

        print('Fetching the image sources from the posts in the search results')
        for i in srcList:
            done=False
            while done==False:

                try:
                    response=requests.get(i,headers=headers)
                    
                    if response.status_code==429:
                        print(response.status_code)
                        #print(response.headers)
                        print('\n rate limited. trying again soon')
                        time.sleep(7)
                    else:
                        done=True
                except:
                    time.sleep(1000)
                    done=False
                    print('errpr')

            d=pq(response.content)
            src=d('#image').attr('src')
            if src!=None:
                imageSrcs.append(src)
       
       
       
        x+=11
    
    #print(imageSrcs)
    print('writing data to files')
    a=0
    for i in imageSrcs:
        if(a<amount):
            done=False
            while done==False:
                try:
                    print(i)
                    response=requests.get(i,headers=headers)
                    if response.status_code==429:
                        print(response.status_code)
                        #print(response.headers)
                        print('\n rate limited. trying again soon')
                        time.sleep(3)
                    else:
                        done=True
                        file=open('./'+str(a)+'.jpg','wb')
                        file.write(response.content)
                except Exception as e:
                    time.sleep(1)
                    done=False

            print(f'progress: {str(a)} out of {str(amount)}({str((a/amount)*100)}%)')
        a+=1
    
print('the amount of images: ')
amount=int(input())
print('the offset of the images in the search table: ')
offset=int(input())
print('the tags(separated by spaces like in the normal search bar):')
tags=input()
main(tags=tags,amount=amount,offset=offset)
print("DONE")
