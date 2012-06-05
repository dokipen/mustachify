import sys

import stachify
import face

if __name__ == '__main__':
    faces = face.find_faces(sys.argv[1])
    print stachify.add_stache(sys.argv[1], faces[0]['mouth_center'], faces[0]['roll'], faces[0]['size'])