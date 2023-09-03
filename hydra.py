from math import sqrt, pow

class Hydra:

    def __init__(self, height):
        self.height = height
        self.cells = []
        self.layers = []
        self.muscles = []

    def calc_volume(self):
        vol = 0
        for i in range(1, len(self.layers)):
            l11, l12 = self.layers[i - 1]
            l21, l22 = self.layers[i]

            l11 = l11.body.position
            l12 = l12.body.position
            l21 = l21.body.position
            l22 = l22.body.position

            vol += calc_volume_quad(l11, l12, l21, l22)
        return vol

def calc_volume_quad(p11, p12, p21, p22):
    return calc_volume_tri(p11, p12, p21) + calc_volume_tri(p12, p21, p22)

def calc_volume_tri(p1, p2, p3):
    s1 = p1 - p2
    s2 = p2 - p3
    s3 = p3 - p1
    s1 = s1.length
    s2 = s2.length
    s3 = s3.length
    return (s2 * sqrt(s1**2 - ((s1**2 + s2**2 - s3**2) / (2*s2))**2)) / 2

