import unittest
import numpy as np
from simulation_matrix.cases.bhd_preexperiment import qfi_metric

class BHDPreExperimentTests(unittest.TestCase):
    def test_h01_benchmark(self):
        ref=np.array([[3.4028,-7.3136],[-7.3136,20.5808]])
        self.assertLessEqual(np.max(np.abs(qfi_metric(1.0,0.1)-ref)),0.08)
    def test_h001_benchmark(self):
        ref=np.array([[1.8032,-9.4046],[-9.4046,275.6538]])
        self.assertLessEqual(np.max(np.abs(qfi_metric(1.0,0.01)-ref)),0.08)

if __name__=="__main__":
    unittest.main()
