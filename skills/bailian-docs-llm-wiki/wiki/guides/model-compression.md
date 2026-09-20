# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，支持在保持推理精度的前提下减小模型体积、降低显存占用并提升推理速度。该功能适用于需要在资源受限环境（如边缘设备或高并发服务）中部署大语言模型的场景。压缩过程由平台统一调度，用户仅需配置参数并提交任务。

## 支持的模型/功能

- 当前支持对 Qwen 系列（Qwen2、Qwen2.5）、Qwen-VL、以及部分开源 Llama 架构变体（如 Llama-3-8B-Instruct）进行压缩；
- 支持的压缩方法包括量化（INT4/INT8）、剪枝（结构化剪枝）、知识蒸馏（需用户提供教师模型）；
- 不支持对自定义训练权重（非百炼托管 checkpoint）或非 Transformer 架构模型（如 RNN-based 模型）执行压缩。  
  > **注意**：[模型压缩](../../raw/model-user-guide/model-compression.md) 中提及支持 Llama-2，但该信息已过时；实际仅支持 Llama-3 及后续版本，请以 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台托管的原始模型 ID（如 `qwen2-7b-instruct`），必须为已发布且可调用的模型 |
| `compression_method` | string | 是 | 可选值：`quantization`、`pruning`、`distillation`；`distillation` 需额外提供 `teacher_model_id` |
| `target_dtype` | string | 否（仅 quantization 时生效） | `int4`（默认）、`int8`；`fp16` 仅用于蒸馏中间结果，不作为最终输出格式 |
| `sparsity_ratio` | float | 否（仅 pruning 时生效） | 剪枝稀疏度，范围 `[0.1, 0.5]`，建议从 `0.2` 起步 |

## 使用方式

1. 通过百炼控制台「模型管理 → 模型压缩」页面创建任务，或调用 API `/v1/models/compress` 提交 JSON 请求体；  
2. 示例请求体：
```json
{
  "model_id": "qwen2-7b-instruct",
  "compression_method": "quantization",
  "target_dtype": "int4"
}
```
3. 任务提交后，平台返回 `job_id`；可通过 `/v1/jobs/{job_id}` 查询状态，成功后生成新模型 ID（如 `qwen2-7b-instruct-int4`）。  
   详细流程参见 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 限制和注意事项

- 单次压缩任务最长运行时间为 4 小时，超时自动终止；  
- 压缩后模型不支持微调（fine-tuning），仅限推理使用；  
- INT4 量化模型在 A10/A100 显卡上可运行，但不兼容 T4（因缺乏 FP16 加速支持）；  
- 若原始模型含自定义 tokenizer 或特殊 preprocessor，压缩后可能失效，需人工验证输入兼容性；  
- 多模态模型（如 Qwen-VL）仅支持量化，不支持剪枝与蒸馏——该限制未在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中明确说明，但已在 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的“适用范围”章节补充。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


