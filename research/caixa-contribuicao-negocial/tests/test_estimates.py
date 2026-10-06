import unittest

from src.estimate import contribution_bounds, largest_remainder


class EstimateTests(unittest.TestCase):
    def test_largest_remainder_preserves_target_total(self):
        historical = {"AC": 293, "AL": 1110, "SP": 22219}
        allocated = largest_remainder(historical, 1000)
        self.assertEqual(sum(allocated.values()), 1000)
        self.assertEqual(set(allocated), set(historical))

    def test_contribution_bounds_use_tst_salary_limits(self):
        result = contribution_bounds(100, minimum=63.00, maximum=310.00, union_share=0.70)
        self.assertEqual(result["gross_min"], 6300.00)
        self.assertEqual(result["gross_max"], 31000.00)
        self.assertEqual(result["union_min"], 4410.00)
        self.assertEqual(result["union_max"], 21700.00)

    def test_zero_employees_produces_zero_bounds(self):
        result = contribution_bounds(0, minimum=63.00, maximum=310.00, union_share=0.70)
        self.assertEqual(result["gross_min"], 0.00)
        self.assertEqual(result["gross_max"], 0.00)
        self.assertEqual(result["union_min"], 0.00)
        self.assertEqual(result["union_max"], 0.00)

    def test_negative_employee_count_is_rejected(self):
        with self.assertRaises(ValueError):
            contribution_bounds(-1, minimum=63.00, maximum=310.00, union_share=0.70)


if __name__ == "__main__":
    unittest.main()
