static void
prefun(float *f,
       float *fd,
       float p,
       float dk,
       float pk,
       float ck)
{
    float ak, bk, pratio, qrt;
    float G1 = 1;
    float G2 = 2;
    float G4 = 4;
    float G5 = 5;
    float G6 = 6;

    if (p <= pk)
    {
        pratio = p / pk;
        f = G4 * ck * (pow(pratio, G1) - 1.0);
        fd = (1.0 / (dk * ck)) * pow(pratio, -G2);
    }
    else
    {
        ak = G5 / dk;
        bk = G6 * pk;
        qrt = sqrt(ak / (bk + p));
        f = (p - pk) * qrt;
        fd = (1.0 - 0.5 * (p - pk) / (bk + p)) * qrt;
    }
}
