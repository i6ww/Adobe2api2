from __future__ import annotations

import time
from typing import Optional


def size_from_ratio(ratio: str, output_resolution: str = "2K") -> dict:
    level = (output_resolution or "2K").upper()
    if level == "1K":
        ratio_map = {
            "1:1": {"width": 1024, "height": 1024},
            "16:9": {"width": 1360, "height": 768},
            "9:16": {"width": 768, "height": 1360},
            "4:3": {"width": 1152, "height": 864},
            "3:4": {"width": 864, "height": 1152},
            "21:9": {"width": 1418, "height": 608},
            "3:2": {"width": 1280, "height": 854},
            "5:4": {"width": 1024, "height": 819},
            "4:5": {"width": 819, "height": 1024},
            "2:3": {"width": 854, "height": 1280},
            "8:1": {"width": 1024, "height": 128},
            "1:4": {"width": 256, "height": 1024},
            "1:8": {"width": 128, "height": 1024},
        }
    elif level == "4K":
        ratio_map = {
            "1:1": {"width": 4096, "height": 4096},
            "16:9": {"width": 5504, "height": 3072},
            "9:16": {"width": 3072, "height": 5504},
            "4:3": {"width": 4096, "height": 3072},
            "3:4": {"width": 3072, "height": 4096},
            "21:9": {"width": 5672, "height": 2432},
            "3:2": {"width": 5120, "height": 3413},
            "5:4": {"width": 4096, "height": 3277},
            "4:5": {"width": 3277, "height": 4096},
            "2:3": {"width": 3413, "height": 5120},
            "8:1": {"width": 4096, "height": 512},
            "1:4": {"width": 1024, "height": 4096},
            "1:8": {"width": 512, "height": 4096},
        }
    else:
        ratio_map = {
            "1:1": {"width": 2048, "height": 2048},
            "16:9": {"width": 2752, "height": 1536},
            "9:16": {"width": 1536, "height": 2752},
            "4:3": {"width": 2048, "height": 1536},
            "3:4": {"width": 1536, "height": 2048},
            "21:9": {"width": 2836, "height": 1216},
            "3:2": {"width": 2560, "height": 1707},
            "5:4": {"width": 2048, "height": 1638},
            "4:5": {"width": 1638, "height": 2048},
            "2:3": {"width": 1707, "height": 2560},
            "8:1": {"width": 2048, "height": 256},
            "1:4": {"width": 512, "height": 2048},
            "1:8": {"width": 256, "height": 2048},
        }
    return ratio_map.get(ratio, ratio_map["16:9"])


def build_image_payload_candidates(
    *,
    prompt: str,
    aspect_ratio: str,
    output_resolution: str,
    upstream_model_id: str,
    upstream_model_version: str,
    source_image_ids: Optional[list[str]] = None,
) -> list[dict]:
    # 确保 aspect_ratio 格式正确
    if not aspect_ratio or not isinstance(aspect_ratio, str):
        aspect_ratio = "16:9"
    
    # 获取尺寸
    size = size_from_ratio(aspect_ratio, output_resolution)
    
    # 使用正确的模型 ID 和版本
    model_id = "google:firefly:colligo:nano-banana-pro"
    model_version = "nano-banana-2"
    
    # 完整的请求参数
    base_payload = {
        "modelId": model_id,
        "modelVersion": model_version,
        "n": 1,
        "prompt": prompt,
        "size": size,
        "seeds": [int(time.time()) % 999999],
        "groundSearch": False,
        "skipCai": False,
        "output": {"storeInputs": True},
        "generationMetadata": {
            "module": "text2image",
            "submodule": "ff-image-generate",
        },
        "modelSpecificPayload": {
            "aspectRatio": aspect_ratio,
            "parameters": {"addWatermark": False},
        },
    }

    if not source_image_ids:
        base_payload["referenceBlobs"] = []
        return [base_payload]

    candidates: list[dict] = []
    edited = dict(base_payload)
    edited["generationMetadata"] = {
        "module": "image2image",
        "submodule": "ff-image-generate",
    }

    c1 = dict(edited)
    c1["referenceBlobs"] = [
        {"id": img_id, "usage": "general"} for img_id in source_image_ids
    ]
    candidates.append(c1)

    c4 = dict(edited)
    c4["referenceBlobs"] = []
    c4["imagePrompt"] = {"referenceImage": source_image_ids[0]}
    candidates.append(c4)

    c5 = dict(edited)
    c5["referenceBlobs"] = []
    c5["imagePrompt"] = {"referenceImage": {"id": source_image_ids[0]}}
    candidates.append(c5)

    return candidates
