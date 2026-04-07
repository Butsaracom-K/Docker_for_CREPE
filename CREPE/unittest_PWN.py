import unittest
from constants import *
from equations import e_max, d11, rdiff, Q0, pulsar, etaW0
from boundaries_setup import *
from single_PWN_setup import initial1, initial2, initial3

class TestPWNModel(unittest.TestCase):
    def setUp(self):
        """ Set Parameters for Test Case"""
        self.en = 100          # GeV                   [Vary - 0.5 GeV - 14 TeV Obs.]
        self.delta = delta     # No unit               [Constant - DRAGON2 Code]
        self.d0 = d0           # m^2/s                 [Constant - DRAGON2 Code]
        self.e0 = e0           # GeV                   [Constant - Paper]
        self.td = 1e5          # years                 [ATNF Catalogue]
        self.edot = 1e34       # erg/s                 [ATNF Catalogue]
        self.d = 0.2           # kpc                   [ATNF Catalogue]
        self.gamma = 2.0       # No unit               [Free parm. emcee]
        self.e_cut = 1000      # GeV                   [Free parm. emcee]
        self.eta = 0.1         # Efficiency [~10%]     [Free parm. emcee]

    def test_e_max_positive(self):
        """Energy max >= 0"""
        em = e_max(self.td)
        self.assertGreater(em.value, 0)
    
    def test_d11_scaling(self):
        """Test Diffusion coefficient vary due to Energy (If delta > 0)"""
        d_low = d11(10, self.d0, self.e0, self.delta)
        d_high = d11(100, self.d0, self.e0, self.delta)
        self.assertGreater(d_high, d_low)

    def test_rdiff_non_nan(self):
        """Test rdiff not in NaN or Complex for normal calculation"""
        rd = rdiff(self.en, self.delta, self.d0, self.e0, self.td)
        self.assertFalse(np.isnan(rd.value))
        self.assertGreaterEqual(rd.value, 0)

    def test_q0_integration(self):
        """Test Q0 are able to calculate (Integration part work!)"""
        q = Q0(self.gamma, self.e_cut, self.eta, self.edot, self.td)
        self.assertIsInstance(q.value, float)
        self.assertGreater(q.value, 0)

    def test_pulsar_heaviside(self):
        """Test Heaviside: If Energy > e_max; model = 0"""
        em_val = e_max(self.td).value
        # Test at high Energy
        model_val = pulsar(em_val + 1000000, self.gamma, self.e_cut, self.eta, 
                           self.edot, self.td, self.delta, self.d0, self.e0, self.d)
        self.assertEqual(model_val, 0)

class TestinitialBounds(unittest.TestCase):
    def setUp(self):
        """Test inital for each case that the initial not exceed to bounds."""
        self.gamma_Young_LB, self.e_cut_Young_LB, self.eta_Young_LB  = gamma_Young_LB, e_cut_Young_LB, eta_Young_LB
        self.gamma_Young_UB, self.e_cut_Young_UB, self.eta_Young_UB = gamma_Young_UB, e_cut_Young_UB, eta_Young_UB
        ##
        self.gamma_Middle_LB, self.e_cut_Middle_LB, self.eta_Middle_LB = gamma_Middle_LB, e_cut_Middle_LB, eta_Middle_LB
        self.gamma_Middle_UB, self.e_cut_Middle_UB, self.eta_Middle_UB = gamma_Middle_UB, e_cut_Middle_UB, eta_Middle_UB
        ##
        self.gamma_Old_LB, self.e_cut_Old_LB, self.eta_Old_LB = gamma_Old_LB, e_cut_Old_LB, eta_Old_LB
        self.gamma_Old_UB, self.e_cut_Old_UB, self.eta_Old_UB = gamma_Old_UB, e_cut_Old_UB, eta_Old_UB

    def test_initial1(self):
        assert self.gamma_Young_LB <= initial1[0] <= self.gamma_Young_UB, "initial for Young PWN should not exceed bound."
        assert self.e_cut_Young_LB <= initial1[1] <= self.e_cut_Young_UB, "initial for Young PWN should not exceed bound."
        assert self.eta_Young_LB <= initial1[2] <= self.eta_Young_UB, "initial forYoung PWN should not exceed bound."
        #return print("inital1 not exceed boundaries")
    
    def test_initial2(self):
        assert self.gamma_Middle_LB <= initial2[0] <= self.gamma_Middle_UB, "initial for Middle PWN should not exceed bound."
        assert self.e_cut_Middle_LB <= initial2[1] <= self.e_cut_Middle_UB, "initial for Middle PWN should not exceed bound."
        assert self.eta_Middle_LB <= initial2[2] <= self.eta_Middle_UB, "initial for Middle PWN should not exceed bound."
        #return print("inital2 not exceed boundaries")
    
    def test_initial3(self):
        assert self.gamma_Old_LB <= initial3[0] <= self.gamma_Old_UB, "initial for Old PWN should not exceed bound."
        assert self.e_cut_Old_LB <= initial3[1] <= self.e_cut_Old_UB, "initial for Old PWN should not exceed bound."
        assert self.eta_Old_LB <= initial3[2] <= self.eta_Old_UB, "initial for Old PWN should not exceed bound."
        #return print("inital3 not exceed boundaries")
    
if __name__ == '__main__':
    unittest.main()
