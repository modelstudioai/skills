# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，支持在保持推理精度基本不变的前提下，显著降低模型体积与显存占用，适用于边缘设备或高并发场景。该功能基于量化、剪枝等技术实现，由平台统一调度执行，用户仅需配置参数即可触发。详细原理与适用场景参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 当前支持 Llama、Qwen、Phi 系列的 7B/14B 参数量级的 Decoder-only 模型（如 `qwen2-7b`, `llama3-8b`），暂不支持多模态或编码器-解码器结构（如 T5、Whisper）。
- 支持 INT4 量化（AWQ/GPTQ）、Group-wise 量化、以及结构化剪枝（仅限注意力头剪枝）；不支持知识蒸馏或低秩适配（LoRA）压缩路径。
- 压缩后模型可直接用于 `model.deploy()` 或通过 `model.invoke()` 调用，兼容标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。更多模型兼容性说明请参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression_type` | string | 是 | 可选 `"int4_awq"`、`"int4_gptq"`、`"prune_head"`；默认 `"int4_awq"` |
| `group_size` | int | 否 | 仅对 AWQ/GPTQ 有效，取值 32/64/128；默认 128 |
| `prune_ratio` | float | 否 | 仅对 `prune_head` 有效，范围 `[0.1, 0.5]`；默认 0.2 |
| `calibration_dataset` | string | 否 | 校准数据集 ID（如 `"alpaca-clean"`），若未指定则使用平台内置小样本集 |

> **注意**：原始文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中提及支持 `"fp16_to_int8"` 类型，但该选项已在 v3.2.0 版本中移除，实际调用将返回 `UnsupportedCompressionType` 错误，请以 SDK 最新枚举为准。

## 使用方式

1. 创建压缩任务：
```python
from dashscope import Model

task = Model.compress(
    model='qwen2-7b',
    compression_type='int4_awq',
    group_size=64,
    calibration_dataset='alpaca-clean'
)
```
2. 轮询任务状态直至 `status == 'succeeded'`；
3. 获取压缩后模型 ID（`task.output.model_id`），用于后续部署或推理；
4. 验证效果建议参考 [模型压缩](../../raw/model-user-guide/model-compression.md) 中的精度评估方法。

## 限制和注意事项

- 单次压缩任务最大耗时 90 分钟，超时自动终止；大模型（>14B）建议优先选用 `int4_awq` 而非 `prune_head`。
- 压缩后模型不支持微调（`model.finetune()` 报错），且无法回退为原始权重。
- 校准数据集需与目标领域分布一致，否则可能引入显著精度下降；平台内置校准集仅适用于通用对话场景。
- 所有压缩操作均需模型处于 `published` 状态，草稿模型（`draft`）不可压缩。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


