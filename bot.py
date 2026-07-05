import os
import time
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件（本地测试用，Railway 上会自动读取系统环境变量）
load_dotenv()

# 从环境变量读取敏感信息（Railway 的 Variables 里设置）
TOKEN = os.environ.get('8838920602:AAE48G6wMxL5KlOpz1FYF_02Z-dPwNYJyqY')
API_KEY = os.environ.get('sk-MV3oIZvDiNOlv8r1nxGcilzHy3Vs9Kr28BxvNdQP5AEiEm3n')

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        print(f"发送消息失败: {e}")
        return None

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 25, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json().get("result", [])
    except Exception as e:
        print(f"获取更新失败: {e}")
        return []

def get_ai_response(user_message):
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://apihub.agnes-ai.com/v1"
        )
        system_prompt = """你是一个专业的美股投资教育助手。请按以下格式回答：

A. 简短结论：[一句话总结]

B. ETF组合：[推荐ETF及配置比例]

C. 风险说明：[列出3-5个风险点]

D. 图片生成提示词：[英文prompt用于生成配图]

E. 短视频脚本（60秒）：[三段式脚本]"""

        response = client.chat.completions.create(
            model="agnes-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 接口错误: {str(e)}"

def main():
    print("🚀 机器人启动中...")
    if not TOKEN:
        print("❌ 错误：TELEGRAM_BOT_TOKEN 未设置")
        return
    if not API_KEY:
        print("❌ 错误：AGNES_API_KEY 未设置")
        return

    print("✅ 机器人已启动，正在监听消息...")
    last_update_id = 0

    while True:
        try:
            updates = get_updates(offset=last_update_id + 1)
            for update in updates:
                last_update_id = update["update_id"]
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text")
                    if text:
                        print(f"收到消息: {text}")
                        if text == "/start":
                            send_message(chat_id, "🚀 欢迎使用美股投资教育助手！\n\n直接发送您的问题即可。")
                        else:
                            ai_reply = get_ai_response(text)
                            send_message(chat_id, ai_reply)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 机器人已停止")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()