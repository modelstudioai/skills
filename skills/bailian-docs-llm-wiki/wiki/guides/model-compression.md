# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，支持在保持推理精度基本不变的前提下显著降低模型体积与显存占用，适用于边缘设备、低配服务器等资源受限场景。该功能基于量化、剪枝等技术实现，由平台统一调度执行，用户仅需配置参数即可触发压缩流程。详细原理与适用场景请参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 支持的模型/功能

- 当前支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan2、Llama2/3（7B/8B/15B 规格）及部分开源 MoE 模型（如 Qwen2-MoE）；
- 支持 INT4、INT5、INT8 三种量化粒度，以及混合精度（如 KV Cache FP16 + 权重 INT4）；
- 提供自动压缩模式（auto），由平台根据模型结构与硬件配置推荐最优压缩策略；该模式已在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中明确说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression_type` | string | 是 | 取值：`int4` / `int5` / `int8` / `auto`；`auto` 模式下平台将忽略 `target_bits` |
| `target_bits` | int | 否 | 显式指定量化位宽（仅当 `compression_type` 非 `auto` 时生效）；默认为 `4` |
| `calibration_dataset` | string | 否 | 校准数据集路径（OSS URI），用于后训练量化（PTQ）；若未提供，平台使用内置通用校准集；详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) |

## 使用方式

1. 在模型部署请求的 `model_config` 字段中嵌入 `compression` 对象：
```json
{
  "model_id": "qwen2-7b",
  "model_config": {
    "compression": {
      "compression_type": "int4",
      "target_bits": 4
    }
  }
}
```
2. 提交部署任务后，平台将在模型加载阶段自动执行压缩，并返回压缩后模型 ID（格式为 `qwen2-7b-compressed-int4-xxx`）；
3. 压缩模型可直接用于 `chat` 或 `embeddings` 接口，无需修改调用逻辑。

## 限制和注意事项

- 不支持对已启用 LoRA 微调的模型进行在线压缩（需先合并权重再提交压缩）；
- `int4` 压缩不兼容 `flash_attention_2: false` 配置，启用时必须设置 `flash_attention_2: true`；
- > **注意**：原始文档中提及“支持 Phi-3 系列模型压缩”，但截至 v2.3.0 版本，Phi-3 实际尚未开放压缩能力，该描述已过时，请以控制台模型支持列表为准；
- 单次压缩任务最大校准样本数为 512；超出时将自动截断，可能影响量化精度；
- 压缩过程不可中断，平均耗时约 8–15 分钟（取决于模型大小与 `calibration_dataset` 规模）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


