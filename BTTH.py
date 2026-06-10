import logging
import unittest

logging.basicConfig(
    filename='arena_tickets.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def calculate_total_revenue(tickets):
    total = 0.0
    for ticket in tickets:
        try:
            if ticket.get("status") == "Booked":
                total += float(ticket.get("price", 0.0))
        except (ValueError, TypeError, KeyError):
            continue
    return total

def display_tickets(tickets):
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    logging.info("User viewed ticket list.")
    print("\n--- DANH SÁCH VÉ ---")
    print(f"{'Mã Vé':<6} | {'Tên Khách Hàng':<18} | {'Giá Vé':<8} | {'Chỗ Ngồi':<8} | {'Trạng Thái'}")
    print("-" * 75)
    
    try:
        for t in tickets:
            t_id = t["ticket_id"]
            name = t["buyer_name"]
            price = t["price"]
            status = t["status"]
            area, seat_num = t["seat"]
            
            status_display = status
            if status == "Cancelled":
                status_display += " [ĐÃ HỦY]"
                
            print(f"{t_id:<6} | {name:<18} | {price:<8.1f} | {area}-{seat_num:<8} | {status_display}")
    except KeyError as e:
        logging.error(f"Missing key while displaying ticket: {e}")
        print("\nLỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
    
    print("-" * 75)

def book_ticket(tickets):
    print("\n--- ĐẶT VÉ MỚI ---")
    t_id = input("Nhập mã vé: ").strip().upper()
    
    exists = False
    for t in tickets:
        if t.get("ticket_id") == t_id:
            exists = True
            break
            
    if exists:
        print(f"Lỗi: Mã vé {t_id} đã tồn tại.")
        logging.warning(f"Duplicate ticket ID entered: {t_id}")
        return

    name = input("Nhập tên khách hàng: ").strip()
    
    while True:
        try:
            price = float(input("Nhập giá vé: "))
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")

    area = input("Nhập khu vực ghế: ").strip().upper()
    
    while True:
        try:
            seat_num = int(input("Nhập số ghế: "))
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    new_ticket = {
        "ticket_id": t_id,
        "buyer_name": name,
        "price": price,
        "status": "Booked",
        "seat": (area, seat_num)
    }
    tickets.append(new_ticket)
    print(f"Thành công: Đã đặt vé {t_id} cho khách hàng {name}.")
    logging.info(f"Booked new ticket {t_id} for {name}")

def change_seat(tickets):
    print("\n--- ĐỔI CHỖ NGỒI ---")
    t_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()
    
    target = None
    for t in tickets:
        if t.get("ticket_id") == t_id:
            target = t
            break
            
    if not target:
        print(f"Không tìm thấy vé mang mã {t_id}.")
        logging.warning(f"Change seat failed - Ticket {t_id} not found")
        return

    new_area = input("Nhập khu vực ghế mới: ").strip().upper()
    
    while True:
        try:
            new_num = int(input("Nhập số ghế mới: "))
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    target["seat"] = (new_area, new_num)
    print(f"Thành công: Đã đổi chỗ vé {t_id} sang {new_area}-{new_num}.")
    logging.info(f"Seat changed for ticket {t_id} to {new_area}-{new_num}")

def cancel_ticket(tickets):
    print("\n--- HỦY VÉ ---")
    t_id = input("Nhập mã vé cần hủy: ").strip().upper()
    
    target = None
    for t in tickets:
        if t.get("ticket_id") == t_id:
            target = t
            break
            
    if not target:
        print(f"Không tìm thấy vé mang mã {t_id}.")
        logging.warning(f"Cancel ticket failed - Ticket {t_id} not found")
        return

    if target["status"] == "Cancelled":
        print(f"Vé {t_id} đã ở trạng thái Cancelled trước đó.")
    else:
        target["status"] = "Cancelled"
        print(f"Thành công: Vé {t_id} đã được hủy.")
        logging.warning(f"Ticket {t_id} has been cancelled.")

def calculate_revenue_report(tickets):
    print("\n--- BÁO CÁO DOANH THU ---")
    
    booked = 0
    cancelled = 0
    for t in tickets:
        if t.get("status") == "Booked":
            booked += 1
        elif t.get("status") == "Cancelled":
            cancelled += 1
            
    try:
        for t in tickets:
            if "price" not in t:
                raise KeyError("price")
                
        revenue = calculate_total_revenue(tickets)
        print(f"Tổng số vé đã đặt: {booked}")
        print(f"Tổng số vé đã hủy: {cancelled}")
        print(f"Tổng doanh thu hợp lệ: {revenue:,.1f}")
        logging.info(f"Revenue report generated. Total: {revenue}")
    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        print("Tổng doanh thu hợp lệ: 0.0")
        logging.error(f"Missing key while calculating revenue: {e}")

class TestTicketing(unittest.TestCase):
    def test_revenue(self):
        sample = [
            {"price": 500.0, "status": "Booked"},
            {"price": 300.0, "status": "Cancelled"},
            {"price": 500.0, "status": "Booked"}
        ]
        self.assertEqual(calculate_total_revenue(sample), 1000.0)
        self.assertEqual(calculate_total_revenue([]), 0.0)

if __name__ == "__main__":
    ticket_db = [
        {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
        {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
        {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
    ]

    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
        print("1. Xem danh sách vé đã bán")
        print("2. Đặt vé mới")
        print("3. Đổi chỗ ngồi (Cập nhật vé)")
        print("4. Hủy vé")
        print("5. Báo cáo doanh thu")
        print("6. Thoát chương trình")
        print("========================================")
        
        choice = input("Chọn chức năng (1-6): ")
        
        if choice == "1":
            display_tickets(ticket_db)
        elif choice == "2":
            book_ticket(ticket_db)
        elif choice == "3":
            change_seat(ticket_db)
        elif choice == "4":
            cancel_ticket(ticket_db)
        elif choice == "5":
            calculate_revenue_report(ticket_db)
        elif choice == "6":
            print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
            logging.info("Ticket management system closed.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-6.")
            logging.warning("Invalid menu choice selected")