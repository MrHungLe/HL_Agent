import restate
from restate import Context
import llm
import tools

# 1. Khởi tạo đối tượng Service chính xác (chữ S viết hoa)
customer_service = restate.Service("CustomerServiceAgent")

# 2. Dùng decorator từ đối tượng vừa tạo, BỎ CLASS và BỎ biến 'self'
@customer_service.handler()
async def process_chat(ctx: Context, message: str) -> str:
    # Bước 1: Phân tích ý định (Bọc trong ctx.run để lưu trạng thái)
    analysis = await ctx.run(
        "analyze_intent",
        lambda: llm.analyze_customer_message(message)
    )

    action = analysis.get("action")

    # Bước 2: Xử lý nếu cần gọi Tool
    if action == "call_tool":
        tool_name = analysis.get("tool_name")
        argument = analysis.get("tool_argument")
        tool_result = ""

        # Thực thi tool an toàn thông qua Restate
        if tool_name == "check_inventory":
            tool_result = await ctx.run(
                f"call_inventory_{argument}",
                lambda: tools.check_inventory(argument)
            )
        elif tool_name == "check_order_status":
            tool_result = await ctx.run(
                f"call_order_{argument}",
                lambda: tools.check_order_status(argument)
            )
        else:
            tool_result = "Không tìm thấy công cụ tương ứng."

        # Bước 3: Tổng hợp câu trả lời cuối cùng
        final_response = await ctx.run(
            "generate_final_answer",
            lambda: llm.generate_final_answer(message, tool_result)
        )
        return final_response

    # Xử lý nếu LLM tự trả lời được luôn
    elif action == "reply":
        return analysis.get("message", "Mình có thể giúp gì thêm cho bạn?")

    return "Yêu cầu chưa được xử lý, vui lòng thử lại."