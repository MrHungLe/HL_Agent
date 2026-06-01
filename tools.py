# Giả lập database hoặc API hệ thống
PRODUCTS_DB = {
    "giày running x": "Còn 5 đôi size 42, giá 1.500.000đ. Đang có khuyến mãi tặng tất.",
    "áo khoác gió": "Hết hàng màu đen, chỉ còn màu xanh size L. Giá 500.000đ.",
    "balo du lịch": "Còn 10 chiếc tại kho Hà Nội, kho HCM hết hàng."
}

ORDERS_DB = {
    "ORD123": "Đơn hàng đang được vận chuyển. Dự kiến giao vào chiều mai.",
    "ORD456": "Đơn hàng đã giao thành công vào ngày 28/05/2026."
}

def check_inventory(product_name: str) -> str:
    """Tra cứu tình trạng kho hàng"""
    name_lower = product_name.lower()
    for key, info in PRODUCTS_DB.items():
        if key in name_lower:
            return f"[Hệ thống Kho]: {info}"
    return f"[Hệ thống Kho]: Không tìm thấy sản phẩm '{product_name}'."

def check_order_status(order_id: str) -> str:
    """Tra cứu trạng thái đơn hàng cho khách"""
    oid = order_id.upper().strip()
    if oid in ORDERS_DB:
        return f"[Hệ thống Đơn hàng]: {ORDERS_DB[oid]}"
    return f"[Hệ thống Đơn hàng]: Không tìm thấy mã đơn hàng {order_id}."