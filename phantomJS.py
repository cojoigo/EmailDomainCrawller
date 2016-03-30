import sys, re, time
from bs4 import BeautifulSoup
from urlparse import urlparse
from selenium import webdriver

visitedDomains = set()
foundEmails = set()
clickedLinks = set()
originDomain = ""

def find_email_address2(domain, visitedPages):
    visitedPages -= 1
    domain = 'http://'+domain
    if domain in visitedDomains:
        return
    o = urlparse(domain)
    #verify we stay in domains that match the input netlocation
    if originDomain not in o.netloc:
        return
    print("visiting: "+domain)
    driver = webdriver.PhantomJS()
    driver.set_window_size(1124, 850)
    driver.get(domain)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    #find email addresses on page
    domains = check_page(soup)
    visitedDomains.add(domain)
    for i in set(domains):
        foundEmails.add(i)
    #find links in page
    links = find_links(soup, domain)

    #click on link
    spans = driver.execute_script("return document.querySelectorAll('span')");
    ngClicks = set()
    for i in spans:
        if i.get_attribute('ng-click'):
            ngClicks.add(i)
    for i in ngClicks:
        if i not in clickedLinks:
            clickedLinks.add(i.get_attribute('ng-click'))
            navigate(driver, i)

    #check recursion
    if visitedPages == 0:
        return
    for j in sorted(set(links)):
        find_email_address2(j, visitedPages)

def navigate(driver, i):
    driver.execute_script("arguments[0].click();", i)
    time.sleep(2)
    #wait 2s for the page to load
    print("Navigated to "+driver.current_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    #find email addresses on page
    domains = check_page(soup)
    visitedDomains.add(driver.current_url)
    for i in set(domains):
        foundEmails.add(i)
    #find links in page
    links = find_links(soup, driver.current_url.strip('http://'))
    return

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
                i=i.strip('http://')
            if 'https://' in i:
                i=i.strip('https://')
            if 'mailto:' in i:
                continue
            retLinks.add(i)
    return retLinks

#run as command line application
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Please provide a domain name, OPTIONAL and recursion depth")
    else:
        if len(sys.argv) == 3:
            recurseDepth = int(sys.argv[2])
        else:
            recurseDepth = 1
        originDomain = sys.argv[1]
        if recurseDepth < 1:
            recurseDepth = 1
        print("Searching domain: "+originDomain+" with recursion depth: "+str(recurseDepth))
        find_email_address2(originDomain, recurseDepth)
        print("Found Emails: ")
        for i in foundEmails:
            print(i)