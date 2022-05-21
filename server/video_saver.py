'save batch of data points and time stamp list'
import numpy as np
import pandas as pd
import cv2
from typing import Tuple
from inference import object_detection
import server_settings

def save_data_points(data_point:dict, face_detector:object_detection.ObjectDetectorTf1, frame_counter:int) -> Tuple[dict, list]:
    'main method for data point processing'
        
    #process frame
    try:
        frame = data_point['frame']
    except TypeError:
        print('data_point got no key "frame"')
        print(data_point)
        return

    face_img = process_frame(data_point['frame'], face_detector)
    
    if server_settings.show_frame:
        show_frame(face_img, frame_counter)

    #Compute mean channel
    blue_channel = save_vid_to_channel(face_img, 'blue')
    mean_blue_channel = average_channel(blue_channel)

    dp_processed = {'time': data_point['time'], 'mean_blue': mean_blue_channel, 'additional_data': data_point['additional_data']}

    return dp_processed

def show_frame(frame, frame_counter:int=2):
    
    if frame_counter % 3 == 0: #increase smoothness of video stream
        #frame = cv2.resize(frame, (110, 110))
        cv2.imshow('ImageWindow',frame)
        cv2.waitKey(1)
    
def process_frame(frame, face_detector):

    #face detection
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Note: Perfomance from face detector is better on RGB
    complete_frame_raw = frame.copy()
    
    face_img = crop_face(complete_frame_raw, server_settings.more_cut_x, server_settings.more_cut_y)

    if type(face_img) == type(None):
        face_img = np.zeros((100,100))

    return face_img

def process_frame(frame:np.ndarray, detector):
    pass

def crop_img(frame, more_cut_x:float, more_cut_y:float) -> np.ndarray:
 
    crop_cond = [y_min < y_max, x_min < x_max]
    if not all(crop_cond):
        print('invalid crop parameter')
        return None

    cropped_img = frame[y_min : y_max, x_min : x_max].copy()

    return cropped_img

def save_vid_to_channel(img, channel_name:str) -> float:

    all_channel = {'red': 0, 'green': 1, 'blue':2}
    try:
        channel = all_channel[channel_name]
    except KeyError:
        print(f'there is no {channel_name} channel')
        return
    single_channel = img[:,:,channel]

    return single_channel

def average_channel(channel):
    channel_mean = np.mean(channel)
    return channel_mean
