import numpy as np
from datetime import datetime
import time

def calibration_function(timestamp):
    # Replace this with your actual calibration logic
    return timestamp


def process_data(channels, timestamps, pps_ch, TAIdate):
    # Find indices where channels are not equal to pps_ch
    pps_idx = np.where(channels == pps_ch)[0]
    processed_data = {}
    if len(pps_idx) != 0:
        #TAIdate = WR.getDate()[1]
        oldTAIdate = TAIdate
        TAIdate = str(datetime.now().now())
        # Execute calibration function on selected timestamps
        calibrated_timestamps = calibration_function(timestamps)
        processed_data[oldTAIdate] = {ch: {oldTAIdate: calibrated_timestamps[:pps_idx[0]][channels[:pps_idx[0]] == ch]} for ch in np.unique(channels[:pps_idx[0]]) if ch != pps_ch}
        
        processed_data[TAIdate] = {ch: {TAIdate: calibrated_timestamps[pps_idx[0]:][channels[pps_idx[0]:] == ch]} for ch in np.unique(channels[pps_idx[0]:]) if ch != pps_ch}
    else:
        processed_data[TAIdate] = {ch: {TAIdate: calibration_function(timestamps)[channels == ch]} for ch in np.unique(channels)}

    #processed_data[TAIdate] = channel_data
    #print(processed_data)
    return processed_data


# Example usage

channels = np.array([1, 2, 2, 1, 2, 1, 8])
timestamps = np.array([100, 200, 300, 400, 500, 600, 700])

channels = np.array([1, 2, 2, 8, 2, 1, 8, 1, 2, 1, 1])
timestamps = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

channels = np.array([1, 2, 2, 1, 2, 1, 8, 1, 2, 1, 1])
timestamps = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

channels = np.array([1, 2, 2, 1, 2, 1, 8, 1, 2, 1, 1])
timestamps = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

pps_ch = 8
TAIdate = str(datetime.now().now())
time.sleep(0.5)



def send_data(data):
    print("will send data")
    print(data)
    for ch in data:
        pass
        #(f"data for channel {ch} :{data[ch]}")

pps_ch = 8
TAIdate = str(datetime.now().now())
print(TAIdate)
data_stream = {}
for i in range (10):
    channels = np.array([1, 2, 2, 1, 2, 1, 8, 1, 2, 1])
    timestamps = np.array([100+(i*1000), 200+(i*1000), 300+(i*1000), 400+(i*1000), 500+(i*1000), 600+(i*1000), 700+(i*1000), 800+(i*1000), 900+(i*1000), 1000+(i*1000)])

    processed_data = process_data(channels, timestamps, pps_ch, TAIdate)

    if TAIdate in processed_data:
        for ch in processed_data[TAIdate]:
            if ch in data_stream:
                data_stream[ch][TAIdate] = np.append(data_stream[ch][TAIdate], processed_data[TAIdate][ch][TAIdate])
            else:
                data_stream[ch] = processed_data[TAIdate][ch]
        del processed_data[TAIdate]
    
    # will be executed if new elements
    if(len(processed_data))>0:
        send_data(data_stream)
        data_stream = {}
        for WR_time in processed_data:
            for ch in processed_data[WR_time]:
                data_stream[ch] = processed_data[WR_time][ch]
            TAIdate = WR_time
        
    
                
        
                


        





"""for key, value in result.items():
    print(f"Channel {key}: {value}")
"""

