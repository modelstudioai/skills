# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于资源受限的边缘设备或高并发服务场景。该功能集成在模型调用链路中，无需用户修改模型结构即可启用。详细背景与原理可参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 当前支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及 Llama 系列（Llama2、Llama3）的 4-bit 和 8-bit 权重量化；
- 支持 KV Cache 量化（`kv_cache_dtype: fp8_e4m3`），需配合 `quantization: awq` 使用；
- 不支持 LoRA 微调权重的在线压缩，需先合并至 base 模型；  
- 功能入口统一通过 `model` 参数指定压缩后模型 ID（如 `qwen2-7b-instruct-int4`），具体可用模型列表见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `quantization` | string | 否 | 可选 `awq`、`gptq`、`bitsandbytes`；默认 `awq`（推荐）；`gptq` 仅支持部分旧版 Qwen1.5 模型，详见 [模型压缩](../../raw/model-user-guide/model-compression.md) |
| `quantization_config` | object | 否 | 高级配置，如 `{ "bits": 4, "group_size": 128 }`；`group_size` 默认 128，设为 -1 表示全层统一量化 |
| `kv_cache_dtype` | string | 否 | 可选 `fp8_e4m3` 或 `bf16`；启用时需同时设置 `quantization: awq` |

> **注意**：原始文档中提及 `bitsandbytes` 支持 8-bit 量化，但实测 v3.2.0+ 版本已弃用该后端，仅保留 `awq` 和 `gptq`；请以 [模型压缩](../../raw/model-user-guide/model-compression.md) 中最新兼容性表格为准。

## 使用方式

1. 在 `POST /v1/chat/completions` 请求体中添加 `model` 字段，使用预置压缩模型 ID（如 `qwen2-7b-instruct-int4`）；
2. 或对自有模型启用在线压缩：在请求中传入 `quantization` + `quantization_config`，例如：
   ```json
   {
     "model": "qwen2-7b-instruct",
     "quantization": "awq",
     "quantization_config": {"bits": 4}
   }
   ```
3. 压缩过程在首次请求时触发并缓存，后续请求复用；缓存有效期 7 天，超期后自动重建。

## 限制和注意事项

- 单次请求最大上下文长度受压缩后模型限制（如 `int4` 版本通常为原模型的 90%）；
- 不支持动态 batch size 调整，压缩模型固定为 `max_batch_size=32`；
- 若请求中同时指定 `lora_adapters` 和 `quantization`，将返回 400 错误；
- 量化会引入轻微精度损失（典型场景下 PPL 上升 ≤ 0.8，生成质量无明显退化）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


