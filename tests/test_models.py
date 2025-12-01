"""
模型管理模块单元测试
"""

import os
import pytest


@pytest.mark.unit
def test_resolve_dtype():
    """测试数据类型解析函数（不依赖模型）"""
    from engine.models import resolve_dtype
    import torch

    dtype = resolve_dtype()
    assert dtype in [torch.float32, torch.float16, torch.bfloat16]


@pytest.mark.unit
def test_get_model_path_fallback():
    """测试模型路径解析函数（fallback 到 HuggingFace ID，不依赖模型）"""
    from engine.models import get_model_path

    # 测试使用 HuggingFace ID 作为 fallback
    result = get_model_path(
        model_id="test/model",
        local_path="/nonexistent/path",
        container_path="/nonexistent/container",
        workspace_path="",
    )
    assert result == "test/model"


@pytest.mark.unit
def test_model_manager_singleton():
    """测试 ModelManager 单例模式（不依赖模型加载）"""
    from engine.models import ModelManager

    manager1 = ModelManager()
    manager2 = ModelManager()
    assert manager1 is manager2
    assert manager1 is not None


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("SKIP_MODEL_LOAD", "false").lower() == "true",
    reason="Skipping model loading tests in CI environment",
)
def test_model_manager_load_llm():
    """测试模型加载（需要真实模型，只在本地运行）"""
    from engine.models import ModelManager

    manager = ModelManager()
    tokenizer, model = manager.load_llm()
    assert tokenizer is not None
    assert model is not None

