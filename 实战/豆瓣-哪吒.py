import requests
from lxml import etree
import csv


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}


def parse_page(current_url):
    response = requests.get(current_url, headers=HEADERS)
    text = response.text
    html = etree.HTML(text)
    # item = html.xpath("//div[@class='comment-item']")[0]
    # print(etree.tostring(item, encoding='utf-8').decode('utf-8'))
    items = html.xpath("//div[@id='comments']/div[position()<21]")
    movies_ = []
    for item in items:
        comments = {}
        try:
            comment_time = item.xpath(".//span[@class='comment-time ']/text()")[0]
            comment_rating = item.xpath(".//span[@class='comment-info']/span[2]/@title")[0]
            comment_star = item.xpath(".//span[@class='comment-info']/span[2]/@class")[0][7:8]
            comment_cond = item.xpath(".//span[@class='comment-info']/span[1]/text()")[0]
            comment_by = item.xpath(".//span[@class='votes']/text()")[0]
            comment_detail = item.xpath(".//span[@class='short']/text()")[0]
        except:
            comment_time = ''
            comment_by = ''
            comment_cond = ''
            comment_star = ''
            comment_detail = ''
            comment_rating = ''

        comments['评论时间'] = comment_time.strip()
        comments['评分'] = comment_star
        comments['推荐级别'] = comment_rating
        comments['认为有用'] = comment_by
        comments['评论内容'] = comment_detail
        comments['观看情况'] = comment_cond
        movies_.append(comments)
    return movies_




def spider():
    url = 'https://movie.douban.com/subject/26794435/comments?start={}&limit=20&sort=new_score&status=P'
    count = 1
    page = 0
    total = []
    while count <= 4:
        current_url = url.format(page)
        print(current_url)
        movies = parse_page(current_url)
        for movie in movies:
            total.append(movie)
        #print('已爬取%s页' % count)
        count += 1
        page += 20


    header = ['评论时间','评分', '推荐级别', '认为有用', '评论内容', '观看情况']
    with open('douban.csv', 'w', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, header)
        writer.writeheader()
        writer.writerows(total)


if __name__ == '__main__':
    spider()