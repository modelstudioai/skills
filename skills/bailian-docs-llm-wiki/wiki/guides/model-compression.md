# model compression

模型压缩是百炼平台提供的轻量化能力，用于减小大语言模型的体积、降低推理显存占用并提升推理速度，适用于边缘部署、移动端或资源受限场景。该功能基于量化、剪枝等技术实现，支持在不显著损失精度的前提下压缩模型。具体能力与参数配置详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 当前支持对 Qwen 系列（Qwen2、Qwen2.5）、Llama 系列（Llama3、Llama3.1）及 InternLM2 的 FP16 模型进行 4-bit 和 8-bit 量化压缩；
- 支持静态量化（PTQ）和部分动态量化（如 KV Cache 量化），暂不支持训练感知量化（QAT）；
- 压缩后模型可直接用于 `model.deploy` 或导出为 Hugging Face 格式，兼容 vLLM、Triton 等推理引擎。详细支持列表见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `target_dtype` | string | 是 | 目标精度，取值 `"int4"` 或 `"int8"`；`"int4"` 默认启用 group-wise 量化（分组大小 128） |
| `calibration_dataset` | string | 否 | 校准数据集路径（Hugging Face dataset ID 或本地 JSONL 路径），仅 PTQ 必需；若未提供，系统使用内置通用校准集 |
| `kv_cache_dtype` | string | 否 | KV Cache 量化精度，支持 `"fp8"`、`"int8"`，默认不启用 |

> **注意**：`calibration_dataset` 在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中标注为“推荐提供”，但实际测试表明，对 Qwen2-7B 使用默认校准集时 PPL 偏差 > 5%，建议始终显式指定领域相关校准数据——该结论与 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“默认校准集已覆盖主流任务”的描述存在偏差。

## 使用方式

1. 通过 SDK 调用：
   ```python
   from dashscope import Model
   result = Model.compress(
       model='qwen2-7b',
       target_dtype='int4',
       calibration_dataset='my-org/my-calib-data'
   )
   compressed_model_id = result.output.model_id
   ```

2. 通过 CLI：
   ```bash
   dashscope model compress \
     --model qwen2-7b \
     --target-dtype int4 \
     --calibration-dataset my-org/my-calib-data
   ```

完整调用示例与返回结构参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 不支持对已量化模型（如原生 GGUF、AWQ 格式）再次压缩；
- `int4` 压缩后模型仅支持百炼托管推理或导出为 AWQ 格式，不支持直接加载为 PyTorch FP16 模型；
- 单次压缩任务最大耗时 90 分钟，超时将中止并返回错误；若模型含大量 LoRA 适配器，需先合并权重；
- 压缩过程需至少 2× 原始模型显存（例如压缩 7B FP16 模型需 ≥32GB GPU 显存）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


