#include <stdio.h>
#include <stdlib.h>
#include "pitch_detection.h"

int argmin(float *f)
{
    int min = f[0];
    int i, idx = 0;
    int size = sizeof(f);

    for (i = 1; i < size; i++)
    {
        if (f[i] < min)
        {
            min = f[i];
            idx = i++;
        }
    }

    return idx;
}

float ACF(float *f, int W, int t, int lag)
{
    float sum = 0.f;
    int i;

    for (i = 0; i < W; i++)
    {
        sum += f[i + t] * f[lag + i + t];
    }

    return sum;
}

float DF(float *f, int W, int t, int lag)
{
    return ACF(f, W, t, 0) + ACF(f, W, t + lag, 0) - (2 * ACF(f, W, t, lag));
}

void CMNDF_memo(float *f, int W, int t, int lag_max, float *vals)
{
    float sum = 0.f;
    int i;

    for (i = 0; i < lag_max; i++)
    {
        if (i == 0)
        {
            vals[i] = 1;
        }
        else
        {
            sum += DF(f, W, t, i);
            vals[i] = (DF(f, W, t, i) / sum) * i;
        }
    }
}

float detect_pitch(float *f, int W, int t, int sample_rate, int lbound, int rbound, float thresh)
{
    float *vals = NULL;
    vals = (float *)malloc(sizeof(float)*rbound);
    int i;

    CMNDF_memo(f, W, t, rbound, vals);
    vals = &vals[lbound];

    for (i = 0; i < rbound-lbound; i++)
    {
        if (vals[i] < thresh)
        {
            return (float)sample_rate / (float)(i + lbound + 1);
        }
    }

    return (float)sample_rate / (float)((argmin(vals) + lbound) + 1);
}