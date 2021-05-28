
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

        self.Id = 0

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

    def __getitem__(self, item):
        """
        Get item override.

        :param item: index
        :return: element of the mask
        """

        return self.E[item]

    # ----------------------------------------------------------------------------------------------

    def __setitem__(self, key, value):
        """
        Set item override.

        :param key: key
        :param value: value
        """

        self.E[key] = value

    # ----------------------------------------------------------------------------------------------

    def id_str(self):
        """
        Identifier string.

        :return: string
        """

        return 'z{0}{1:02}.{2:02}'.format(self.T, self.N, self.Id)

    # ----------------------------------------------------------------------------------------------

    def str_s(self):
        """
        Convert to string (short).

        :return: string
        """

        return self.id_str()

    # ----------------------------------------------------------------------------------------------

    def str_l(self):
        """
        Convert to string (long).

        :return: string
        """

        s = ['{0:5}'.format(e) for e in self.E]

        return '{0}:[{1}]'.format(self.id_str(), ', '.join(s))

    # ----------------------------------------------------------------------------------------------

    def copy(self):
        """
        Copy of register.

        :return: copy
        """

        zmm = ZMM(self.T)

        for i in range(self.N):
            zmm[i] = self[i]

        return zmm

# ==================================================================================================
