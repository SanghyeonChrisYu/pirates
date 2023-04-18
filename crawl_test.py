from turtle import title
import requests
from bs4 import BeautifulSoup as bs

header = {'User-agent': 'Mozila/2.0'}
response = requests.get("https://www.naver.com", headers=header)
html = response.text
# print(html)

f = open('temp_html.txt', 'w', encoding='utf8')
f.write(html)
f.close()

soup = bs(html, 'html.parser')
# print(soup)
word = soup.select_one("#NM_set_home_btn") # css 선택자 때문에 id를 가져올때는 #을 붙인다
print(word)
print(word.text)
print()

response = requests.get("https://news.naver.com/", headers=header) 
html = response.text
soup = bs(html, 'html.parser')
title_list = soup.select(".cjs_link_dept")
print(type(title_list))
print(len(title_list))
print(title_list[1].text.strip()) # text.strip() 가능 -> 양쪽 공백 제거해주는거
print(title_list[1].attrs['href'])


## 검색어 바꾸기: 검색 결과 창 url에서 query={keyword} 이런 식으로 넣어주면 됨
## 여러 페이지 찾기: 페이지 바뀌면서 url 어떻게 바뀌는지 확인해서 바꿔주면 됨

# 결국 핵심은 원하는 요소를 찾고, 클릭하고, 입력하고, 가져오는 것
# ㄴㄷㄱ
