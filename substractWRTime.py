import numpy as np

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

# Sample data for demonstration
channel = np.array([1, 2, 8, 3, 4, 8, 5, 1, 1, 2, 8, 3, 4, 8, 5, 1], dtype=np.intc)
timestamps = np.array([100, 200, 300, 400, 500, 600, 700, 800, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800], dtype=np.int64)

# Specify the WRChannel (e.g., 8)
WRChannel = 8

# Call the function to subtract timestamps
modified_timestamps = subtract_WRtimestamps(channel, timestamps, WRChannel)

print("Original timestamps:", timestamps)
print("Modified timestamps:", modified_timestamps)
