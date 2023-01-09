void fun(float kind,
         float r, float u, float v, float w, float p,
         float *ru, float *rv, float *rw, float *E)
{
    if (kind > 1.9)
    {
        ru = r * u;
        rv = r * v;
        rw = r * w;

        E = 0.5 * r * (u * u + v * v + w * w) + p / (1.4 - 1.0);
    }
}
