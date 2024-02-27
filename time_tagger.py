import TimeTagger

class time_tagger:
    def __init__(self) -> None:
        pass
        # Create a TimeTagger instance to control your hardware
        self.tagger = TimeTagger.createTimeTagger()
    def get

# Enable the test signal on channels 1 and 2
self.tagger.setTriggerLevel(1,0.1)
self.tagger.setTriggerLevel(2,0.1)
#tagger.setTestSignal([1, 2], True)
#tagger.setTestSignal()
event_buffer_size = 1000000

stream = TimeTagger.TimeTagStream(tagger=self.tagger,
                                  n_max_events=event_buffer_size,
                                  channels=[1, 2])



stream.start()
event_counter = 0
chunk_counter = 1
while stream.isRunning():
    data = stream.getData()
    if data.size > 0:
        # With the following methods, we can retrieve a numpy array for the particular information:
        channel = data.getChannels()            # The channel numbers
        timestamps = data.getTimestamps()       # The timestamps in ps
        overflow_types = data.getEventTypes()   # TimeTag = 0, Error = 1, OverflowBegin = 2, OverflowEnd = 3, MissedEvents = 4
        missed_events = data.getMissedEvents()  # The numbers of missed events in case of overflow
        total_missed_events = sum(missed_events)


        