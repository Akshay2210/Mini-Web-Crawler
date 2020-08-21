import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import os


PROJECT_NAME=str(input("Enter Project Name:"))
HOMEPAGE=str(input("Enter Website to Crawl:"))
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

print('Crawling...')


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()



def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()



def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        
        create_jobs()

def printer():
    os.system('clear')
    print('Links found by the Spider:')
    x=open(PROJECT_NAME+'/crawled.txt',"r")
    print(x.read())

create_workers()
crawl()
printer()
