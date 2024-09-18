import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

data = 20 + 10 * np.sin(np.linspace(0, 2 * np.pi, 1440)) + np.random.normal(0, 2, 1440)

b, a = butter(4, 0.03, btype='low')
smoothed_data = filtfilt(b, a, data)

hourly_avg = np.mean(smoothed_data.reshape(24, 60), axis=1)

time = np.arange(1440)
plt.plot(time, data, label='Noisy Data', alpha=0.5)
plt.plot(time, smoothed_data, label='Smoothed Data', linewidth=2)
plt.scatter(np.arange(0, 1440, 60), hourly_avg, color='red', label='Hourly Averages', zorder=5)

threshold = 20
exceeds_threshold = smoothed_data > threshold
exceeds_intervals = np.split(exceeds_threshold, np.where(np.diff(exceeds_threshold) != 0)[0]+1)
for interval in exceeds_intervals:
    if len(interval) > 20 and np.all(interval):
        plt.axvspan(time[np.where(exceeds_threshold)[0][0]], time[np.where(exceeds_threshold)[0][-1]], color='orange', alpha=0.3)

plt.legend()
plt.show()
