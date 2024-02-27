import TimeTagger

# Create a TimeTagger instance to control your hardware
tagger = TimeTagger.createTimeTagger()

# Enable the test signal on channels 1 and 2
tagger.setTriggerLevel(1,0.1)
tagger.setTriggerLevel(2,0.1)
#tagger.setTestSignal([1, 2], True)
#tagger.setTestSignal()
event_buffer_size = 1000000

stream = TimeTagger.TimeTagStream(tagger=tagger,
                                  n_max_events=event_buffer_size,
                                  channels=[1, 2])




stream.start()
while stream.isRunning():
    data = stream.getData()
    if data.size > 0:
        # With the following methods, we can retrieve a numpy array for the particular information:
        channel = data.getChannels()            # The channel numbers
        timestamps = data.getTimestamps()       # The timestamps in ps
        overflow_types = data.getEventTypes()   # TimeTag = 0, Error = 1, OverflowBegin = 2, OverflowEnd = 3, MissedEvents = 4
        missed_events = data.getMissedEvents()  # The numbers of missed events in case of overflow
        total_missed_events = sum(missed_events)



        