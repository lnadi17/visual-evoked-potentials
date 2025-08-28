import matplotlib.pyplot as plt

from ExperimentDataVEP import ExperimentDataVEP

plt.switch_backend('TkAgg')  # Interactive plots


def main():
    min_freq, max_freq = 0.5, 30
    # min_freq, max_freq = None, None
    data_luka = ExperimentDataVEP('2_vep_2025-08-05_06-51-40_1.xdf', min_frequency=min_freq, max_frequency=max_freq,
                                  bad_ch=None)
    data_wiko = ExperimentDataVEP('3_vep_2025-08-06_07-59-51_1.xdf', min_frequency=min_freq, max_frequency=max_freq,
                                  bad_ch='Pz')
    data_nani = ExperimentDataVEP('4_vep_2025-08-12_06-41-43_1.xdf', min_frequency=min_freq, max_frequency=max_freq,
                                  bad_ch=None)
    data_ucha = ExperimentDataVEP('7_vep_2025-08-25_08-38-32_1.xdf', min_frequency=min_freq, max_frequency=max_freq,
                                  bad_ch=None)
    data_sensor = ExperimentDataVEP('6_vep_2025-08-25_10-59-36_1.xdf', min_frequency=min_freq, max_frequency=max_freq,
                                    bad_ch=None)
    # picks = ['Pz', 'Oz', 'PO7', 'PO8']
    # picks = ['Fz']
    picks = 'eeg'

    def plot_data_for(dataset):
        dataset.plot_sensors()
        dataset.plot_all_channels(duration=10)
        dataset.plot_epochs()
        dataset.plot_compare_conditions(confidence_interval=0.5, picks=picks)
        standard = dataset._epochs["standard"].average()
        oddball = dataset._epochs["oddball"].average()
        standard.plot(gfp=True, spatial_colors=True)
        oddball.plot(gfp=True, spatial_colors=True)

    plot_data_for(data_ucha)


if __name__ == "__main__":
    main()
