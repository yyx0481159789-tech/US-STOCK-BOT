import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/getMe"

# 代理配置（改成你的端口）
proxies = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}

def test_proxy_stability(times=20, timeout=15):
    """测试代理稳定性：连续请求 times 次，统计成功次数和响应时间"""
    success = 0
    response_times = []

    print(f"🚀 开始测试代理稳定性，共 {times} 次请求，超时 {timeout} 秒")
    print("=" * 50)

    for i in range(times):
        start = time.time()
        try:
            r = requests.get(URL, proxies=proxies, timeout=timeout)
            elapsed = (time.time() - start) * 1000  # 毫秒
            if r.status_code == 200:
                success += 1
                response_times.append(elapsed)
                print(f"✅ 第 {i+1:2d} 次成功 | 耗时: {elapsed:.0f} ms")
            else:
                print(f"❌ 第 {i+1:2d} 次失败 | HTTP状态码: {r.status_code}")
        except requests.exceptions.Timeout:
            print(f"❌ 第 {i+1:2d} 次失败 | 超时 (> {timeout} 秒)")
        except Exception as e:
            print(f"❌ 第 {i+1:2d} 次失败 | 错误: {str(e)[:50]}")
        
        # 间隔 1 秒，模拟真实轮询频率
        if i < times - 1:
            time.sleep(1)

    print("=" * 50)
    print(f"📊 测试结果：成功 {success}/{times} 次，成功率 {success/times*100:.1f}%")
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        print(f"⏱️  响应时间：平均 {avg_time:.0f} ms | 最快 {min_time:.0f} ms | 最慢 {max_time:.0f} ms")
    
    if success / times < 0.8:
        print("\n⚠️ 稳定性较差，建议：")
        print("  - 更换速游VPN的节点")
        print("  - 检查代理软件是否开启了UDP转发")
        print("  - 尝试关闭防火墙或添加允许规则")
    else:
        print("\n✅ 代理稳定，可以运行机器人！")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ 未找到 TELEGRAM_BOT_TOKEN，请在 .env 文件中设置")
    else:
        test_proxy_stability(times=20, timeout=15)