# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发低延迟场景。该功能集成在 `model.deploy` 接口的 `compression` 字段中，支持对已发布的模型版本进行无损/有损压缩配置。所有压缩操作均在服务端完成，用户无需本地执行转换。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）和 Qwen-VL 的 FP16 模型版本进行 INT4 量化压缩；不支持 LoRA 微调后未合并权重的模型。
- 支持两种压缩模式：`int4_weight_only`（权重 INT4 + 激活 FP16）和 `int4_weight_activation`（权重与激活均 INT4），后者需显存 ≥24GB 且仅限 A10/A100 卡型。
- 剪枝、知识蒸馏等高级压缩方式暂未开放，详见 [模型压缩](../../raw/model-user-guide/model-compression.md) 的功能路线图说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression.type` | string | 是 | 取值为 `"int4_weight_only"` 或 `"int4_weight_activation"` |
| `compression.group_size` | integer | 否 | 权重量化分组大小，默认 `128`；设为 `0` 表示全量统一量化（不推荐） |
| `compression.quant_method` | string | 否 | 仅当 type 为 `int4_weight_activation` 时有效，取值 `"awq"` 或 `"gptq"`；默认 `"awq"` |

> **注意**：`compression.quant_method` 在 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中被错误标注为必填项，实际为可选参数，以本页为准。

## 使用方式

1. 调用 `model.deploy` 创建部署实例时，在 `spec.compression` 字段中配置压缩参数：
   ```json
   {
     "spec": {
       "model_id": "qwen2-7b",
       "compression": {
         "type": "int4_weight_only",
         "group_size": 128
       }
     }
   }
   ```
2. 部署成功后，可通过 `model.get` 查看 `status.compression_status` 字段确认压缩状态（`"completed"` / `"failed"`）。
3. 压缩后的模型 endpoint 与原模型完全兼容，无需修改客户端请求格式 —— 此行为已在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中明确约定。

## 限制和注意事项

- 单次压缩任务最长等待时间为 15 分钟，超时将自动失败并释放资源；
- 压缩过程不可中断，且不支持取消或重试；若失败，请检查原始模型是否满足 [模型压缩介绍](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中的兼容性要求；
- 已启用压缩的模型实例不支持后续变更 `compression` 配置，如需调整，必须重新部署新实例。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


