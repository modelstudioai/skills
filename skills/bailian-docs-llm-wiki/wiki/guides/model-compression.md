# model compression

模型压缩是百炼平台提供的轻量化[模型部署](../concepts/model-deployment.md)能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能集成在模型服务 SDK 与控制台中，支持主流开源大模型的离线压缩与在线推理加速。详细原理与适用场景参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 支持 Llama、Qwen、Phi 等基于 Transformer 架构的开源大模型（vLLM/llama.cpp 后端）
- 提供 INT4/INT8 量化、KV Cache 剪枝、LoRA 微调后压缩三种模式
- 输出兼容 ONNX Runtime、Triton 和百炼自研推理引擎的压缩模型包  
- 不支持对已部署的在线服务实时压缩；需先导出原始模型权重，再调用压缩 API —— 具体流程详见 [模型压缩](../../raw/model-user-guide/model-compression.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `quantization_type` | string | 是 | 取值：`int4`, `int8`, `fp16`；`int4` 为默认且推荐选项 |
| `calibration_dataset` | string | 否 | 校准数据集路径（OSS URI），若未提供则使用内置通用校准集 |
| `target_device` | string | 否 | `cpu`, `cuda`, `aipu`；影响算子融合策略，缺省为 `cuda` |

> **注意**：`target_device=aipu` 仅在 v2.3.0+ 版本 SDK 中可用；旧版文档中提及的 `npu` 设备类型已废弃，请以 [模型压缩](../../raw/model-user-guide/model-compression.md) 中最新参数列表为准。

## 使用方式

1. 安装支持压缩的 SDK：
   ```bash
   pip install alibabacloud-bailian20231219==2.3.0
   ```
2. 调用 `compress_model()` 方法：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client(...)
   resp = client.compress_model(
       model_id="qwen2-7b",
       quantization_type="int4",
       calibration_dataset="oss://my-bucket/calib-1024.jsonl"
   )
   print(resp.compressed_model_id)  # 返回可直接部署的压缩模型 ID
   ```
3. 部署压缩模型（同标准[模型部署](../concepts/model-deployment.md)流程）：参考 [模型压缩](../../raw/model-user-guide/model-compression.md)

## 限制和注意事项

- 单次压缩任务最大超时时间为 180 分钟，超时将终止并释放资源
- 输入模型必须为 Hugging Face 格式（含 `config.json` + `pytorch_model.bin` 或 `model.safetensors`）
- 不支持对多模态模型（如 Qwen-VL）进行 KV Cache 剪枝；该限制已在新版文档中明确，旧版指南存在遗漏，请以 [模型压缩](../../raw/model-user-guide/model-compression.md) 为准
- 压缩后模型不支持梯度更新，仅用于推理；如需微调，请先压缩再加载至训练框架（需手动适配）

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


