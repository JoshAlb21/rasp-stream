import socket
import numpy as np
import cv2
import pickle
import struct
import time

import server_settings

class Data_Measurement:
    def __init__(self, session_name=None, show_video:bool=True):
        self.socket_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_stream.connect(("192.168.188.26", 10001))

        self.data = b""
        self.payload_size = struct.calcsize(">L")

        self.show_video = show_video
        self.frame_counter = 0

    def update(self):
        'preprocess binary stream for further processing'

        frame, additional_val = self.recv_data()
        if self.show_video:
            show_frame(frame, self.frame_counter)
        
        return frame, additional_val
    
    def recv_data(self):
        'receive data trough socket from RaspPi'

        frame = self.recv_frame()

        if not server_settings.additional_val_signal:
            additional_val = 0.0
        else:
            additional_val = self.recv_additional_val()

        return frame, additional_val
    
    def recv_frame(self):
        'convert and decode Frame Data'
        
        while len(self.data) < self.payload_size:
            self.data += self.socket_stream.recv(4096)
        
        packed_msg_size_frame = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size_frame = struct.unpack(">L", packed_msg_size_frame)[0]
        while len(self.data) < msg_size_frame:
            self.data += self.socket_stream.recv(4096)
        frame_data = self.data[:msg_size_frame]
        self.data = self.data[msg_size_frame:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        return frame
    
    def recv_additional_val(self):
        'Decode additional Data'

        while len(self.data) < self.payload_size:
            self.data += self.socket_stream.recv(4096)
        
        packed_msg_size_additional_val = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size_additional_val = struct.unpack(">L", packed_msg_size_additional_val)[0]
        while len(self.data) < msg_size_additional_val:
            self.data += self.socket_stream.recv(4096)
        additional_val_data = self.data[:msg_size_additional_val]
        self.data = self.data[msg_size_additional_val:]

        additional_val = pickle.loads(additional_val_data, fix_imports=True, encoding="bytes")

        return additional_val


def show_frame(frame, frame_counter:int):
    
    if frame_counter % 2 == 0: #increase smoothness of video stream
        cv2.imshow('ImageWindow',frame)
        cv2.waitKey(1)


if __name__ == '__main__':

    data_measurement = Data_Measurement(show_video=False)

    while True:
        data_measurement.update()
        time.sleep(0.05)
