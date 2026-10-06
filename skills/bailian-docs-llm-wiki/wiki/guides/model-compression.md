# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发低延迟场景。该功能集成在 `model.deploy` 接口的 `compression` 字段中，支持对已发布的模型版本进行无损/有损压缩配置。所有压缩操作均在服务端完成，用户无需本地执行转换。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）和 Qwen-VL 的 **FP16 模型版本** 进行压缩；INT4 量化仅限文本模型（不支持多模态）。
- 支持两种压缩模式：`int4`（权重 4-bit 量化）和 `int8`（权重 8-bit 量化），暂不支持混合精度或结构化剪枝。
- 压缩后模型保持原始 API 接口兼容性，可直接用于 `model.invoke` 调用。详细能力范围请参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

调用 `model.deploy` 时需在 `compression` 对象中指定：
- `method`: 必填，取值为 `"int4"` 或 `"int8"`
- `compute_type`: 可选，取值为 `"cpu"`（默认）或 `"cuda"`；若指定 `"cuda"`，则要求目标实例具备 GPU 且驱动版本 ≥ 535.54.03
- `calibration_dataset`: 仅 `int4` 时可选，传入数据集 ID（如 `"qwen-calib-202406"`）以启用校准量化；未提供时使用平台内置通用校准集  
更多参数说明见 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 使用方式

1. 确保目标模型已发布（`model.publish` 成功），且版本状态为 `active`
2. 调用 `model.deploy`，传入 `compression` 配置（示例）：
   ```json
   {
     "model_id": "qwen2-7b",
     "version": "v1",
     "compression": {
       "method": "int4",
       "compute_type": "cpu"
     }
   }
   ```
3. 部署成功后，返回的 `endpoint` 可直接用于推理；压缩模型的 token 吞吐量提升约 2.1×（CPU）或 1.7×（CUDA），详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 单次部署最多申请 1 个压缩实例；同一模型版本不可同时部署多个不同 `method` 的压缩变体。
- `int4` 压缩在部分长上下文（> 32k tokens）场景下可能出现轻微精度下降（< 0.8% BLEU），建议在业务侧做回归验证。
- > **注意**：原始文档中提及“支持 Llama 系列模型压缩”，但该能力已于 v2.3.0 版本下线，当前仅 Qwen 系列受支持，请以 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中的最新支持列表为准。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


