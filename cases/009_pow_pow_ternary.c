void pow_ternary(float a, float b, float *c)
{
    c = pow(pow(a > b ? a : b, a < b ? a : b), pow(a > b ? a : b, a < b ? a : b));
}
