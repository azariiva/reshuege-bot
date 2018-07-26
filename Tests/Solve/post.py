import requests
from bs4 import BeautifulSoup

def extract(text):
    
    res = ''
    flag = False
    
    i = 0
    while i < len(text):
        if flag:
            if text[i] in '0123456789':
                res += text[i]
            else:
                break
        if text[i] in '№':
            flag = True
            i += 1
        i+= 1
        
    return res
        
def get_excercise(search):
    
    data= {'search': search}
    req = requests.get('https://rus-ege.sdamgia.ru/search', data=data)

    soup = BeautifulSoup(req.text, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()
    #print(soup.get_text())
    return(extract(soup.get_text()))

a = get_excercise(input())
print(a)
