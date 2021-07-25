
import re 
import requests
from bs4 import BeautifulSoup
import json

str = input("link copiado:")
output_file = input("nombre de archivo mp4:")
match = re.compile(r'.*(wvideo=)(.*)(\").*')
wvideo = match.search(str).group(2) 
print(wvideo) 

page = requests.get("https://fast.wistia.net/embed/iframe/"+wvideo+"?videoFoam=true")
soup = BeautifulSoup(page.content, 'html.parser')

script = soup.find_all('script')[4]
#print(script.text)
#http = re.compile(r'(.*)(https:.*bin)(.*)')
url = re.findall(r'https:[^"]*bin', script.text)[2]
print("Descargando archivo url:"+url)
r = requests.get(url, allow_redirects=True)
open(output_file+".mp4", 'wb').write(r.content)