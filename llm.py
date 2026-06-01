import json
from google import genai
from google.genai import types
from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

SYSTEM_INSTRUCTION = """
Bạn là AI Agent tư vấn sản phẩm và chăm sóc khách hàng chuyên nghiệp cho cửa hàng.
Nhiệm vụ của bạn là phân tích tin nhắn của khách hàng và phản hồi theo đúng định dạng được yêu cầu.

PHẠM VI HỖ TRỢ:
- Chỉ hỗ trợ các vấn đề liên quan đến tư vấn sản phẩm (tồn kho, giá cả, khuyến mãi) và trạng thái đơn hàng (tra cứu mã đơn hàng).
- Tuyệt đối KHÔNG trả lời các câu hỏi ngoài phạm vi này (ví dụ: kiến thức chung, chính trị, thời tiết, lập trình, toán học, dịch thuật, thơ ca, hoặc các sản phẩm/dịch vụ của bên khác).

ĐỊNH DẠNG PHẢN HỒI (Bắt buộc luôn luôn trả về JSON):

1. Nếu bạn cần thông tin từ hệ thống để trả lời (như kiểm tra kho, kiểm tra đơn hàng), trả về định dạng JSON:
{
  "action": "call_tool",
  "tool_name": "check_inventory" HOẶC "check_order_status",
  "tool_argument": "tên sản phẩm hoặc mã đơn hàng cụ thể"
}

2. Nếu câu hỏi nằm trong phạm vi (hỏi xã giao, cảm ơn, chào hỏi, hoặc bạn đã có đủ thông tin về sản phẩm/đơn hàng để trả lời trực tiếp), trả về định dạng JSON:
{
  "action": "reply",
  "message": "Nội dung câu trả lời thân thiện, lịch sự bằng tiếng Việt"
}

3. Nếu câu hỏi NẰM NGOÀI PHẠM VI hỗ trợ (hỏi kiến thức chung, code, toán, thời tiết, chính trị,...), bạn PHẢI từ chối lịch sự và hướng khách hàng quay lại chủ đề hỗ trợ. Trả về định dạng JSON:
{
  "action": "reply",
  "message": "Xin lỗi bạn, tôi là trợ lý ảo chuyên hỗ trợ tư vấn sản phẩm và tra cứu đơn hàng của cửa hàng. Tôi không thể hỗ trợ các thông tin ngoài phạm vi này. Bạn có cần tôi giúp gì về sản phẩm hay kiểm tra đơn hàng không ạ?"
}
"""

def analyze_customer_message(message: str) -> dict:
    """Gọi Gemini để phân tích ý định khách hàng và ra quyết định chọn Tool"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error calling analyze_customer_message: {e}")
        err_msg = str(e).upper()
        if "QUOTA" in err_msg or "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            return {
                "action": "reply",
                "message": "⚠️ [Giới hạn API]: Tài khoản của bạn đã hết lượt sử dụng Gemini API miễn phí trong ngày hôm nay (giới hạn của Free Tier là 20 requests/ngày). Xin vui lòng thử lại sau hoặc nâng cấp/thay thế GOOGLE_API_KEY trong file .env nhé!"
            }
        return {"action": "reply", "message": "Xin lỗi, hệ thống đang bận. Bạn vui lòng thử lại nhé!"}

def generate_final_answer(customer_message: str, tool_result: str) -> str:
    """Dùng thông tin từ Tool để Gemini tổng hợp thành câu trả lời tự nhiên"""
    prompt = f"Tin nhắn khách: {customer_message}\nDữ liệu hệ thống cung cấp: {tool_result}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="Bạn là AI chăm sóc khách hàng. Hãy tổng hợp dữ liệu hệ thống thành một câu trả lời ngắn gọn, thuyết phục và lịch sự."
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling generate_final_answer: {e}")
        err_msg = str(e).upper()
        if "QUOTA" in err_msg or "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            return "⚠️ [Giới hạn API]: Tài khoản đã hết lượt sử dụng Gemini API miễn phí trong ngày (giới hạn 20 requests/ngày). Vui lòng cấu hình API Key mới trong .env hoặc thử lại sau!"
        return f"Hệ thống đã nhận được dữ liệu: {tool_result}. Tuy nhiên việc tạo câu trả lời tự nhiên đang gặp gián đoạn tạm thời. Rất xin lỗi bạn vì sự bất tiện này!"