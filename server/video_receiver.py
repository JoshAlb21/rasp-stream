import os
from multiprocessing import Process,Queue,Pipe,Value
import time
from datetime import datetime
import numpy as np
import sys
import server_settings
import video_saver
from signal_processing import general_processing
from general import tools, show_info
import receive_data
from threading import Thread

raw_dp_queue = Queue() #FIFA
data_tupel_queue = Queue()
connection_closed = Value('i', 0)

from inference import object_detection
face_detector = object_detection.ObjectDetectorTf1(server_settings.face_detector_path, server_settings.input_img_width, server_settings.input_img_height)
last_acc_face_box = np.zeros([4, 1])

def get_data_points():
    'receive data points from client'
    
    global raw_dp_queue
    dp = {}
    data_measurement = receive_data.Data_Measurement(show_video=False)
    while True:
        frame, additional_val = data_measurement.update()
        dp['frame'] = frame
        dp['time'] = simulate_time_stamp()
        dp['additional_val'] = additional_val
        raw_dp_queue.put(dp)
        #print(raw_dp_queue.qsize())

def simulate_time_stamp():
    '''
    we have to simulate the time stamp of the frame records (dont know yet how to send more than one array)
    current state: time stamp is the time when receiving a frame
    TODO should be the time when capturing the frame
    '''
    return datetime.now()

def start_stream():
    'start data point stream'

    #build connection
    #server_process = Process(target=get_data_points, args=(), daemon=True)
    #start process
    #server_process.start()
    #TODO wenn auf linux: wieder mit Process machen wie oben
    receive_thread = Thread(target=get_data_points, args=())
    receive_thread.start()

def compute_time_delta(start, end):
    differ = start - end
    print(differ.dt.total_seconds()['time'])

def receive_loop():
    'looking wheter there are data points in queue and then calling the processing pipeline'

    tools.replace_existing_path(server_settings.plot_path)
    start_stream()

    #global raw_dp_queue
    global data_tupel_queue
    global face_detector
    global last_acc_face_box
    last_dp_batch = None
    collect_raw_dp = []
    fft_batch = []
    plot_data = {'additional_data': [], 'data_predict': []}
    num_of_points_per_batch = int(server_settings.fps * server_settings.window_size_per_fft)
    batch_counter = 1
    frame_counter = 1
    while True:
        if raw_dp_queue.qsize() == 0:
            print(f'pipe is empty (time:{datetime.now().time().replace(microsecond=0)})', end="\r")
            continue
        else:
            collect_raw_dp.append(raw_dp_queue.get())
            if connection_closed.value == 1:
                print('FINISHED')
                break
            
            df_data_point, last_acc_face_box = video_saver.save_data_points("data")
            data_tupel_queue.put(df_data_point)
            frame_counter +=1

        cond1 = (batch_counter == 1) and (data_tupel_queue.qsize() > num_of_points_per_batch)
        cond2 = (batch_counter > 1) and (data_tupel_queue.qsize() > server_settings.offset_next_fft)
        
        if cond1 or cond2:
            'process data values'

            if cond1: #batch to start with
                pass
            elif cond2:
                pass
            
            # Processing
            # ...
            
            #General (same for all method)
            plot_data = show_info.plot_values(plot_data)
            show_info.print_info("data")

            batch_counter += 1 

if __name__ == '__main__':
    receive_loop()
