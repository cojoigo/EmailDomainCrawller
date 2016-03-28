# EmailDomainCrawller
Jana Challenge

Required Packages:
sys
requests
BeautifulSoup
selenium
contextlib

I have 2 solutions, find_email_addresses.py and find_email_address2.py. Both are run from the command line in the format explained python find_email_addresses.py jana.com and will print out found email addresses. The first solution uses an API called emailhunter I found and got a free key for, it gives many results back but since it is a very short file and doesn't guarantee the same level of crawling on a domain I impleneted a second solution. The second solution is my crawler and parser, I didn't have much luck with a bot (scrappy) so I implimented my own crawler that looks for navigatable links and checks itself to avoid infinite looping. This uses Firefox to open the browser (to load pages with Javascript) and saves the loaded data to html that is then parsed.
