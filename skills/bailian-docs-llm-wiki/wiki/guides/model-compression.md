# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发低延迟场景。该功能集成在 `model.deploy` 接口的 `compression` 字段中，支持对已发布的模型版本进行无损/有损压缩配置。所有压缩操作均在服务端完成，用户无需本地执行转换。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）和 Qwen-VL 的 FP16 模型版本进行 INT4 量化压缩；不支持 LoRA 微调后未合并权重的模型。
- 支持两种压缩模式：`int4_weight_only`（权重 INT4 + 激活 FP16）和 `int4_weight_activation`（权重与激活均 INT4），后者需显存 ≥24GB 且仅限 A10/A100 卡型。
- 剪枝、知识蒸馏等高级压缩方式暂未开放，详见 [模型压缩](../../raw/model-user-guide/model-compression.md) 的功能矩阵说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression.type` | string | 是 | 取值为 `"int4_weight_only"` 或 `"int4_weight_activation"` |
| `compression.calibration_dataset` | string | 否 | 校准数据集 ID（如 `calib-2024-qwen2`），仅当 type 为 `int4_weight_activation` 时生效；默认使用平台内置校准集 |
| `compression.quantization_aware` | boolean | 否 | 是否启用量化感知训练（QAT）模拟，仅对已支持 QAT 的模型版本有效；参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中的兼容性列表 |

> **注意**：`compression.quantization_aware=true` 在 v3.2.1 版本后仅对 Qwen2-7B-Instruct 及以上版本生效；旧版模型设置该参数将被静默忽略——此行为与 [模型压缩](../../raw/model-user-guide/model-compression.md) 中“参数兼容性”章节描述存在偏差，以当前 API 实际行为为准。

## 使用方式

1. 确保目标模型已发布且状态为 `active`；
2. 调用 `POST /v1/models/{model_id}/versions/{version_id}/deploy`，在请求体中嵌入 `compression` 对象；
3. 示例（INT4 权重压缩）：
   ```json
   {
     "instance_type": "a10",
     "compression": {
       "type": "int4_weight_only"
     }
   }
   ```
4. 部署成功后，可通过 `/v1/deployments/{deployment_id}` 查看 `compression_status: "completed"` 及实际量化误差指标（如 `max_activation_error: 0.023`）。

## 限制和注意事项

- 单次压缩任务最长等待 45 分钟，超时自动失败；若校准数据集过大（>10k 样本），建议先抽样至 2k–5k；
- 压缩后的模型不支持热更新权重，需重新部署新版本；
- INT4 激活压缩会导致部分长文本生成质量下降（尤其在数学推理类 prompt 下），建议在业务侧做 A/B 测试；详细评估方法见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的效果验证章节。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


