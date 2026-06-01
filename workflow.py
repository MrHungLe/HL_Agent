import restate
from restate import Context
import llm
import tools

customer_service = restate.Service("CustomerServiceAgent")

@customer_service.handler()
async def process_chat(ctx: Context, message: str) -> str:
    analysis = await ctx.run(
        "analyze_intent",
        lambda: llm.analyze_customer_message(message)
    )

    action = analysis.get("action")

    if action == "call_tool":
        tool_name = analysis.get("tool_name")
        argument = analysis.get("tool_argument")
        tool_result = ""

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

        final_response = await ctx.run(
            "generate_final_answer",
            lambda: llm.generate_final_answer(message, tool_result)
        )
        return final_response

    elif action == "reply":
        return analysis.get("message", "Mình có thể giúp gì thêm cho bạn?")

    return "Yêu cầu chưa được xử lý, vui lòng thử lại."