from time import time
import numpy as np
from experiments.experiment import Experiment
from supplement.definitions import const


class Ridme_5p_rect(Experiment):
    ''' Class for 5-pulse RIDME with rectangular pulses '''
    
    def __init__(self, name):
        super().__init__(name)
        self.technique = 'ridme'
        self.frequency_increment_bandwidth = 0.001 # in GHz
    
    def set_parameters(self, magnetic_field, detection_frequency, detection_pulse_lengths, mixing_time, temperature):
        ''' Sets the parameters of an experiment '''
        self.magnetic_field = magnetic_field
        self.detection_frequency = detection_frequency
        self.detection_pi_half_pulse_length = detection_pulse_lengths[0]
        self.detection_pi_pulse_length = detection_pulse_lengths[1]
        self.mixing_time = mixing_time
        self.temperature = temperature
        self.bandwidth_detection_pi_half_pulse = 1 / (4 * self.detection_pi_half_pulse_length)
        self.bandwidth_detection_pi_pulse = 1 / (2 * self.detection_pi_pulse_length)

    def detection_probability(self, resonance_frequencies, weights=[]):
        ''' Computes pump probabilities for different resonance frequencies '''
        frequency_offsets_squared = (self.detection_frequency - resonance_frequencies)**2
        rabi_frequencies_pi_half_pulse = np.sqrt(frequency_offsets_squared + self.bandwidth_detection_pi_half_pulse**2)
        rabi_frequencies_pi_pulse = np.sqrt(frequency_offsets_squared + self.bandwidth_detection_pi_pulse**2)
        # This equation needs to be validated by theory!!!
        detection_probabilities = (self.bandwidth_detection_pi_half_pulse / rabi_frequencies_pi_half_pulse)**3 * np.sin(2*np.pi * rabi_frequencies_pi_half_pulse * self.detection_pi_half_pulse_length)**3 * \
                                  0.25 * (self.bandwidth_detection_pi_pulse / rabi_frequencies_pi_pulse) ** 4 * (1 - np.cos(2*np.pi * rabi_frequencies_pi_pulse * self.detection_pi_pulse_length))**2
        if weights != []:
            pump_probabilities = pump_probabilities * weights.reshape(weights.size,1)
            pump_probabilities = pump_probabilities.sum(axis=0)
        return detection_probabilities.flatten()

    def pump_probability(self, T1, g_anisotropy, g_eff):
        ''' Computes pump probabilities for different g-factors '''
        if g_anisotropy:
            exp_factor = np.exp(-g_eff * const['bohr_magneton'] * self.magnetic_field / (const['bolzmann_constant'] * self.temperature))
            pump_probabilities = 2 * exp_factor / (1 + exp_factor)**2 * (1 - np.exp(-self.mixing_time/T1))
            return pump_probabilities
        else:
            pump_probability = 0.5 * (1 - np.exp(-self.mixing_time/T1))
            return pump_probability * np.ones(g_eff.size)
        
    def get_detection_bandwidth(self, ranges=()):
        ''' Computes the bandwidth of detection pulses '''
        if ranges == ():
            frequencies = np.arange(self.detection_frequency - 10 * self.bandwidth_detection_pi_half_pulse, self.detection_frequency + 10 * self.bandwidth_detection_pi_half_pulse, self.frequency_increment_bandwidth)
        else:
            frequencies = np.arange(ranges[0], ranges[1], self.frequency_increment_bandwidth)
        probabilities = self.detection_probability(frequencies)
        detection_bandwidth = {}
        detection_bandwidth['f'] = frequencies
        detection_bandwidth['p'] = probabilities
        return detection_bandwidth