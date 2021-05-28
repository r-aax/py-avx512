
# ==================================================================================================

class ZMM:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, t):
        """
        Constructor.

        ZMM register may be created with one of the following types:
            'f' - 16 elements of float32,
            'd' -  8 elements of float64,
            'i' - 16 elements of int32.

        :param t: type
        """

        if t == 'f':
            self.T = 'f'
            self.N = 16
            self.E = [0.0] * self.N
        elif t == 'd':
            self.T = 'd'
            self.N = 8
            self.E = [0.0] * self.N
        elif t == 'i':
            self.T = 'i'
            self.N = 16
            self.E = [0] * self.N
        else:
            raise Exception('Unknown ZMM type.')

    # ----------------------------------------------------------------------------------------------

    def __repr__(self):
        """
        Convert to string.

        :return: string
        """

        s = ['{0:5}'.format(e) for e in self.E]

        return 'zmm{0}-{1:02}:[{2}]'.format(self.T, self.N, ', '.join(s))

# ==================================================================================================
