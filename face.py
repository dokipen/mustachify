import requests
import sys
import json

def find_faces(url):
    key = '7bdb6c49418f9f42b3217625fd91a6dd'
    secret = '2c6a2047416e91b09e90f467fbf44837'
    req =  'http://api.face.com/faces/detect.json?api_key={key}'
    req += '&api_secret={secret}&urls={url}&detector=Aggressive'
    req += '&attributes=all'
    req = req.format(key=key, secret=secret, url=url)
    r = requests.get(req)
    faces = json.loads(r.text)
    ret = []
    for photo in faces['photos']:
        w, h = photo['width'], photo['height']
        for tag in photo['tags']:
            ret.append({'mouth_center': (int(tag['mouth_center']['x'] * w / 100), 
                                         int(tag['mouth_center']['y'] * h / 100)),
                        'roll': tag['roll'],
                        'size': int(tag['width'] * w / 100)})
    return ret
    

if __name__ == '__main__':
    print find_faces(sys.argv[1])
    