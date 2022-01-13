float fun(float a, float b, float &c)
{
    if (a == b)
    {
        c = 1 / 3.0 + 1 / 4.0 + 1 / 5.0;
    }
    else
    {
        c = a + b;
    }
}
