float fun(float a, float b, float *c, float *d)
{
    if (a > b)
    {
        c = a + b;
    }
    else
    {
        c = a - b;
    }

    if (b < 2 * a)
    {
        d = a * b;
    }
    else
    {
        d = a / b;
    }
}
