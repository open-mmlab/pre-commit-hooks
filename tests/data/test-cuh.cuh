#include <math.h>

#include <iostream>
// Kernel function to add the elements of two arrays
__global__ void add(int n, float *x, float *y) {
  for (int i = 0; i < n; i++) y[i] = x[i] + y[i];
}
