import threading
import TimeTagger
import time
import queue
import numpy as np
np.set_printoptions(suppress=True)
from datetime import datetime
from WhiteRabbitSwitches.LEN_lib import dev



class TT_agent:
    def __init__(self, event_buffer_size = 1000000) -> None:
        self.tagger = TimeTagger.createTimeTagger()
        self.event_buffer_size = event_buffer_size
        self.pps_ch = 8
        self.WR = dev('COM4')
        self.cur_pps, self.old_pps, self.cal_fac, self.old_cal_fac = 0, 0, 0, 0
    
    def ttSetTriggerLevel(self, levels : dict):
        #levels : dict{channel:level}
        for channel in levels:
            self.tagger.setTriggerLevel(channel,levels[channel])

    def createStream(self, channels):
        stream = TimeTagger.TimeTagStream(tagger=self.tagger,
                                  n_max_events=self.event_buffer_size,
                                  channels=channels)
        return stream
    
    def calibration_function(self, timestamps, cal_fac):
        if cal_fac != 0:
            timestamps = (timestamps - self.old_pps) * cal_fac
        return timestamps
    
    def process_data(self, channels, timestamps, pps_ch, TAIdate):
        # Find indices where channels are not equal to pps_ch
        pps_idx = np.where(channels == pps_ch)[0]
        processed_data = {}
        if len(pps_idx) != 0:
            self.cur_pps = timestamps[pps_idx[0]]
            if self.old_pps != 0:
                self.old_cal_fac = self.cal_fac
                self.cal_fac = 1e12/(self.cur_pps - self.old_pps)                      
            oldTAIdate = TAIdate
            try:
                TAIdate = self.WR.getDate()[0]
                #TAIdate =  datetime.now().time()
            except:
                TAIdate = 'no WRS connected'
            # Execute calibration function on selected timestamps
            processed_data[oldTAIdate] = {ch: {oldTAIdate: self.calibration_function(timestamps[:pps_idx[0]], cal_fac = self.old_cal_fac)[channels[:pps_idx[0]] == ch]} for ch in np.unique(channels[:pps_idx[0]]) if ch != pps_ch}
            self.old_pps = self.cur_pps
            processed_data[TAIdate] = {ch: {TAIdate: self.calibration_function(timestamps[pps_idx[0]:], cal_fac = self.cal_fac)[channels[pps_idx[0]:] == ch]} for ch in np.unique(channels[pps_idx[0]:]) if ch != pps_ch}
        else:
            processed_data[TAIdate] = {ch: {TAIdate: self.calibration_function(timestamps[channels == ch], cal_fac = self.cal_fac)} for ch in np.unique(channels)}
        return processed_data

    def startStreaming(self, stream: TimeTagger.TimeTagStream):
        data_queue = queue.Queue()
        def stream_worker():
            stream.start()
            data_stream = {}
            TAIdate = '0'
            while stream.isRunning():
                data = stream.getData()
                if data.size > 0:
                    # With the following methods, we can retrieve a numpy array for the particular information:
                    channel = data.getChannels()            # The channel numbers
                    timestamps = data.getTimestamps()       # The timestamps in ps
                    overflow_types = data.getEventTypes()   # TimeTag = 0, Error = 1, OverflowBegin = 2, OverflowEnd = 3, MissedEvents = 4
                    missed_events = data.getMissedEvents()  # The numbers of missed events in case of overflow
                    
                    processed_data = self.process_data(channel, timestamps, self.pps_ch, TAIdate)

                    if TAIdate in processed_data:
                        for ch in processed_data[TAIdate]:
                            if ch in data_stream:
                                data_stream[ch][TAIdate] = np.append(data_stream[ch][TAIdate], processed_data[TAIdate][ch][TAIdate])
                            else:
                                data_stream[ch] = processed_data[TAIdate][ch]
                        del processed_data[TAIdate]
                    
                    # will be executed if new elements
                    if(len(processed_data))>0:
                        if len(data_stream) > 1:
                            data_queue.put(data_stream)
                        data_stream = {}
                        for WR_time in processed_data:
                            for ch in processed_data[WR_time]:
                                data_stream[ch] = processed_data[WR_time][ch]
                            TAIdate = WR_time
        
        thread = threading.Thread(target=stream_worker)
        thread.start()
        return thread, data_queue

    
    def stopStreaming(self, stream: TimeTagger.TimeTagStream, thread: threading.Thread):
        stream.stop()
        thread.join()  # Wait for the thread to finish


main_counter=0

myTT_agent = TT_agent()
myTT_agent.ttSetTriggerLevel({1:0.1,2:0.1})
stream1 = myTT_agent.createStream([1, 2, 8])
stream_thread, data_queue = myTT_agent.startStreaming(stream1)

stop_waiting = False
def stop_waiting_signal():
    global stop_waiting
    stop_waiting = True

print("s")
# Main thread can check the queue for data

try:
    while not stop_waiting:
        try:
            data = data_queue.get(timeout=1)
            # Process the data or return it to the main function
            print("===========")
            for ch in data:
                inner_dict_key = next(iter(data[ch]))
                array_size = len(data[ch][inner_dict_key])
                print(f"Recived {array_size} elements for channel: {ch}")
                print(data[ch])
            main_counter+=1
        except queue.Empty:
            pass
except KeyboardInterrupt:
    print("stopping the main thread")
    print("Stream stopped")
    print("main counter:", main_counter)
    stop_waiting_signal()

# Continue with other tasks
# Stop the streaming thread when done
myTT_agent.stopStreaming(stream1, stream_thread)
print(myTT_agent.cur_pps, myTT_agent.old_pps, myTT_agent.cal_fac, myTT_agent.old_cal_fac)


