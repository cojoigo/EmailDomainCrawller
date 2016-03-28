import sys, re, urllib
from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

visitedDomains = set()

def find_email_address2(domain):
    #print("visiting: "+domain)
    if domain in visitedDomains:
        return
    with closing(Firefox()) as browser:
        browser.get('http://'+domain)
        page_source = browser.page_source
    soup = BeautifulSoup(page_source, "lxml")
    #find email addresses on page
    domains = check_page(soup)
    visitedDomains.add(domain)
    for i in set(domains):
        print(i)
    #find links in page
    links = find_links(soup, domain)
    #print(links)
    for j in set(links):
        find_email_address2(j)

def check_page(document):
    email_reg = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    pattern = re.compile(email_reg)
    return re.findall(pattern, str(document))

def find_links(document, domain):
    links = re.findall('''href=["'](.[^"']+)["']''', str(document))
    retLinks = set()
    for i in links:
        if sys.argv[1] in i:
            if 'http://' in i:
                i.strip('http://')
            if 'https://' in i:
                i.strip('https://')
            if 'mailto:' in i:
                continue
            retLinks.add(i)
        if re.match("^\/[a-zA-Z0-9_-]{1,10}", i):
            if i in visitedDomains:
                continue
            #regex didn't want to cooperate here
            if '.' in i:
                continue
            retLinks.add(domain+i)
            visitedDomains.add(i)
    return retLinks


#run as command line application
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a domain only")
    else:
        find_email_address2(sys.argv[1])