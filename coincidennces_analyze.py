import numpy as np
import matplotlib.pyplot as plt
import json


class Coincidences():
    def __init__(self, Alice, Bob) -> None:
        self.Alice = Alice
        self.Bob = Bob

    def findpeak(self, bins=100):
        # Ensure both arrays have the same length
        min_length = min(len(self.Alice), len(self.Bob))
        Alice_trimmed = self.Alice[:min_length]
        Bob_trimmed = self.Bob[:min_length]

        # Calculate the histogram of time delays
        delays = Alice_trimmed - Bob_trimmed
        hist, bin_edges = np.histogram(delays, bins=bins)

        # Find the index of the peak in the histogram
        peak_index = np.argmax(hist)

        # Calculate the delay corresponding to the peak
        peak_delay = (bin_edges[peak_index] + bin_edges[peak_index + 1]) / 2

        return peak_delay
    
    def coincidences_count(self, peak_delay):
        # Subtract the peak delay from the time stamps in Alice and Bob arrays
        Alice_shifted = self.Alice - peak_delay
        Bob_shifted = self.Bob

        # Calculate coincidences rate (counting the number of coincident events)
        coincidences_count = np.sum(np.isclose(Alice_shifted, Bob_shifted, rtol=1e-5, atol=1e-8))
        

        return coincidences_count
