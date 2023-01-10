float fun(float a, float b, float *c)
{
    if (a > b)
    {
        c = a + b + 0.5;
    }
    else if (a < b)
    {
        c = a - b - 0.5;
    }
    else
    {
        c = a * b;
    }
}
