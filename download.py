import os
import requests
import re
from urllib.parse import urlparse
import shutil
import argparse

def download_img(url,save_path):
    proxies = {
        'http':'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
    }
    r = requests.get(url,proxies=proxies, stream=True)
    if r.status_code == 200:
        open(save_path, 'wb').write(r.content)
    del r



def start(item):
    print("------------------------------------")
    print(item.encode())
    if not item[-2:] == 'md':
        return False
    if not os.path.exists(f"../../source/images/{item[:-3]}/"):
        os.mkdir(f"../../source/images/{item[:-3]}/")
    

    with open(f"./{item}","r",encoding="utf8") as f:
        text = f.read()
    try:
        image_links = re.findall("\!\[.*?\]\((.*?)\)",text)
        for image_link in image_links:
            if image_link[:4] != "http":
                continue
            else:
                print(image_link)


            url_parse = urlparse(image_link).path[1:].replace('/','_')
            save_path = f'../../source/images/{item[:-3]}/{url_parse}'
            download_img(image_link,save_path)

            text = text.replace(image_link,f'../../source/images/{item[:-3]}/{url_parse}')
        with open(f"./{item}",'w',encoding="utf8") as f:
            f.write(text)
    except:
        return False

def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help='markdown文件全名', dest="file")
    args = parser.parse_args()
    options = vars(args)
    return options
if __name__ == "__main__":
    options = Parser()
    if not options["file"]:
        print("python download.py -f 'filename.md'")
    else:
        start(options["file"])
    