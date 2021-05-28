
# ==================================================================================================

class Mask:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, n=16):
        """
        Constructor.

        :param n: count of elements
        """

        self.Id = 0
        self.T = 'm'
        self.N = 16
        self.E = [False] * self.N

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

        return 'ms{0:02}.{1:02}'.format(self.N, self.Id)

    # ----------------------------------------------------------------------------------------------

    def str_s(self):
        """
        Convert mask to string (short).

        :return: string
        """

        return self.id_str()

    # ----------------------------------------------------------------------------------------------

    def str_l(self):
        """
        Convert mask to string (long).

        :return: string
        """

        s = ['01'[e] for e in self.E]

        return '{0}:[{1}]'.format(self.id_str(), ''.join(s))

    # ----------------------------------------------------------------------------------------------

    def copy(self):
        """
        Copy of mask.

        :return: new mask
        """

        m = Mask(self.N)

        for i in range(self.N):
            m[i] = self[i]

        return m

# ==================================================================================================
