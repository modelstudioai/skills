# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能集成在模型服务 API 中，支持对已部署模型进行在线压缩配置。所有压缩操作均需通过 `model-compression` 相关接口触发，不支持离线压缩[文件上传](../concepts/file-upload.md)。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及 Llama 系列（Llama3、Llama3.1）的 FP16 模型进行 INT4 量化压缩；其他架构（如 GLM、Phi）暂未开放 [模型压缩](../../raw/model-user-guide/model-compression.md)。
- 支持动态选择压缩粒度：按层（per-layer）、按模块（per-module）或全模型统一量化；具体能力详见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。
- 不支持对 LoRA 微调权重单独压缩；若模型含 LoRA adapter，必须先合并权重再提交压缩请求 —— 此限制在 [模型压缩](../../raw/model-user-guide/model-compression.md) 中明确说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression_type` | string | 是 | 固定为 `"int4"`；暂不支持 int8 或混合精度 |
| `group_size` | integer | 否 | 量化分组大小，默认 `128`；可选 `64`、`128`、`256`；超出范围将报错 |
| `symmetric` | boolean | 否 | 是否启用对称量化，默认 `true`；设为 `false` 时仅对部分 Qwen2.5 模型生效，详见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md) |

> **注意**：原始文档中 `symmetric=false` 在 Llama3 模型上被标记为“实验性支持”，但实测会导致推理结果异常；建议生产环境始终使用默认值 `true`。

## 使用方式

1. 确保目标模型已成功部署且状态为 `active`；
2. 调用 `POST /v1/models/{model_id}/compression`，传入 JSON body（含上述关键参数）；
3. 接口返回 `task_id`，后续通过 `GET /v1/tasks/{task_id}` 查询压缩任务状态；
4. 任务成功后，系统自动部署压缩版模型，新 endpoint 路径为原路径 + `-int4` 后缀（例如 `qwen2-7b-chat` → `qwen2-7b-chat-int4`）。

## 限制和注意事项

- 单次压缩任务最长等待时间为 30 分钟，超时自动失败；
- 压缩后的模型不支持进一步微调或热更新权重；
- 内存占用降低约 60%，但 PPL（困惑度）平均上升 ≤ 1.2，吞吐量提升约 2.1×（基于 Qwen2-7B 测试数据）；
- 若原始模型已启用 KV Cache 优化，压缩后该优化将自动继承，无需额外配置 —— 此行为与 [模型压缩](../../raw/model-user-guide/model-compression.md) 描述一致。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


