# Context 
The website of the parish from the mass I go to was hacked.
The attackers added a redirect from the homepage to a malicious website.
The parishoners found backups on the wayback machine, the latest capture of the blog posts page of which I found to be from Jan 4, 2022.

The link to the website can be found at https://web.archive.org/web/20220104120816/http://www.pastoralcentre.pl/blog-3/#.
Note that going to the home page from the wayback machine will redirect you to the malicious website.

Using the wayback machine, we can obtain 1280 URLs that have been captured the URL prefix `www.pastoralcentre.pl`.

The code in this repository tries to extract the pages from the wayback machine and save them to a local directory.
The ultimate goal is to reinsert them into the parishe's wordpress instance.

We will be using `python3.10` and `poetry`.

# Find all the suitable pages

The first step is to extract all the URLs captured by the wayback machine.
The URL with the list is at `https://web.archive.org/web/*/https://www.pastoralcentre.pl*`.
The script at `extract_urls.py` does this job, and exports the result to `all_pages.json`.