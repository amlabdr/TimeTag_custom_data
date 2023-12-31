"""import numpy as np
import sys
channel_number_value = 2
event_indicator_value = 0
timestamp_value = 1803273693449
# Define your channel number, event indicator, and timestamp
channel_number = np.int32(channel_number_value)       # Assume channel_number_value is your value
event_indicator = np.int32(event_indicator_value)     # Assume event_indicator_value is your value
timestamp = np.int64(timestamp_value)                 # Assume timestamp_value is your value

channel_number_size = sys.getsizeof(channel_number)
event_indicator_size = sys.getsizeof(event_indicator)
timestamp_size = sys.getsizeof(timestamp)

# Ensure that the values fit within their respective bit ranges
max_channel_bits = 0b111111  # 6 bits for channel
max_event_bits = 0b111111    # 6 bits for event
max_timestamp_bits = 0b1111111111111111111111111111111111111111111111111111  # 52 bits for timestamp

channel_number &= max_channel_bits
event_indicator &= max_event_bits
timestamp &= max_timestamp_bits

# Concatenate the values into a single numpy.int64
packed_data = np.int64((channel_number << 58) | (event_indicator << 52) | timestamp)

# Convert packed_data to bytes for sending over the network
packed_data_bytes = packed_data.tobytes()

# Now you can send packed_data_bytes over the network using a suitable communication method
print(packed_data_bytes)
packed_data_bytes_size = sys.getsizeof(packed_data_bytes)
print("Size of channel_number (bytes):", channel_number_size)
print("Size of event_indicator (bytes):", event_indicator_size)
print("Size of timestamp (bytes):", timestamp_size)
print("Size of packed_data_bytes (bytes):", packed_data_bytes_size)

# Store packed_data_bytes in a binary file
with open("packed_data.bin", "wb") as binary_file:
    binary_file.write(packed_data_bytes)

# Calculate the size of the binary file
import os

file_size = os.path.getsize("packed_data.bin")

# Print the size
print("Size of packed_data.bin (bytes):", file_size)

# Clean up: remove the binary file
#os.remove("packed_data.bin")



# Assuming you have received the packed data as bytes over the network
received_data_bytes = packed_data_bytes  # Replace with the actual received bytes


# Convert the received bytes back to a numpy.int64
received_data = np.frombuffer(received_data_bytes, dtype=np.int64)[0]

# Convert received_data to a regular Python integer (int)
received_data = int(received_data)

# Extract the components
timestamp_mask = 0xFFFFFFFFFFFFF  # Mask for extracting the 52-bit timestamp
event_mask = 0x3F0000000000000    # Mask for extracting the 6-bit event indicator
channel_mask = 0xFC00000000000000  # Mask for extracting the 6-bit channel number

timestamp = received_data & timestamp_mask
event_indicator = (received_data & event_mask) >> 52
channel_number = (received_data & channel_mask) >> 58  # Right-shift by 58 bits

# Now you have the individual components extracted
print("Channel Number:", channel_number)
print("Event Indicator:", event_indicator)
print("Timestamp:", timestamp)
"""


import numpy as np

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


def unpack_packed_data(packed_data_bytes):
    # Convert the received bytes back to a numpy.int64
    received_data = np.frombuffer(packed_data_bytes, dtype=np.int64)[0]
    # Extract the components
    timestamp_mask =  0xFFFFFFFFFFFFF  # Mask for extracting the 52-bit timestamp
    event_mask =    0x3F0000000000000    # Mask for extracting the 6-bit event indicator
    channel_mask =  0xFF0000000000000  #0xFC00000000000000  # Mask for extracting the 6-bit channel number

    timestamp = received_data & timestamp_mask
    event_indicator = (received_data & event_mask) >> 52
    channel_number = (received_data & channel_mask) >> 58  # Right-shift by 58 bits

    return channel_number, event_indicator, timestamp
# Sample data for demonstration
channel = np.array([1, 2, 8, 3, 4, 8, 5], dtype=np.intc)
timestamps = np.array([100, 200, 300, 400, 500, 600, 700], dtype=np.int64)
overflow_types = [0, 0, 0, 0, 0, 0, 0]  # Example overflow types
WRChannel = 8

# Call the function
packed_data_bytes_list = data_compression(channel, timestamps, overflow_types, WRChannel)

# Print the list of packed data bytes
for packed_data_bytes in packed_data_bytes_list:
    print("Packed Data Bytes:", packed_data_bytes)
    print("unpack teh data bytes:")
    # Call the function to unpack the data
    channel_number, event_indicator, timestamp = unpack_packed_data(packed_data_bytes)

    print("Channel Number:", channel_number)
    print("Event Indicator:", event_indicator)
    print("Timestamp:", timestamp)



