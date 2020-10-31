#Only works for 4anime.to

import requests
from bs4 import BeautifulSoup
from clint.textui import progress
import sys
import os
session = requests.Session()

#os.chdir(r"C:\Users\user\Downloads")						#setting default download directory		uncomment the line by removing the # and editting the address in quotes

url = input("Enter episode URL: ")
slice_index = url.rfind("-episode-") + 9
sliced_url = url[:slice_index]
#use start > 0 and end > 0 and start <= end
start = int(input("Start episode: "))
end = int(input("End episode: "))
filename = str(input("Filename prefix: "))					#Setting filename

if start > 0 and end > 0 and start <= end : 
    for i in range(start,end+1):
        no = str(i)
        if(len(no) == 1):
            final_url = sliced_url + "0" + no
        else:
            final_url = sliced_url + no
        print("\naccessing url : " + final_url)
        r = session.get(final_url)                  		#starting webscraping
        soup = BeautifulSoup(r.text, 'html.parser')
        source = soup.find_all('source')
        if(source != []):
            img_link = source[0].get('src')
            print("starting download - episode : " + no)
            raw_image = session.get(img_link,stream=True)
            total_length = int(raw_image.headers['Content-Length'])
            with open(filename+" "+ no + '.mp4', 'wb') as f:
                    for c in progress.mill(raw_image.iter_content(chunk_size=1024),expected_size=(total_length/1024) +1):
                        if c:
                            f.write(c)
                            f.flush()
        else:
            print("episode not found")
    print("\nfinished\n")
else:
    print("\nprovide meaningful values\n")
