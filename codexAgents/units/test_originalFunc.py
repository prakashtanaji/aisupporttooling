import sys
import unittest
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from originalFunc import calculateFinalCost


class CalculateFinalCostTests(unittest.TestCase):
    def test_calculate_final_cost_applies_discount(self):
        self.assertEqual(calculateFinalCost(100, 20), 80)


if __name__ == "__main__":
    unittest.main()
