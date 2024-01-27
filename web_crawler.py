import sys
import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
import argparse
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TO_CRAWL = []
CRAWLED = set()
LINK_COUNT = 0
PAGE_COUNT = 0

BANNER = """

 ██╗    ██╗███████╗██████╗      ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗     
██║    ██║██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗    
██║ █╗ ██║█████╗  ██████╔╝    ██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝    
██║███╗██║██╔══╝  ██╔══██╗    ██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗    
╚███╔███╔╝███████╗██████╔╝    ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║    
 ╚══╝╚══╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝    
                                                                                            
██████╗ ██████╗  ██╗████████╗ ██████╗                                                       
╚════██╗██╔══██╗███║╚══██╔══╝██╔═████╗                                                      
 █████╔╝██████╔╝╚██║   ██║   ██║██╔██║                                                      
 ╚═══██╗██╔══██╗ ██║   ██║   ████╔╝██║                                                      
██████╔╝██║  ██║ ██║   ██║   ╚██████╔╝        

github: https://github.com/brito101
"""

def print_banner():
    print(BANNER)
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Web Crawler Script")
    parser.add_argument("domain", help="DOMAIN to start crawling from - ex: rodrigobrito.dev.br")
    return parser.parse_args()

def determine_url_properties(url):
    try:
        for prefix in ["https://www.", "http://www.", "https://", "http://"]:
            full_url = f"{prefix}{url}"
            http = urllib3.PoolManager()
            response = http.request("GET", full_url, timeout=urllib3.Timeout(connect=5, read=5), retries=urllib3.Retry(2, redirect=2))
            
            if response.status == 200:
                print(f"Status code for {full_url}: {response.status}")
                return prefix, True if "www." in prefix else False

    except urllib3.exceptions.HTTPError as e:
        
        return None, None

def request(url, timeout=5):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"}
    http = urllib3.PoolManager()
    try:
        response = http.request("GET", url, headers=header, timeout=urllib3.Timeout(connect=timeout, read=timeout), retries=urllib3.Retry(2, redirect=2))
        return response.data
    except KeyboardInterrupt:
        sys.exit(0)
    except urllib3.exceptions.HTTPError:
        pass

def get_links(html):
    global LINK_COUNT
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else None

        for tag in tags_a:
            link = tag["href"]
            if link.startswith("http"):
                link_domain = urlparse(link).netloc
                links.append(link)
                LINK_COUNT += 1
                print(f"Title: {title} | Link: {link}")
        return links
    except Exception as e:
        pass

def crawl(url):
    global PAGE_COUNT
    
    while TO_CRAWL:
        current_url = TO_CRAWL.pop()
        
        if current_url not in CRAWLED:
            html = request(current_url)
            if html:
                links = get_links(html)
                
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL and url in link:
                            TO_CRAWL.append(link)
                            PAGE_COUNT += 1
                            title = get_title(link)
                            print(f"Title: {title} | Link: {link}")
                    print("Crawling {}".format(current_url))
                CRAWLED.add(current_url)
            else:
                CRAWLED.add(current_url)

def get_title(url):
    try:
        html = request(url)
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        return title_tag.text.strip() if title_tag else None
    except Exception as e:
        pass
    
if __name__ == "__main__":
    print_banner()
    
    args = parse_arguments()

    domain = args.domain
    
    prefix, needs_www = determine_url_properties(domain)
    if(needs_www):
        domain = prefix + domain
    
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Script started at: {start_time}\n")
        
    TO_CRAWL.append(domain)   
           
    crawl(domain)
    
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"\nScript end at: {end_time}")
    print(f"Total links found: {LINK_COUNT}")
    print(f"Total pages crawled: {PAGE_COUNT}")  
