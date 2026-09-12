# model compression

模型压缩是百炼平台提供的轻量化[模型部署](../concepts/model-deployment.md)能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能集成在模型服务 SDK 与控制台中，支持主流开源大模型的离线压缩与在线推理加速。详细原理与适用场景参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 支持 Llama 系列（Llama-2/3、CodeLlama）、Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Phi 系列（Phi-3）等 Hugging Face 格式模型  
- 提供 INT4/INT5/FP16 三种量化精度选项；支持 AWQ、GPTQ、Bitsandbytes 后训练量化（PTQ）  
- 支持导出为 ONNX、GGUF、Safetensors 格式，兼容 vLLM、llama.cpp 等推理引擎  
- 压缩后模型可直接部署为百炼标准 API 服务，无需修改客户端调用逻辑，详见 [模型压缩](../../raw/model-user-guide/model-compression.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 原始模型 ID（如 `qwen2-7b-instruct`），需在百炼模型仓库中可见 |
| `quantization_method` | string | 是 | 可选 `awq`、`gptq`、`bitsandbytes`；`awq` 推荐用于 Llama/Qwen 系列 |
| `compute_dtype` | string | 否 | 默认 `int4`；可设为 `int5` 或 `fp16`（仅 `bitsandbytes` 支持 fp16） |
| `calibration_dataset` | string | 否 | 仅 PTQ 方法需指定校准数据集 ID（如 `alpaca-zh-1000`），详见 [模型压缩](../../raw/model-user-guide/model-compression.md) |

## 使用方式

1. **控制台操作**：进入「模型管理」→「模型压缩」页，选择源模型、配置量化方法与精度，提交任务  
2. **API 调用**（Python SDK）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client.compress_model(
       request=bailian_models.CompressModelRequest(
           model_id="qwen2-7b-instruct",
           quantization_method="awq",
           compute_dtype="int4"
       )
   )
   ```
3. 压缩任务完成后，生成新模型 ID（如 `qwen2-7b-instruct-awq-int4`），可像普通模型一样部署与调用

## 限制和注意事项

- 单次压缩任务最大支持 30B 参数量模型；超大模型（>30B）需联系技术支持开通白名单  
- `awq` 和 `gptq` 方法不支持动态 batch size，部署时需固定 `max_batch_size=1`（vLLM backend 下）  
- > **注意**：原始文档中提及“支持 LoRA 微调后模型压缩”，但当前版本（v2.4.1）尚未实现该能力，实际调用将返回 `NotImplementedError`；此信息已过时，请以 SDK 错误提示为准  
- 量化后模型不支持梯度计算与继续训练，仅限推理使用  
- 校准数据集必须与目标领域一致（如中文模型应使用中文校准集），否则精度下降显著

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


