from bs4 import BeautifulSoup
import requests
import os


def detect_latest(main_page):
    soup = BeautifulSoup(main_page,'lxml')
    latest = soup.find('div',class_='tape-item').find('a')['href']
    latest_id = int(latest.split('/')[-1])
    return latest_id


def download(link):
    r = requests.get(link)
    if r:
        return r.text


def parse_page(page):
    soup = BeautifulSoup(page,'lxml')
    title = soup.find('h1').text.strip()
    rubric = soup.find('li',class_='detail category').text.strip()
    date = soup.find('li',class_='detail date').text.strip().replace('-','.')
    author = soup.find('li',class_='detail author')
    if author is None:
        author = 'Noname'
    else:
        author = author.text.strip()
    text = '\n'.join([x.text.strip() for x in soup.find('div',class_='text').findAll('p')])
    return (title,rubric,date,author,text)


def write_article(link,title,rubric,date,author,text,idx):
    template = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n%s'
    with open('./articles/'+str(idx)+'.txt','w',encoding='utf-8-sig') as f:
        f.write(template % (author,title,date,rubric,link,text))
    

if __name__ == '__main__':
    if not os.path.exists('articles'):
        os.makedirs('articles')
    main_page = download('https://hron.ru')
    n_art = 0
    if main_page:
        n = detect_latest(main_page)
        while n_art < 1000:
            link = 'https://hron.ru/news/read/'+str(n)
            page = download(link)
            if page:
                title,rubric,date,author,text = parse_page(page)
                write_article(link,title,rubric,date,author,text,n)
                n_art += 1
            n -= 1
            
