
# ==================================================================================================
import random


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

        self.IsA = False
        self.IsR = False

    # ----------------------------------------------------------------------------------------------

    def set_arg(self):
        """
        Set flag that this register is argument.
        """

        self.IsA = True

    # ----------------------------------------------------------------------------------------------

    def set_res(self):
        """
        Set flag that this register is result.
        """

        self.IsR = True

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

        # return 'z{0}{1:02}.{2:02}'.format(self.T, self.N, self.Id)

        if self.IsA:
            ch = 'a'
        elif self.IsR:
            ch = 'r'
        else:
            ch = 'v'

        return '{0}{1:02}'.format(ch, self.Id)

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

        s = ['{0:8}'.format(round(e, 5)) for e in self.E]

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

    # ----------------------------------------------------------------------------------------------

    def zero_element(self, i):
        """
        Set element to zero.

        :param i: index
        """

        if (self.T == 'f') or (self.T == 'd'):
            self[i] = 0.0
        elif self.T == 'i':
            self[i] = 0
        else:
            raise Exception('Unknown type of ZMM register.')

    # ----------------------------------------------------------------------------------------------

    def set_all_elements(self, v):
        """
        Set all elements with the given value.

        :param v: value
        """

        for i in range(self.N):
            self[i] = v

    # ----------------------------------------------------------------------------------------------

    def set_elements(self, vs):
        """
        Set elements with array of values.

        :param vs: array of values
        """

        for i in range(min(self.N, len(vs))):
            self[i] = vs[i]

    # ----------------------------------------------------------------------------------------------

    def set_elements_random(self, low=0.0, hi=1.0):
        """
        Set random values to register.

        :param low: low border of random values
        :param hi: high border of random values
        """

        for i in range(self.N):
            self[i] = random.uniform(low, hi)

# ==================================================================================================
