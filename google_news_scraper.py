from bs4 import BeautifulSoup
import requests, re, csv, datetime

search_term = input("What's the term you want to search in Google News? ")
search_term = search_term.replace(" ", "+")


request_page = "https://www.google.com/search?q="+search_term+"&tbm=nws"
page = requests.get(request_page)
soup = BeautifulSoup(page.text, 'html.parser')  #抓出全頁的source code
result_block_1 = soup.find_all('h3', attrs={'class': 'r'})    #抓出Title / link的部分
result_block_2 = soup.find_all('div', attrs={'class': 'slp'})    #抓出Publisher / Date的部分

regex_rule = re.compile(r'&sa=U&.*|&amp;sa=U.*')

title_list = []
link_list = []
publisher_list = []

for result in result_block_1:
    title = result.get_text()   #列出Title
    title_list.append(title)

    link = result.find('a')
    link = link['href']
    link = link.replace(regex_rule.search(link).group(),'')
    link = link.replace('/url?q=','')
    link_list.append(link)
    #print(link)

for result in result_block_2:
    publisher = result.get_text()
    publisher_list.append(publisher)
    #print(publisher)


#Write into an CSV file
def csv_output():
    today = datetime.date.today()
    today = today.strftime("%Y%m%d")

    output = open(search_term+'_news_'+today+'.csv', 'w', newline='')
    output_writer = csv.writer(output)
    output_writer.writerow(['Title', 'Link', 'Publisher/Date'])
    for i in range(len(title_list)):
        row = []
        row.append(title_list[i])
        row.append(link_list[i])
        row.append(publisher_list[i])
        output_writer.writerow(row)
    output.close()

csv_output()
