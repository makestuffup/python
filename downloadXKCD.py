#! python3
# downloadXKCD.py - Downloads the newest 10 comics from XKCD.com

import requests, os, bs4, sys

# Create directory for comics
try:
    os.mkdir('./XKCD Comics')
except:
    pass

# Download XKCD front page
res = requests.get('https://xkcd.com')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: {error}'.format(error=exc))
    sys.exit()

# Parse webpage and download image
i = 0
for i in range(0,10):
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # Generate image link
    image_soup = soup.find(id="comic")
    image_link = 'https:' + image_soup.img['src']
    status = 'Downloading: {img} as image{i}.png...'.format(img=image_link, i=i+1)
    print(status)

    # Download image
    res = requests.get(image_link)
    res.raise_for_status()
    image_file = open('./XKCD Comics/image%s.png' % (i+1), 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

    # Generate previous comic link and download page
    prev_soup = soup.find(rel="prev")
    prev_link = 'https://xkcd.com' + prev_soup['href']
    res = requests.get(prev_link)

print('Finished.')

