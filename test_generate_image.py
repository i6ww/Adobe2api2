import requests

# 服务器地址
BASE_URL = "http://43.165.172.5:6001"
# API密钥
API_KEY = "123456"

def generate_image():
    """使用指定模型生成图片"""
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 请求体
    data = {
        "model": "flux",
        "messages": [
            {"role": "user", "content": "a cinematic mountain sunrise"}
        ]
    }
    
    try:
        print("正在生成图片...")
        print(f"模型: {data['model']}")
        print(f"提示词: {data['messages'][0]['content']}")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查响应状态
        
        result = response.json()
        
        print("\n=== 生成结果 ===")
        print(f"创建时间: {result['created']}")
        print(f"使用模型: {result['model']}")
        print(f"ID: {result['id']}")
        
        # 打印生成的图片URL
        for i, choice in enumerate(result['choices']):
            print(f"\n选择 {i+1}:")
            print(f"消息: {choice['message']['content']}")
            print(f"完成原因: {choice['finish_reason']}")
        
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
