# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发低延迟场景。该功能集成在模型服务 API 中，无需用户自行训练压缩模型。所有压缩操作均在百炼后端完成，用户仅需在请求中指定压缩参数。

## 支持的模型/功能

当前支持对以下开源模型进行在线压缩（仅限 `qwen` 系列）：
- `qwen2-1.5b`, `qwen2-7b`, `qwen2-57b-a14b`（v2.0+ 版本）
- 仅支持 **INT4 量化**（AWQ 算法），不支持剪枝、知识蒸馏等其他压缩方式  
- 不支持自定义模型或 LoRA 微调后的模型压缩  

> **注意**：文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中提及“支持 LLaMA 系列模型”，但该描述已过时；实际仅 `qwen` 系列可用，详见 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的最新说明。

## 关键参数

调用 `/v1/models/{model}/compress` 接口时需传入以下必选参数：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `quantization_bit` | int | 必填，仅支持 `4`（INT4） |
| `quantization_method` | string | 必填，仅支持 `"awq"` |
| `calibration_dataset` | string | 可选，指定校准数据集名称（如 `"alpaca"`），默认使用平台内置校准集 |

参数组合无效将直接返回 `400 Bad Request`，不触发[异步任务](../concepts/asynchronous-task.md)。

## 使用方式

1. 确认目标模型支持压缩：调用 `GET /v1/models/{model}/capabilities`，检查 `compression.supported` 字段为 `true`  
2. 发起压缩请求（同步阻塞，通常耗时 3–8 分钟）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/models/qwen2-7b/compress" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"quantization_bit":4,"quantization_method":"awq"}'
   ```
3. 成功后返回新模型 ID（格式如 `qwen2-7b-int4-awq-20240520`），可立即用于 `/v1/chat/completions`

详细流程见 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 限制和注意事项

- 单次压缩任务最大等待时间 15 分钟，超时自动终止  
- 同一原始模型最多保留 3 个压缩版本（按创建时间自动清理最旧版本）  
- 压缩后模型 **不支持微调**，且 `max_tokens` 输出上限降为原始模型的 80%（例如原 `qwen2-7b` 支持 32768，压缩版仅 26214）  
- 若原始模型已下线（如 `qwen2-1.5b-v1.0`），其压缩版本也将不可用 —— 此行为在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中未明确说明，但实测验证一致。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


