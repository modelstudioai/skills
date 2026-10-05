# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于资源受限的边缘设备或高并发服务场景。该功能集成在模型部署工作流中，支持对已发布的模型版本进行离线压缩并生成新版本。所有压缩操作均需通过 API 或控制台触发，不支持运行时动态压缩。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）和 Qwen-VL 的 FP16 模型版本进行 INT4 量化压缩；[模型压缩](../../raw/model-user-guide/model-compression.md) 明确列出不支持 Llama、Phi 等第三方开源架构。
- 支持的压缩类型包括：W4A16（权重 INT4 + 激活 FP16）、AWQ（通道级权重量化）；[模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中提到的“混合精度剪枝”功能暂未上线，属于规划中特性。
- > **注意**：[模型压缩](../../raw/model-user-guide/model-compression.md) 文档中提及的 “支持 ONNX 格式导出” 与实际平台能力不符——当前压缩后模型仅输出适配百炼推理引擎的专有格式（`.bml`），ONNX 导出尚未开放。

## 关键参数

- `compression_type`: 必填，取值为 `"w4a16"` 或 `"awq"`；
- `calibration_dataset`: 可选，指定校准数据集 ID（需为已上传的 JSONL 格式样本集，含 `text` 字段）；
- `calibration_steps`: 默认 128，建议 64–512，影响量化精度；[模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 强调该参数对 AWQ 效果尤为关键；
- `device_map`: 可选，指定校准所用 GPU 设备（如 `"cuda:0"`），多卡环境下需显式声明。

## 使用方式

1. 确保目标模型版本状态为 `published`，且满足架构与精度要求；
2. 调用 `POST /v1/models/{model_id}/versions/{version_id}/compress` 接口，传入上述参数；
3. 压缩任务异步执行，可通过 `GET /v1/jobs/{job_id}` 查询状态；成功后返回新模型版本 ID，该版本可直接用于部署；
4. 控制台路径：模型详情页 →「版本管理」→ 选择版本 →「压缩」按钮（仅对支持型号可见）。

## 限制和注意事项

- 单次压缩任务最大耗时 120 分钟，超时自动终止；大模型（>10B 参数）建议预留至少 2× GPU 显存（相对于原始 FP16 占用）；
- 压缩后模型不支持微调或继续训练，仅限推理使用；
- 校准数据集质量直接影响量化稳定性：若 `calibration_dataset` 缺失或样本过少（<32 条），系统将回退至内部默认校准集，但 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 提示此模式可能导致部分长文本生成质量下降。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


