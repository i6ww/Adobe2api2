import requests
import time

# 服务器地址
BASE_URL = "http://127.0.0.1:6001"
# API密钥
API_KEY = "123456"

# 新添加的比例列表
new_ratios = [
    "21x9",  # 21:9
    "3x2",   # 3:2
    "5x4",   # 5:4
    "4x5",   # 4:5
    "2x3",   # 2:3
    "8x1",   # 8:1
    "1x4",   # 1:4
    "1x8"    # 1:8
]

def generate_image_with_ratio(ratio_suffix):
    """使用指定比例的模型生成图片"""
    url = f"{BASE_URL}/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建模型ID
    model_id = f"firefly-nano-banana2-1k-{ratio_suffix}"
    
    # 请求体
    data = {
        "model": model_id,
        "prompt": f"A beautiful landscape with {ratio_suffix} aspect ratio",
        "n": 1  # 生成一张图片
    }
    
    try:
        print(f"\n正在测试模型: {model_id}")
        print(f"提示词: {data['prompt']}")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查响应状态
        
        result = response.json()
        
        print(f"OK 生成成功!")
        print(f"  创建时间: {result['created']}")
        print(f"  使用模型: {result['model']}")
        
        # 打印生成的图片URL
        for i, image in enumerate(result['data']):
            print(f"  图片 {i+1} URL: {image['url']}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR 生成失败: {e}")
        try:
            # 尝试获取错误响应
            error_data = response.json()
            print(f"  错误信息: {error_data['error']['message']}")
        except:
            pass
        return False

def main():
    """测试所有新比例的模型"""
    print("=== 测试所有新比例的图片模型 ===")
    print(f"总共有 {len(new_ratios)} 个新比例需要测试")
    print("\n开始测试...")
    
    success_count = 0
    failure_count = 0
    
    for ratio in new_ratios:
        success = generate_image_with_ratio(ratio)
        if success:
            success_count += 1
        else:
            failure_count += 1
        
        # 避免请求过快，添加短暂延迟
        time.sleep(2)
    
    print("\n=== 测试结果 ===")
    print(f"成功: {success_count}/{len(new_ratios)}")
    print(f"失败: {failure_count}/{len(new_ratios)}")
    
    if failure_count == 0:
        print("OK 所有新比例模型测试通过!")
    else:
        print("ERROR 部分模型测试失败，需要检查")

if __name__ == "__main__":
    main()
