import requests

# 服务器地址
BASE_URL = "http://43.165.172.5:6001"
# API密钥
API_KEY = "123456"

def generate_image():
    """使用指定模型生成图片"""
    url = f"{BASE_URL}/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 请求体
    data = {
        "model": "firefly-nano-banana-pro-1k-16x9",
        "prompt": "A beautiful sunset over the mountains, with a lake in the foreground and pine trees on the hillside",
        "n": 1  # 生成一张图片
    }
    
    try:
        print("正在生成图片...")
        print(f"模型: {data['model']}")
        print(f"提示词: {data['prompt']}")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查响应状态
        
        result = response.json()
        
        print("\n=== 生成结果 ===")
        print(f"创建时间: {result['created']}")
        print(f"使用模型: {result['model']}")
        
        # 打印生成的图片URL
        for i, image in enumerate(result['data']):
            print(f"\n图片 {i+1}:")
            print(f"URL: {image['url']}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        try:
            # 尝试获取错误响应
            error_data = response.json()
            print(f"错误信息: {error_data['error']['message']}")
        except:
            pass
        return None

if __name__ == "__main__":
    generate_image()
