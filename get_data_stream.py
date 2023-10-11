"""The TimeTagStream measurement class"""

import TimeTagger

def calibrate():
    return 1
def referenceTimeStamps():
    return 1
# Create a TimeTagger instance to control your hardware
tagger = TimeTagger.createTimeTagger()

# Enable the test signal on channels 1 and 2
tagger.setTestSignal([1, 2], True)

event_buffer_size = 1000000

stream = TimeTagger.TimeTagStream(tagger=tagger,
                                  n_max_events=event_buffer_size,
                                  channels=[1, 2])

while stream.isRunning():
    data = stream.getData()
    if data.size == event_buffer_size:
        print('TimeTagStream buffer is filled completely. Events arriving after the buffer has been filled have been discarded. Please increase the buffer size not to miss any events.')
    if data.size > 0:
        # With the following methods, we can retrieve a numpy array for the particular information:
        channel = data.getChannels()            # The channel numbers
        timestamps = data.getTimestamps()       # The timestamps in ps
        overflow_types = data.getEventTypes()   # TimeTag = 0, Error = 1, OverflowBegin = 2, OverflowEnd = 3, MissedEvents = 4
        #do calibration
        calibrate()
        #reference the timestamps based on the WR time
        referenceTimeStamps()
        

