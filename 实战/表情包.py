import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading


class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            img_name = img.get('alt')
            ## 去除指定符号
            img_name = re.sub(r'[\\/:\*\?\'\"\<\>\|]', '', img_name)
            ## 获取后缀名
            suffix = os.path.splitext(img_url)[1]
            file_name = img_name + suffix
            self.img_queue.put((img_url, file_name))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, file_name = self.img_queue.get()
            request.urlretrieve(img_url, 'images/' + file_name)
            print(file_name + '下载完成！！！')


def main1():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1, 10):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url)

    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()
    for x in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()

#########################################################
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
    for img in imgs:
        img_url = img.get('data-original')
        img_name = img.get('alt')
        ## 去除指定符号
        img_name = re.sub(r'[\\/:\*\?\'\"\<\>\|]', '', img_name)
        ## 获取后缀名
        suffix = os.path.splitext(img_url)[1]
        file_name = img_name + suffix
        ## 下载链接
        request.urlretrieve(img_url, 'images/' + file_name)
        print(file_name,'下载完成！！！')


def main2():
    for x in range(1, 10):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        parse_page(url)


# if __name__ == '__main__':
#     main1()
#     main2()