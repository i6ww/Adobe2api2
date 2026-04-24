from __future__ import annotations

# 默认支持的所有比例
SUPPORTED_RATIOS = {"1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "3:2", "5:4", "4:5", "2:3", "8:1", "1:4", "1:8"}

# GPT Image 2 支持的比例
GPT_IMAGE2_RATIOS = {
    "4:3": "4x3",
    "5:4": "5x4",
    "4:5": "4x5",
    "3:2": "3x2",
    "2:3": "2x3",
    "1:1": "1x1",
}

# firefly-nano-banana-pro 支持的比例
NANO_BANANA_PRO_RATIOS = {
    "1:1": "1x1",
    "16:9": "16x9",
    "9:16": "9x16",
    "4:3": "4x3",
    "3:4": "3x4",
    "21:9": "21x9",
    "5:4": "5x4",
    "4:5": "4x5",
}

# firefly-nano-banana2 支持的比例
NANO_BANANA2_RATIOS = {
    "1:1": "1x1",
    "16:9": "16x9",
    "9:16": "9x16",
    "4:3": "4x3",
    "3:4": "3x4",
    "21:9": "21x9",
    "3:2": "3x2",
    "5:4": "5x4",
    "4:5": "4x5",
    "2:3": "2x3",
    "8:1": "8x1",
    "1:4": "1x4",
    "1:8": "1x8",
}

# 基础比例映射（默认）
RATIO_SUFFIX_MAP = NANO_BANANA_PRO_RATIOS

MODEL_CATALOG: dict[str, dict] = {}


def _register_nano_banana_family(
    prefix: str,
    *,
    upstream_model_id: str,
    upstream_model_version: str,
    family_label: str,
    supported_ratios: dict = None,
) -> None:
    # 使用指定的比例映射，如果没有指定则使用默认的
    ratios_map = supported_ratios or RATIO_SUFFIX_MAP
    for res in ("1k", "2k", "4k"):
        for ratio, suffix in ratios_map.items():
            model_id = f"{prefix}-{res}-{suffix}"
            MODEL_CATALOG[model_id] = {
                "upstream_model": "google:firefly:colligo:nano-banana-pro",
                "upstream_model_id": upstream_model_id,
                "upstream_model_version": upstream_model_version,
                "output_resolution": res.upper(),
                "aspect_ratio": ratio,
                "description": f"{family_label} ({res.upper()} {ratio})",
            }


_register_nano_banana_family(
    "firefly-nano-banana-pro",
    upstream_model_id="gemini-flash",
    upstream_model_version="nano-banana-2",
    family_label="Firefly Nano Banana Pro",
    supported_ratios=NANO_BANANA_PRO_RATIOS,
)
_register_nano_banana_family(
    "firefly-nano-banana",
    upstream_model_id="gemini-flash",
    upstream_model_version="nano-banana-2",
    family_label="Firefly Nano Banana",
    supported_ratios=NANO_BANANA_PRO_RATIOS,
)
_register_nano_banana_family(
    "firefly-nano-banana2",
    upstream_model_id="gemini-flash",
    upstream_model_version="nano-banana-3",
    family_label="Firefly Nano Banana 2",
    supported_ratios=NANO_BANANA2_RATIOS,
)

DEFAULT_MODEL_ID = "firefly-nano-banana-pro-2k-16x9"

VIDEO_MODEL_CATALOG: dict[str, dict] = {
    "firefly-sora2-4s-9x16": {
        "duration": 4,
        "aspect_ratio": "9:16",
        "description": "Firefly Sora2 video model (4s 9:16)",
    },
    "firefly-sora2-4s-16x9": {
        "duration": 4,
        "aspect_ratio": "16:9",
        "description": "Firefly Sora2 video model (4s 16:9)",
    },
    "firefly-sora2-8s-9x16": {
        "duration": 8,
        "aspect_ratio": "9:16",
        "description": "Firefly Sora2 video model (8s 9:16)",
    },
    "firefly-sora2-8s-16x9": {
        "duration": 8,
        "aspect_ratio": "16:9",
        "description": "Firefly Sora2 video model (8s 16:9)",
    },
    "firefly-sora2-12s-9x16": {
        "duration": 12,
        "aspect_ratio": "9:16",
        "description": "Firefly Sora2 video model (12s 9:16)",
    },
    "firefly-sora2-12s-16x9": {
        "duration": 12,
        "aspect_ratio": "16:9",
        "description": "Firefly Sora2 video model (12s 16:9)",
    },
}

for dur in (4, 8, 12):
    for ratio in ("9:16", "16:9"):
        model_id = f"firefly-sora2-pro-{dur}s-{RATIO_SUFFIX_MAP[ratio]}"
        VIDEO_MODEL_CATALOG[model_id] = {
            "duration": dur,
            "aspect_ratio": ratio,
            "upstream_model": "openai:firefly:colligo:sora2-pro",
            "description": f"Firefly Sora2 Pro video model ({dur}s {ratio})",
        }

for dur in (4, 6, 8):
    for ratio in ("16:9", "9:16"):
        for res in ("1080p", "720p"):
            model_id = f"firefly-veo31-{dur}s-{RATIO_SUFFIX_MAP[ratio]}-{res}"
            VIDEO_MODEL_CATALOG[model_id] = {
                "engine": "veo31-standard",
                "upstream_model": "google:firefly:colligo:veo31",
                "duration": dur,
                "aspect_ratio": ratio,
                "resolution": res,
                "description": f"Firefly Veo31 video model ({dur}s {ratio} {res})",
            }

for dur in (4, 6, 8):
    for ratio in ("16:9", "9:16"):
        for res in ("1080p", "720p"):
            model_id = f"firefly-veo31-ref-{dur}s-{RATIO_SUFFIX_MAP[ratio]}-{res}"
            VIDEO_MODEL_CATALOG[model_id] = {
                "engine": "veo31-standard",
                "upstream_model": "google:firefly:colligo:veo31",
                "duration": dur,
                "aspect_ratio": ratio,
                "resolution": res,
                "reference_mode": "image",
                "description": f"Firefly Veo31 Ref video model ({dur}s {ratio} {res})",
            }

for dur in (4, 6, 8):
    for ratio in ("16:9", "9:16"):
        for res in ("1080p", "720p"):
            model_id = f"firefly-veo31-fast-{dur}s-{RATIO_SUFFIX_MAP[ratio]}-{res}"
            VIDEO_MODEL_CATALOG[model_id] = {
                "engine": "veo31-fast",
                "upstream_model": "google:firefly:colligo:veo31-fast",
                "duration": dur,
                "aspect_ratio": ratio,
                "resolution": res,
                "description": f"Firefly Veo31 Fast video model ({dur}s {ratio} {res})",
            }

# GPT Image 2 models
for ratio, suffix in GPT_IMAGE2_RATIOS.items():
    model_id = f"firefly-gpt-image-2-{suffix}"
    MODEL_CATALOG[model_id] = {
        "upstream_model": "openai:firefly:colligo:gpt-image-2",
        "upstream_model_id": "gpt-4o",
        "upstream_model_version": "gpt-image-2",
        "output_resolution": "4K",
        "aspect_ratio": ratio,
        "description": f"Firefly GPT Image 2 ({ratio})",
    }

# GPT Image 2 4K model
MODEL_CATALOG["firefly-gpt-image-2-4k"] = {
    "upstream_model": "openai:firefly:colligo:gpt-image-2",
    "upstream_model_id": "gpt-4o",
    "upstream_model_version": "gpt-image-2",
    "output_resolution": "4K",
    "aspect_ratio": "1:1",
    "description": "Firefly GPT Image 2 (4K)",
}