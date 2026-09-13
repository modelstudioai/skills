# model compression

模型压缩是百炼平台提供的轻量化能力，用于减小大语言模型体积、降低推理资源消耗，同时尽可能保持原始模型性能。该功能支持对已部署或待部署的模型进行量化、剪枝等操作，适用于边缘部署、低成本推理等场景。具体能力与参数需结合平台当前版本的模型服务接口使用。

## 支持的模型/功能

- 当前仅支持 Qwen 系列开源模型（如 `qwen2-1.5b`、`qwen2-7b`）的 INT4 量化压缩；其他模型（如 Llama、Phi 等）暂不支持 [模型压缩](../../raw/model-user-guide/model-compression.md)。  
- 支持的压缩类型包括：AWQ（推荐）、GPTQ（实验性），不支持 PTQ 全精度校准流程。  
- 压缩后模型可直接用于百炼 `chat` 和 `completion` 接口，无需修改调用代码，但需在请求中显式指定压缩后的模型 ID（如 `qwen2-7b-int4-awq`）。

## 关键参数

- `compression_type`: 必填，取值为 `"awq"` 或 `"gptq"`；`"awq"` 为默认且唯一稳定支持的类型。  
- `weight_dtype`: 可选，仅当 `compression_type="awq"` 时生效，固定为 `"int4"`（不支持 int8 或 fp16）。  
- `calibration_dataset`: 可选，若未提供，平台将自动使用内部通用校准集；自定义数据集需符合 [模型压缩](../../raw/model-user-guide/model-compression.md) 中规定的格式（JSONL，每行含 `"text"` 字段）。  
- `quantize_config`: 高级参数，仅限企业版用户配置，普通开发者应忽略；其字段含义详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 使用方式

1. 通过百炼控制台「模型管理 → 模型压缩」页面上传原始模型或选择已注册模型；  
2. 配置压缩参数（类型、校准数据集等），点击「开始压缩」；  
3. 压缩任务完成后，平台生成新模型 ID，并自动注册至模型仓库；  
4. 在 API 调用中，将 `model` 参数设为该新 ID（例如 `qwen2-7b-int4-awq`），其余参数（`messages`, `temperature` 等）保持不变。

## 限制和注意事项

- 单次压缩任务最长运行 120 分钟，超时将失败并释放资源；  
- 原始模型必须为 Hugging Face 格式（含 `config.json`、`pytorch_model.bin` 或 `model.safetensors`），不支持 GGUF 或 ONNX 格式；  
- > **注意**：文档中提及的 “支持 Llama-3-8B 的 GPTQ 压缩” 已过时——当前平台实际仅对 Qwen 系列启用 GPTQ，且处于实验阶段，稳定性与精度未达生产要求，强烈建议优先选用 AWQ；该矛盾信息源于旧版 [模型压缩](../../raw/model-user-guide/model-compression.md) 未及时同步。  
- 压缩后模型不支持微调（fine-tuning），如需微调，请先压缩再训练的流程不被支持；  
- INT4 压缩模型在长上下文（>8K tokens）场景下可能出现轻微输出退化，建议在业务侧增加结果校验逻辑。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


