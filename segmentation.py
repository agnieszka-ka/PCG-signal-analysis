# -*- coding: utf-8 -*-
"""
Segmentation based on Shannon Energy.

@author: Agnieszka Kaczmarczyk
"""

import numpy as np
import matplotlib.pyplot as plt

def energy(signal_in):
    return [x**2 for x in signal_in]

def shannon_entrophy(signal_in):
    return [(-abs(x) * (logarithm(x))) for x in signal_in]
    
def shannon_energy(signal_in):
    return [((-(x**2)) * (logarithm(x**2))) for x in signal_in]    
    
def logarithm(x):
    if x == 0:
        return 0
    else:
        return np.log10(x)
        
def moving_average(signal_in, n = 100) :
    mov_av = np.zeros(len(signal_in))
    mov_av[0:n - 1] = signal_in[0:n - 1]
    for t in range(n - 1, len(mov_av)):
        mov_av[t] = np.average(signal_in[t - n + 1 : t])
    return mov_av

def shannon_energy_i(x):
    return ((-(x**2)) * (logarithm(x**2)))
    
def envelope(signal_in, freq, n = 0.05):
    shannon_envelope = np.zeros(len(signal_in))
    delta_t = n
    delta_t_frame = int(delta_t * freq)
    N = 2 * delta_t_frame + 1
    
    for x in range (delta_t_frame, (len(shannon_envelope) - delta_t_frame)):
        for tau in range(x - delta_t_frame, x + delta_t_frame):
            shannon_envelope[x] = shannon_envelope[x] + shannon_energy_i(signal_in[tau])
        shannon_envelope[x] = shannon_envelope[x] / N
        
    return shannon_envelope

def normalize_shannon(shannon_energy):
    m = np.average(shannon_energy)
    std = np.std(shannon_energy)
    return [((x - m)/ std) for x in shannon_energy]
    
def histogram_denoising(signal_in):
    n_bins = 100
    
    signal_out = np.copy(signal_in)
    
    plt.figure()
    n, bins, patches = plt.hist(abs(signal_out), n_bins, normed=1, histtype='step', cumulative=True)
    plt.close()

    index = 0
    thr = 0
    while n[index] < 0.96:
        thr = bins[index]
        index = index + 1
    
    for index in range(0, len(signal_out)):
        if abs(signal_out[index]) < thr:
            signal_out[index] = 0
            
    return signal_out

def heart_rate(signal, freq):
    autocorr = np.correlate(signal, signal, mode = 'full')
    autocorr = autocorr[autocorr.size/2:]
    autocorr = energy(autocorr)
    autocorr = envelope(autocorr, freq, 0.04)
    autocorr[0:(0.4 * freq)] = 0    # max freq is 150/min
    autocorr[(1.2 * freq):] = 0     # min freq is 50/min   
    autocorr = abs(autocorr)
    index = autocorr.argmax(axis=0)
    heart_rate = 60 * freq / index
    return heart_rate