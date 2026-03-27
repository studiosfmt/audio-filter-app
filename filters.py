import numpy as np
from scipy import signal

def apply_fir_filter(audio_data, cutoff_freq, fs, order=101):
    """
    Applies a low-pass FIR filter to the audio signal.
    
    Args:
        audio_data (np.ndarray): The input audio signal.
        cutoff_freq (float): The cutoff frequency for the low-pass filter.
        fs (int): The sampling frequency of the audio.
        order (int): The number of taps in the FIR filter (must be odd).
        
    Returns:
        np.ndarray: The filtered audio signal.
    """
    # Ensure order is odd for Type I FIR filter
    if order % 2 == 0:
        order += 1
        
    # Design the FIR filter using the window method
    nyquist = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyquist
    
    # Create the filter coefficients (taps)
    taps = signal.firwin(order, normalized_cutoff, window='hamming')
    
    # Apply the filter using lfilter
    filtered_audio = signal.lfilter(taps, 1.0, audio_data)
    
    return filtered_audio.astype(np.float32)

def apply_lms_filter(desired_signal, reference_noise, mu=0.01, filter_order=32):
    """
    Applies a Least Mean Squares (LMS) adaptive filter for noise cancellation.
    
    Args:
        desired_signal (np.ndarray): The noisy signal (speech + noise).
        reference_noise (np.ndarray): A signal correlated with the noise in the desired signal.
        mu (float): The learning rate (step size).
        filter_order (int): The number of weights/taps in the adaptive filter.
        
    Returns:
        tuple: (clean_signal_estimate, error_signal, weights)
    """
    n_samples = len(desired_signal)
    # Ensure reference noise has the same length
    if len(reference_noise) < n_samples:
        reference_noise = np.pad(reference_noise, (0, n_samples - len(reference_noise)))
    else:
        reference_noise = reference_noise[:n_samples]
        
    # Initialize weights and output arrays
    weights = np.zeros(filter_order)
    output_signal = np.zeros(n_samples)
    error_signal = np.zeros(n_samples)
    
    # Adaptive filter loop
    for n in range(filter_order, n_samples):
        # Extract the current window of the reference signal (sliding window)
        # x = [r[n], r[n-1], ..., r[n-order+1]]
        x = reference_noise[n : n - filter_order : -1]
        
        # Calculate filter output: y[n] = w^T * x
        y = np.dot(weights, x)
        output_signal[n] = y
        
        # Calculate error: e[n] = d[n] - y[n]
        e = desired_signal[n] - y
        error_signal[n] = e
        
        # Update weights: w[n+1] = w[n] + mu * e[n] * x[n]
        # (Standard LMS update rule)
        weights = weights + mu * e * x
        
    return error_signal.astype(np.float32)

def normalize_audio(audio_data):
    """
    Normalizes audio data to be between -1.0 and 1.0.
    """
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        return audio_data / max_val
    return audio_data
