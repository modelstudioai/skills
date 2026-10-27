# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，支持在保持推理精度基本不变的前提下，显著降低模型体积与显存占用，适用于边缘设备或高并发低延迟场景。该功能通过量化、剪枝等技术实现，由平台统一调度并封装为标准化 API。当前仅支持部分开源大模型的离线压缩流程，不支持在线实时压缩。

## 支持的模型/功能

- 当前支持的模型：`Qwen2-1.5B`、`Qwen2-7B`、`Phi-3-mini-4k-instruct`（需为 Hugging Face 格式，且已上传至百炼模型仓库）  
- 支持的压缩类型：INT4 量化（AWQ 算法）、INT8 量化（RTN）、结构化剪枝（仅限注意力头剪枝）  
- 不支持 LoRA 微调后模型的直接压缩；需先合并权重再提交压缩任务  
- 更多兼容模型列表详见 [模型压缩](../../raw/model-user-guide/model-compression.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台内注册的源模型 ID（如 `qwen2-1.5b-chat`） |
| `compression_type` | string | 是 | 可选值：`awq_int4`、`rtn_int8`、`head_pruning` |
| `calibration_dataset` | string | 否 | 校准数据集 ID（仅 `awq_int4` 和 `rtn_int8` 需指定，格式为 `dataset:xxx`）；默认使用平台内置校准集 |
| `pruning_ratio` | float | 否 | 仅 `head_pruning` 有效，取值范围 `[0.1, 0.5]`，表示保留注意力头的比例 |

> **注意**：`calibration_dataset` 参数在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中被标记为“可选”，但 [模型压缩介绍](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md) 明确要求 `awq_int4` 必须提供校准数据集，否则任务将失败。请以 API 文档为准。

## 使用方式

1. **准备模型**：确保源模型已通过 `POST /v1/models` 注册，并处于 `ready` 状态  
2. **发起压缩任务**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/model-compression \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen2-1.5b-chat",
           "compression_type": "awq_int4",
           "calibration_dataset": "dataset:calib-wikitext"
         }'
   ```
3. **轮询状态**：使用返回的 `task_id` 调用 `GET /v1/model-compression/{task_id}` 查询进度  
4. **部署压缩后模型**：任务成功后，新模型 ID 为 `{model_id}-awq-int4`（命名规则见 [模型压缩介绍](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)）

## 限制和注意事项

- 单次压缩任务最大超时时间为 120 分钟；超时后自动终止，不计费但不返还配额  
- 压缩后模型仅支持 `chat` 和 `completion` 推理接口，不支持 `embedding` 或 `rerank`  
- INT4 压缩模型在 A10 GPU 上最低需 8GB 显存，INT8 需 12GB；剪枝模型显存需求与原始模型相近  
- 压缩过程不可中断，任务提交后无法取消或修改参数  
- 若源模型含自定义 `forward` 实现或非标准 attention 结构，压缩可能失败，建议优先使用官方 Hugging Face 模型卡中验证过的配置

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


