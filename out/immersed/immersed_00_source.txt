void fun(float xl, float xr, float yl, float yr, float zl, float zr,
         float sph_x, float sph_y, float sph_z, float sph_r,
         float *kind)
{
    float dxl2 = (xl - sph_x) * (xl - sph_x);
    float dxr2 = (xr - sph_x) * (xr - sph_x);
    float dyl2 = (yl - sph_y) * (yl - sph_y);
    float dyr2 = (yr - sph_y) * (yr - sph_y);
    float dzl2 = (zl - sph_z) * (zl - sph_z);
    float dzr2 = (zr - sph_z) * (zr - sph_z);
    float r2 = sph_r * sph_r;
    float lll_in = (dxl2 + dyl2 + dzl2 <= r2) ? 1.0 : 0.0;
    float llr_in = (dxl2 + dyl2 + dzr2 <= r2) ? 1.0 : 0.0;
    float lrl_in = (dxl2 + dyr2 + dzl2 <= r2) ? 1.0 : 0.0;
    float lrr_in = (dxl2 + dyr2 + dzr2 <= r2) ? 1.0 : 0.0;
    float rll_in = (dxr2 + dyl2 + dzl2 <= r2) ? 1.0 : 0.0;
    float rlr_in = (dxr2 + dyl2 + dzr2 <= r2) ? 1.0 : 0.0;
    float rrl_in = (dxr2 + dyr2 + dzl2 <= r2) ? 1.0 : 0.0;
    float rrr_in = (dxr2 + dyr2 + dzr2 <= r2) ? 1.0 : 0.0;
    float in_cnt = lll_in + llr_in + lrl_in + lrr_in + rll_in + rlr_in + rrl_in + rrr_in;
    float xc = (xl + xr) / 2.0;
    float yc = (yl + yr) / 2.0;
    float zc = (zl + zr) / 2.0;

    if (in_cnt == 0.0)
    {
        kind = 0.0;
    }
    else if (in_cnt == 8.0)
    {
        kind = 1.0;
    }
    else
    {
        if ((xc - sph_x) * (xc - sph_x) + (yc - sph_y) * (yc - sph_y) + (zc - sph_z) * (zc - sph_z) <= r2)
        {
            kind = 2.0;
        }
        else
        {
            kind = 3.0;
        }
    }
}