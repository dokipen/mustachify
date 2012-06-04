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
        for tag in photo['tags']:
            ret.append({'mouth_center': (tag['mouth_center']['x'], tag['mouth_center']['y']),
                        'roll': tag['roll'],
                        'size': tag['width']})
    return ret
    

if __name__ == '__main__':
    print find_faces(sys.argv[1])