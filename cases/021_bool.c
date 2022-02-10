void fun(float a, float b, float *c)
{
    bool p = a > b;

    if (p)
    {
        c = 1.0;
    }
    else
    {
        c = 2.0;
    }
}
