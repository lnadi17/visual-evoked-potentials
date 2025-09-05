import os

import pyxdf


class ExperimentData:
    def _read_metadata(self, original_filename):
        # Read info of the first stream
        info = self._xdf_data[0]['info']
        self.metadata = {
            "effective_sample_rate": info['effective_srate'],
            # "subject": {
            #     # "name": info['desc'][0]['subject'][0]['name'][0],
            #     # "alertness": info['desc'][0]['subject'][0]['alertness'][0],
            #     "id": info['desc'][0]['subject'][0]['id'][0],
            #     "group": info['desc'][0]['subject'][0]['group'][0],
            #     "session": info['desc'][0]['subject'][0]['session'][0]
            # },
            "markers": list(set(self.marker_data)),
            # "experiment_variant": info['desc'][0]['experiment'][0]['variant'][0],
            "original_filename": original_filename
        }

    def _read_eeg_data(self):
        # Read data of the first stream
        self.eeg_time = self._xdf_data[0]['time_stamps']
        # self._time_offset = min(self.eeg_time)
        self._time_offset = 0  # Assume already aligned
        self.eeg_time = self.eeg_time - self._time_offset
        self.eeg_data = self._xdf_data[0]['time_series'][:, :8]
        # self.accelerometer_data = self._xdf_data[0]['time_series'][:, 8:11]
        # self.gyroscope_data = self._xdf_data[0]['time_series'][:, 11:14]
        # self.battery_level_data = self._xdf_data[0]['time_series'][:, 14]
        # self.counter_data = self._xdf_data[0]['time_series'][:, 15]
        # self.validation_indicator_data = self._xdf_data[0]['time_series'][:, 16]

    def _read_marker_data(self):
        # Read data of the second stream
        self.marker_time = self._xdf_data[1]['time_stamps']
        self.marker_time = self.marker_time - self._time_offset
        self.marker_data = [x[0] for x in self._xdf_data[1]['time_series']]

    def __init__(self, xdf_path):
        self._xdf_data = pyxdf.load_xdf(xdf_path)[0]
        # self._xdf_data = pyxdf.load_xdf(xdf_path, synchronize_clocks=False, dejitter_timestamps=False)[0]
        self._xdf_data[0], self._xdf_data[1] = self._xdf_data[1], self._xdf_data[0]  # Swap streams if needed
        self._read_eeg_data()
        self._read_marker_data()
        self._read_metadata(os.path.basename(xdf_path))
