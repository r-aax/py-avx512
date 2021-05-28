
# ==================================================================================================

class Mask:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, n=16):
        """
        Constructor.

        :param n: count of elements
        """

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

    def __repr__(self):
        """
        Convert mask to string.

        :return: string
        """

        s = ['01'[e] for e in self.E]

        return 'mask-{0:2}:[{1}]'.format(self.N, ''.join(s))

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
