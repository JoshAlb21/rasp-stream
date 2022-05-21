import cv2
import socket
import pickle
import struct
from threading import Thread

import sys
import sys
client_path = '/home/<client_folder>'
sys.path.append(client_path)

from data_to_send import DataManager

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 10001				

    s.bind(('', port))
    print ("socket binded to %s" %(port)) 

    s.listen(5)	 
    print ("socket is listening")

    c, addr = s.accept()
    print ('Got connection from', addr ) 

    #STREAM
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    data_recorder = DataManager()
    data_recorder.run_data_collecting()

    while True:
        #Camera Data
        ret, frame = cam.read()
        result, frame_send = cv2.imencode(".jpg", frame, encode_param)
        frame_data = pickle.dumps(frame_send, 0)
        size_frame_data = len(frame_data)

        #Additional Data
        try:
            data_val = data_recorder.get_value()
        except AttributeError:
            print('data value has not been updated yet!')
            data_val = -1
        data_file = pickle.dumps(data_val, 0)
        size_data_file = len(data_file)

        c.sendall(struct.pack(">L",size_frame_data)+frame_data+struct.pack(">L",size_data_file)+data_file)

    cam.release()
