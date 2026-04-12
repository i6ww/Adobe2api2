import requests

# 服务器地址
BASE_URL = "http://127.0.0.1:6001"
# API密钥
API_KEY = "123456"

def get_models():
    """获取模型列表"""
    url = f"{BASE_URL}/v1/models"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查响应状态
        
        data = response.json()
        print("\n=== 模型列表 ===")
        print(f"总模型数: {len(data['data'])}")
        print("\n支持的模型:")
        
        # 按类型分组打印
        image_models = []
        video_models = []
        
        for model in data['data']:
            model_id = model['id']
            description = model['description']
            
            if model_id.startswith('firefly-sora2') or model_id.startswith('firefly-veo31'):
                video_models.append((model_id, description))
            else:
                image_models.append((model_id, description))
        
        # 打印图像模型
        print("\n--- 图像模型 ---")
        for model_id, description in image_models:
            print(f"- {model_id}: {description}")
        
        # 打印视频模型
        print("\n--- 视频模型 ---")
        for model_id, description in video_models:
            print(f"- {model_id}: {description}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

if __name__ == "__main__":
    print("正在获取模型列表...")
    get_models()
