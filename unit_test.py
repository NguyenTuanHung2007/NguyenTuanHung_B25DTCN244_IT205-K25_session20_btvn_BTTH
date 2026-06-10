import unittest
from BTTH import calculate_total_revenue

class TestTicketingSystem(unittest.TestCase):
    
    def test_revenue_with_mixed_status(self):
        # Case 1: Danh sách có cả vé Booked và Cancelled
        mock_data = [
            {"price": 500.0, "status": "Booked"},
            {"price": 300.0, "status": "Cancelled"},
            {"price": 200.0, "status": "Booked"}
        ]
        # Kết quả mong đợi: 500 + 200 = 700.0
        self.assertEqual(calculate_total_revenue(mock_data), 700.0)

    def test_revenue_empty_list(self):
        # Case 2: Danh sách trống
        self.assertEqual(calculate_total_revenue([]), 0.0)

    def test_revenue_all_cancelled(self):
        # Case 3: Tất cả vé đều hủy
        mock_data = [
            {"price": 100.0, "status": "Cancelled"},
            {"price": 200.0, "status": "Cancelled"}
        ]
        self.assertEqual(calculate_total_revenue(mock_data), 0.0)

if __name__ == "__main__":
    unittest.main()