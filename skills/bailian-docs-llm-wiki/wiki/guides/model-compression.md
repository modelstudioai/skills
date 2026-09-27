# model compression

模型压缩是百炼平台提供的轻量化能力，用于减小大语言模型的体积、降低推理显存占用并提升推理速度，适用于边缘部署、移动端或资源受限场景。该功能基于结构化剪枝、量化和知识蒸馏等技术实现，支持在不显著损失精度的前提下生成压缩后的模型版本。具体能力与参数配置详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 当前仅支持 `qwen-plus`、`qwen-max` 和 `qwen-turbo` 三类 Qwen 系列模型的压缩（v2024.06 起生效）；
- 支持 INT4 量化（对称/非对称）、通道级结构化剪枝（稀疏度 20%–50%）、以及教师-学生蒸馏（需指定教师模型 ID）；
- 不支持 LoRA 微调后模型的直接压缩；须先合并权重再提交压缩任务。详细兼容性说明见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression_method` | string | 是 | 可选 `"int4"`, `"pruning"`, `"distillation"`；若为 `"distillation"`，必须同时提供 `teacher_model_id` |
| `sparsity_ratio` | float | 否（仅 pruning 时有效） | 剪枝稀疏度，取值范围 `[0.2, 0.5]`，默认 `0.3` |
| `quantization_config` | object | 否（仅 int4 时有效） | 包含 `symmetric: bool` 和 `group_size: int`（默认 128） |
| `teacher_model_id` | string | 否（仅 distillation 时必填） | 百炼平台内已发布的模型 ID，如 `"qwen-max-20240515"` |

> **注意**：原始文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中曾列出 `"fp16"` 作为 `compression_method` 选项，但该值已于 v2024.07 版本移除，实际调用将返回 `400 Bad Request`；请以当前 API 文档为准。

## 使用方式

1. 通过百炼控制台「模型管理 → 模型压缩」页面上传待压缩模型（需为 `.safetensors` 格式，且已通过 `bailian-cli validate-model` 校验）；
2. 或调用 REST API：`POST /v1/models/{model_id}/compress`，请求体按上述参数格式构造 JSON；
3. 提交后返回 `task_id`，可通过 `GET /v1/compression-tasks/{task_id}` 轮询状态；成功后生成新模型 ID，可直接用于 `chat.completions` 接口。完整流程参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 单次压缩任务最大支持 24GB 原始模型（未量化前），超限将拒绝提交；
- 压缩后模型不支持进一步微调（fine-tuning），仅可用于推理；
- INT4 量化模型在 A10/A100 GPU 上可运行，但不兼容 T4（因缺乏 INT4 Tensor Core 支持）；
- 若原始模型含自定义 OP（如 `flash_attn` 的特定变体），压缩可能失败，建议使用标准 Hugging Face 格式导出。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


