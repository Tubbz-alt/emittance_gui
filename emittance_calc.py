import math
import numpy as np
import numpy.matlib


# model_rMatElement
# This class is used to set the matrix elements
# sigma matrices, quad matrices, drift matrix
class model_rMatElement:
    # drift matrix
    L = 0.560  # temporary value for L (from ppt)
    M_drift = np.identity(2)
    M_drift[0, 1] = L

    def __init__(self, d, par):
        self.d = d
        self.par = par

    # for quadrupole
    def qu(self):

        kx2 = self.par(1)
        M_quad = np.identity(2)
        M_quad[1, 0] = kx2
        ky2 = -kx2

        # Setting the quad matrix
        kx = math.sqrt(kx2)
        ky = math.sqrt(ky2)
        phix = kx * self.d
        phiy = ky * self.d

        # if np.logical_not(any(kx)):  # Thin Lens approximation
        mx1 = np.transpose([[1, self.d]])
        mx2 = np.transpose([[0, 1]])

        mx = np.zeros(4)
        mx[0, 0] = mx1[0]
        mx[0, 1] = mx1[1]
        mx[1, 0] = mx2[0]
        mx[1, 1] = mx2[1]
        # else:
        #     mx1 = np.transpose([[np.cos(phix), self.d * np.sinc(phix)]])
        #     mx2 = np.transpose([[-kx * np.sin(phix), np.cos(phix)]])

        # if np.logical_not(any(ky)):
        my1 = np.transpose([1, self.d])
        my2 = np.transpose([0, 1])
        # else:
        #     my1 = np.transpose([np.cos(phiy), self.d * np.sinc(phiy)])
        #     my2 = np.transpose([-ky * np.sin(phiy), np.cos(phiy)])

        screen_matrix = self.par  # ???? check
        transformation_matrix = np.matmul(self.M_drift, mx)
        solution_matrix = np.matmul(np.linalg.inv(transformation_matrix), screen_matrix)

        r = np.identity(4)
        r[0, 0] = mx1[0]
        r[0, 1] = mx1[1]
        r[1, 0] = mx2[0]
        r[1, 1] = mx2[1]
        r[2, 2] = my1[0]
        r[2, 3] = my1[1]
        r[3, 2] = my2[0]
        r[3, 3] = my2[1]

        return r

    # for solenoid
    def so(self):

        kx2 = (self.par(1) / 2) ** 2
        ky2 = kx2

        # Setting the quad matrix
        kx = math.sqrt(kx2)
        ky = math.sqrt(ky2)
        phix = kx * self.d
        phiy = ky * self.d
        if np.logical_not(any(kx)):  # Thin Lens approximation
            mx1 = np.transpose([[1, self.d]])
            mx2 = np.transpose([[0, 1]])
        else:
            mx1 = np.transpose([[np.cos(phix), self.d * np.sinc(phix)]])
            mx2 = np.transpose([[-kx * np.sin(phix), np.cos(phix)]])

        if np.logical_not(any(ky)):
            my1 = np.transpose([1, self.d])
            my2 = np.transpose([0, 1])
        else:
            my1 = np.transpose([np.cos(phiy), self.d * np.sinc(phiy)])
            my2 = np.transpose([-ky * np.sin(phiy), np.cos(phiy)])

        r = np.identity(6)
        r[0, 0] = mx1[0]
        r[0, 1] = mx1[1]
        r[1, 0] = mx2[0]
        r[1, 1] = mx2[1]
        r[2, 2] = my1[0]
        r[2, 3] = my1[1]
        r[3, 2] = my2[0]
        r[3, 3] = my2[1]

        return r


# calculates the sigma matrix
# uses model_rMatElement
# r = Transport Matrices - [2 x 2 x N] size
# sizes = vector of sqrt(sigma11) measurements
def beamAnalysis_sigmaFit(r, sizes):
    sizes = np.array(sizes)
    sizesStd = np.array([])

    use = np.logical_not(np.isnan(sizes) + np.isinf(sizes)).astype(int)
    data = sizes ** 2

    if (not sizesStd) or np.logical_not(all(sizesStd.flatten())):
        sizesStd = sizes * 0 + 0.05 * np.mean(sizes)
        if sum(use) > 3:
            sizesStd = []

    if sizesStd:
        dataStd = 2 * np.transpose(sizes[np.logical_not(np.isnan(sizes) + np.isinf(sizes))]).reshape(3, 1) * sizesStd
    else:
        dataStd = []

    r = np.array(r)
    r = np.transpose(np.reshape(r, (4, -1)))
    m = np.transpose([r[:, 0] ** 2, 2 * r[:, 0] * r[:, 2], r[:, 2] ** 2])
    m = m[0:use.size, ]
    sigma = np.zeros((np.size(m, 1), 1))

    if np.sum(use) > 2:
        weight = 1 / dataStd ** 2
        sigma = np.linalg.lstsq(m * np.sqrt(weight[:, ]), data * np.sqrt(weight))[0]

    return sigma


# computes beta, alpha, from sigma matrix
# def model_sigma2Twiss(sig, sigCov, energy):
def model_sigma2Twiss(sig, energy):
    e0 = 0.511e-3
    sig = np.array(sig)

    if not energy:  # if there is no input for energy
        energy = e0

    gam = np.transpose(energy) / e0
    twiss = sig * 0

    eps = np.sqrt(sig[0, :] * sig[2, :] - np.square(sig[1, :]))
    twiss = [[eps * gam], [sig[0, :] / eps], [-sig[1, :] / eps]]
    twiss = np.nan_to_num(np.real(twiss))

    return twiss


# calculates the emittance and twiss parameters
def emittance_process(d, var, data, plane, energy, twiss0):
    # for qu: par=k^2=K1=GL/L/Brho [1/m^2]
    # for sol: par=2k=BL/L/Brho [1/m]
    test = model_rMatElement(d, var)  # insert d, par before running
    r = test.qu()

    par = beamAnalysis_sigmaFit(r, data)

    e0 = 0.511e-3
    gam = energy / e0
    if plane < 3:
        twiss0 = twiss0[:, plane]
    else:
        twiss0 = np.mean(twiss0, 2)

    eps = twiss0(1) / gam
    twiss = model_sigma2Twiss(par, energy)

    return twiss


# test if model_sigma2Twiss works
twiss = model_sigma2Twiss([[0.434, 0.3327, 0.2390], [0.1692, 0.1617, 0.2248], [0.3207, 0.4289, 0]])
print(twiss)

twiss = emittance_process(data, 1, 135, twiss)
