#ifndef PITCH_DETECTION_H_
#define PITCH_DETECTION_H_

/**
 * @brief \n Finds the index of the minimum value in the array.
 * @note \n REPLACE: With ARM's or AVR's argmin implementation.
 * 
 * @param arr \n A float array.
 * @return int \n The index of the minimum value of the array.
 */
int argmin(float *arr);

/**
 * @brief \n The auto-correlation function for pitch detection.
 * 
 * @param f \n Points to a float array of samples.
 * @param W \n Window size: how many samples to check for periodicity.
 * @param t \n Time delay: how far into the samples are we.
 * @param lag \n How much does the correlator lag by?
 * @return float \n The autocorrelated value.
 */
float ACF(float *f, int W, int t, int lag);

/**
 * @brief The difference function.
 * 
 * @param f \n Points to a float array of samples.
 * @param W \n Window size: how many samples to check for periodicity.
 * @param t \n Time delay: how far into the samples are we.
 * @param lag \n How much does the correlator lag by?
 * @return float \n The difference function value.
 */
float DF(float *f, int W, int t, int lag);

/**
 * @brief A memoized version of the cumulative-mean, normalized difference function.
 * 
 * @param f \n Points to a float array of samples.
 * @param W \n Window size: how many samples to check for periodicity.
 * @param t \n Time delay: how far into the samples are we.
 * @param lag \n How much does the correlator lag by?
 * @param[out] vals \n 
 */
void CMNDF_memo(float *f, int W, int t, int lag_max, float *vals);

/**
 * @brief Wraps around CMNDF_memo to detect pitches.
 * 
 * @param f \n Points to a float array of samples.
 * @param W \n Window size: how many samples to check for periodicity.
 * @param t \n Time delay: how far into the samples are we.
 * @param sample_rate \n Sample rate of the audio.
 * @param lbound \n Lower bound for lag.
 * @param rbound \n Upper bound for lag.
 * @param thresh \n A threshold to account for harmonics. Typ. values between 0.1 and 0.5
 * @return float \n A frequency in Hz, the detected pitch of the note at time t.
 */
float detect_pitch(float *f, int W, int t, int sample_rate, int lbound, int rbound, float thresh);

#endif //PITCH_DETECTION_H_