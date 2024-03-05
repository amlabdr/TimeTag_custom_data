import json
import numpy as np

# Assuming you have a list of channels
channels = [1, 2]  # Add more channels as needed

for ch in channels:
    file_name = f'channel_{ch}_data.json'

    with open(file_name, 'r') as file:
        for line in file:
            data = json.loads(line)

            inner_dict_key = next(iter(data))
            array_size = len(data[inner_dict_key])
            array_data = data[inner_dict_key]

            print(f"Received {array_size} elements for channel: {ch}")

            # Print the first 3 elements
            print(f"{inner_dict_key}: array({array_data[:3]}, ...,")

            # Print the last 3 elements
            print(f"..., {array_data[-3:]})")
    
    print("===========")
