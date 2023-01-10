void fun(float p, float r, float u, float v, float w,
         float *fp_r, float *fp_ru, float *fp_rv, float *fp_rw, float *fp_E,
         float *fn_r, float *fn_ru, float *fn_rv, float *fn_rw, float *fn_E)
{
    float GAMMA = 1.4;
    float a = sqrt(GAMMA * p / r);
    float l1 = u - a;
    float l2 = u;
    float l5 = u + a;
    float lp1 = 0.5 * (l1 + abs(l1));
    float lp2 = 0.5 * (l2 + abs(l2));
    float lp5 = 0.5 * (l5 + abs(l5));
    float ln1 = 0.5 * (l1 - abs(l1));
    float ln2 = 0.5 * (l2 - abs(l2));
    float ln5 = 0.5 * (l5 - abs(l5));
    float k = 0.5 * r / GAMMA;
    float V2 = u * u + v * v + w * w;
    float H = 0.5 * V2 + a * a / (GAMMA - 1.0);

    fp_r = k * (lp1 + 2.0 * (GAMMA - 1.0) * lp2 + lp5);
    fp_ru = k * ((u - a) * lp1 + 2.0 * (GAMMA - 1.0) * u * lp2 + (u + a) * lp5);
    fp_rv = k * (v * lp1 + 2.0 * (GAMMA - 1.0) * v * lp2 + v * lp5);
    fp_rw = k * (w * lp1 + 2.0 * (GAMMA - 1.0) * w * lp2 + w * lp5);
    fp_E = k * ((H - u * a) * lp1 + (GAMMA - 1.0) * V2 * lp2 + (H + u * a) * lp5);
    fn_r = k * (ln1 + 2.0 * (GAMMA - 1.0) * ln2 + ln5);
    fn_ru = k * ((u - a) * ln1 + 2.0 * (GAMMA - 1.0) * u * ln2 + (u + a) * ln5);
    fn_rv = k * (v * ln1 + 2.0 * (GAMMA - 1.0) * v * ln2 + v * ln5);
    fn_rw = k * (w * ln1 + 2.0 * (GAMMA - 1.0) * w * ln2 + w * ln5);
    fn_E = k * ((H - u * a) * ln1 + (GAMMA - 1.0) * V2 * ln2 + (H + u * a) * ln5);
}
