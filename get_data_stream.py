"""The TimeTagStream measurement class"""

import TimeTagger
import numpy as np

WRChannel = 8
def subtract_WRtimestamps(channel, timestamps, WRChannel):
    # Initialize a variable to keep track of whether we're currently subtracting
    subtracting = False
    WR_timestamp = 0

    for i in range(len(channel)):
        if channel[i] == WRChannel:
            # If we find a new WRChannel, start subtracting from the next timestamps
            subtracting = True
            WR_timestamp = timestamps[i]
        elif subtracting:
            # Subtract the WR_timestamp from the timestamps
            timestamps[i] -= WR_timestamp

    return timestamps


def data_compression(channel, timestamp, overflow_types, WRChannel):
    # Ensure that the values fit within their respective bit ranges
    max_channel_bits = 0b111111  # 6 bits for channel
    max_event_bits = 0b111111    # 6 bits for event
    max_timestamp_bits = 0b1111111111111111111111111111111111111111111111111111 
    packed_data_bytes_list = []  # Create a list to collect the packed data bytes

    for i in range(len(channel)):
        if overflow_types[i] == 0:
            if channel[i] == WRChannel:
                event_indicator = 1
            else:
                event_indicator = 0

            channel[i] &= max_channel_bits
            event_indicator &= max_event_bits
            timestamp[i] &= max_timestamp_bits

            # Concatenate the values into a single numpy.int64
            packed_data = np.int64((channel[i] << 58) | (event_indicator << 52) | timestamp[i])
            # Convert packed_data to bytes for sending over the network
            packed_data_bytes = packed_data.tobytes()

            packed_data_bytes_list.append(packed_data_bytes)

        else:
            pass

    return packed_data_bytes_list

# Create a TimeTagger instance to control your hardware
tagger = TimeTagger.createTimeTagger()

# Enable the test signal on channels 1 and 2
tagger.setTestSignal([1, 2], True) 
#emulate the WR Signal
tagger.setTestSignal(WRChannel, True)
tagger.setEventDivider(WRChannel, 62500) #Emulate 1 Hz Signal



event_buffer_size = 10000000

stream = TimeTagger.TimeTagStream(tagger=tagger,
                                  n_max_events=event_buffer_size,
                                  channels=[1, 2, WRChannel])

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

        #reference the timestamps based on the WR time
        timestamps = subtract_WRtimestamps(channel, timestamps, WRChannel)
        packed_data_bytes_list = data_compression(channel=channel, timestamp=timestamps, overflow_types=overflow_types,WRChannel=WRChannel)
        print("done")
        

