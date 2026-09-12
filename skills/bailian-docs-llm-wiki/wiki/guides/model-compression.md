# model compression

模型压缩是百炼平台提供的轻量化[模型部署](../concepts/model-deployment.md)能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能集成在模型服务 SDK 与 API 中，支持主流开源大模型的离线压缩与在线推理加速。详细原理与适用场景可参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- **支持模型类型**：Llama 系列（Llama-2/3）、Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Phi-3、Gemma（1B/2B）等 Hugging Face 格式模型  
- **支持压缩方式**：AWQ（4-bit）、GPTQ（4-bit）、FP16 → INT4 量化、结构化剪枝（仅 Qwen 系列）  
- **不支持**：LoRA 微调权重的直接压缩（需先 merge）、非 Transformer 架构（如 CNN/RNN 类模型）  
- 更完整的兼容性列表见 [模型压缩](../../raw/model-user-guide/model-compression.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台已注册的原始模型 ID（如 `qwen2-7b-instruct`） |
| `compression_method` | string | 是 | 可选值：`awq`, `gptq`, `int4`；注意 `gptq` 仅支持 `qwen2-*` 和 `llama-3-*` 模型 |
| `compute_type` | string | 否 | 默认 `auto`；显式指定时可选 `cpu`（仅 `int4`）、`cuda`（`awq`/`gptq`） |
| `quantization_bits` | int | 否 | 仅 `int4` 方法下生效，默认 `4`；暂不支持 `int8` |

> **注意**：文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中提及的 `prune_ratio` 参数已在 v2.3.0 版本中移除，当前剪枝仅对 Qwen 系列自动启用，不可配置。

## 使用方式

1. **API 调用（推荐）**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/compression \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen2-1.5b-instruct",
           "compression_method": "awq",
           "compute_type": "cuda"
         }'
   ```
2. **SDK 调用（Python）**：  
   ```python
   from dashscope import ModelCompression
   result = ModelCompression.compress(
       model_id="llama3-8b-instruct",
       compression_method="gptq",
       wait_until_done=True
   )
   print(result.model_id)  # 返回压缩后的新 model_id
   ```
3. 压缩完成后，新模型 ID 可直接用于 `dashscope.Generation.call()`，无需修改推理代码。完整示例参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 单次压缩任务最大耗时 60 分钟，超时将失败并释放资源  
- 输入模型权重必须为 HF 格式（含 `config.json` + `pytorch_model.bin` 或 `model.safetensors`），不支持 GGUF  
- 压缩后模型**不支持**进一步微调（梯度计算被禁用），如需微调请在压缩前完成  
- AWQ/GPTQ 压缩仅支持 A10/A100/V100 GPU 实例；INT4 量化可在 CPU 实例运行，但吞吐下降约 40%  
- 压缩过程会占用约 2× 原始模型内存（例如 7B FP16 模型需约 28GB 显存）

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)



