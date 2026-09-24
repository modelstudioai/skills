# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能目前仅支持部分开源大模型的离线压缩，不支持实时在线压缩或微调后模型的增量压缩。所有压缩操作均需通过 API 或控制台提交异步任务完成。

## 支持的模型与功能

- **支持模型**：仅限 `Qwen2-1.5B`、`Qwen2-7B`、`Qwen1.5-4B`（INT4 量化）及 `Phi-3-mini-4K`（AWQ 量化），其他模型暂未开放压缩入口。  
- **支持功能**：静态量化（INT4/INT8）、AWQ 权重压缩、KV Cache 优化；不支持结构化剪枝、知识蒸馏或 LoRA 压缩。  
- 详细支持列表见 [模型压缩](../../raw/model-user-guide/model-compression.md)。  
- 各模型压缩能力差异说明参见 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台注册的原始模型 ID（如 `qwen2-7b-chat`），必须为已支持列表中的模型 |
| `compression_type` | string | 是 | 取值：`int4`、`int8`、`awq`；`awq` 仅对 `phi3-mini-4k` 有效 |
| `device` | string | 否 | 目标设备类型，可选 `cpu`、`cuda`（默认 `cuda`）；`cpu` 下仅支持 `int8` |
| `calibration_dataset` | string | 否 | 校准数据集路径（OSS URI），若未提供则使用平台内置校准集 |

> **注意**：`calibration_dataset` 参数在 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中被标记为“推荐提供”，但实际任务中若缺失会导致 INT4/AWQ 压缩失败——该行为与 [模型压缩](../../raw/model-user-guide/model-compression.md) 中“自动 fallback 到内置集”的描述矛盾，请务必显式传入校准集。

## 使用方式

1. 通过百炼 SDK 提交压缩任务：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = Bailian20231219Client(...)
   req = bailian_models.CreateCompressionJobRequest(
       model_id="qwen2-7b-chat",
       compression_type="int4",
       calibration_dataset="oss://my-bucket/calib-1024.jsonl"
   )
   resp = client.create_compression_job(req)
   ```
2. 任务状态轮询 `GetCompressionJobStatus`，成功后返回压缩后模型 ID（格式：`<original_id>-int4-<timestamp>`）。  
3. 压缩模型可直接用于 `ChatCompletion` 接口，无需额外配置。完整流程详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 单次压缩任务最大耗时 120 分钟，超时自动终止；失败任务不退还配额。  
- 压缩后模型不可逆，且不支持二次压缩（如对 `qwen2-7b-chat-int4` 再执行 AWQ）。  
- INT4 压缩要求 GPU 显存 ≥ 24GB（A10/A100），CPU 模式下仅支持 `int8` 且推理速度下降约 40%。  
- 所有压缩结果默认保留 30 天，过期自动清理；如需长期保存，请及时导出至自有 OSS。  
- 当前不支持多卡并行压缩，也不支持混合精度（如部分层 FP16 + 部分层 INT4）。更多约束请参考 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


