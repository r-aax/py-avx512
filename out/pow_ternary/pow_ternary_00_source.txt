void pow_ternary(float a, float b, float *c)
{
    c = pow(a > b ? a : b, a < b ? a : b);
}
