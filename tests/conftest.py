"""
pytest 配置和共享 fixtures
"""

import os
import pytest
from unittest.mock import Mock, patch


@pytest.fixture(autouse=True)
def mock_model_loading():
    """在 CI 环境中自动 mock 模型加载"""
    if os.getenv("SKIP_MODEL_LOAD", "false").lower() == "true":
        with (
            patch("engine.models.AutoModelForCausalLM.from_pretrained") as mock_model,
            patch("engine.models.AutoTokenizer.from_pretrained") as mock_tokenizer,
        ):
            # 创建 mock tokenizer
            mock_tok = Mock()
            mock_tok.pad_token = None
            mock_tok.eos_token = "<|eot_id|>"
            mock_tok.pad_token_id = 0
            mock_tok.eos_token_id = 128001
            mock_tok.encode.return_value = [1, 2, 3]  # 用于 stop_sequences
            mock_tok.return_value = {"input_ids": Mock(shape=[1, 10])}  # 用于 tokenizer 调用
            mock_tokenizer.return_value = mock_tok

            # 创建 mock model
            mock_mod = Mock()
            mock_mod.eval.return_value = None
            # 创建模拟的 device
            mock_device = Mock()
            mock_device.type = "cuda" if os.getenv("CUDA_AVAILABLE", "false") == "true" else "cpu"
            mock_param = Mock()
            mock_param.device = mock_device
            mock_mod.parameters.return_value = [mock_param]
            # Mock generate 方法
            mock_output_ids = Mock()
            mock_output_ids.shape = [1, 20]
            mock_output_ids.__getitem__.return_value = [1, 2, 3, 4, 5]
            mock_mod.generate.return_value = mock_output_ids
            mock_model.return_value = mock_mod

            yield
    else:
        yield


@pytest.fixture
def mock_model_manager():
    """提供 mock 的 ModelManager，避免加载真实模型"""
    from engine.models import ModelManager

    # 创建 mock 返回值
    mock_tokenizer = Mock()
    mock_tokenizer.pad_token = None
    mock_tokenizer.eos_token = "<|eot_id|>"
    mock_tokenizer.pad_token_id = 0
    mock_tokenizer.eos_token_id = 128001
    mock_tokenizer.encode.return_value = [1, 2, 3]
    mock_tokenizer.return_value = {"input_ids": Mock(shape=[1, 10])}
    mock_tokenizer.decode.return_value = "Mocked output text"

    mock_model = Mock()
    mock_model.eval.return_value = None
    mock_param = Mock()
    mock_param.device = Mock()
    mock_model.parameters.return_value = [mock_param]
    mock_output_ids = Mock()
    mock_output_ids.shape = [1, 20]
    mock_output_ids.__getitem__.return_value = [1, 2, 3, 4, 5]
    mock_model.generate.return_value = mock_output_ids

    with (
        patch.object(ModelManager, "load_llm", return_value=(mock_tokenizer, mock_model)),
        patch.object(ModelManager, "load_guard", return_value=(mock_tokenizer, mock_model)),
        patch.object(ModelManager, "generate", return_value=("Mocked output", 10, 20, 100.0)),
        patch.object(
            ModelManager,
            "moderate",
            return_value={
                "verdict": "allow",
                "severity": "low",
                "rationale": ["No issues found"],
                "categories": [],
            },
        ),
    ):
        manager = ModelManager()
        yield manager
