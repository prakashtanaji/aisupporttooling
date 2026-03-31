import sys
import unittest
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from originalFunc import calculateFinalCost


class CalculateFinalCostTests(unittest.TestCase):
    def test_calculate_final_cost_applies_discount(self):
        self.assertEqual(calculateFinalCost(100, 20), 80)

    def test_calculate_final_cost_with_zero_discount_returns_original_price(self):
        self.assertEqual(calculateFinalCost(100, 0), 100)

    def test_calculate_final_cost_without_discount_uses_zero(self):
        self.assertEqual(calculateFinalCost(100), 100)

    def test_calculate_final_cost_with_full_discount_returns_zero(self):
        self.assertEqual(calculateFinalCost(100, 100), 0)

    def test_calculate_final_cost_supports_decimal_price(self):
        self.assertAlmostEqual(calculateFinalCost(99.99, 15), 84.9915)

    def test_calculate_final_cost_supports_decimal_discount(self):
        self.assertEqual(calculateFinalCost(100, 12.5), 87.5)

    def test_calculate_final_cost_with_zero_price_returns_zero(self):
        self.assertEqual(calculateFinalCost(0, 25), 0)

    def test_calculate_final_cost_with_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculateFinalCost(-100, 20)

    def test_calculate_final_cost_with_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculateFinalCost(100, -20)

    def test_calculate_final_cost_with_discount_over_hundred_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculateFinalCost(100, 120)

    def test_calculate_final_cost_raises_type_error_for_string_price(self):
        with self.assertRaises(TypeError):
            calculateFinalCost("100", 20)

    def test_calculate_final_cost_with_none_discount_treats_it_as_zero(self):
        self.assertEqual(calculateFinalCost(100, None), 100)


if __name__ == "__main__":
    unittest.main()
