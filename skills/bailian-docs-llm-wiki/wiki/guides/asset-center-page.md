# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理模型、向量模型等）的核心页面，提供模型的上传、版本管理、部署配置与权限控制能力。开发者可通过该页面完成模型生命周期的关键操作，包括发布、下线、查看元信息及访问凭证管理。所有操作均需通过百炼控制台或 OpenAPI 接口触发，前端 UI 与后端服务强绑定。

## 支持的模型/功能

资产中心支持以下模型类型及其对应功能：
- **微调模型（Fine-tuned Model）**：支持 LoRA/全参数微调模型的上传、版本快照、评估指标关联；
- **推理模型（Inference Model）**：支持 ONNX、PyTorch、TensorRT 格式模型的注册与在线推理服务绑定；
- **向量模型（Embedding Model）**：支持 HuggingFace 格式文本嵌入模型的部署，自动适配 RAG 场景的向量化接口；
- **自定义容器模型（Custom Container）**：允许用户通过 Docker 镜像方式注册任意框架模型，需满足 [原文标题](../../raw/model-user-guide/asset-center-page.md) 中定义的健康检查与 HTTP 协议规范。

> **注意**：文档 [原文标题](../../raw/model-user-guide/asset-center-page.md) 中提及“支持 TensorFlow SavedModel 格式”，但当前 v3.2.0 平台已移除此格式支持，实际仅兼容 ONNX 和 PyTorch；请以控制台上传界面的格式下拉选项为准。

## 关键参数

在注册或更新模型资产时，以下参数为必填且影响后续部署行为：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model_id` | string | 全局唯一标识，命名需符合正则 `^[a-z][a-z0-9\-]{2,63}$`，不可修改 |
| `version` | string | 语义化版本（如 `v1.2.0`），同一 `model_id` 下不可重复 |
| `framework` | enum | 取值：`pytorch` / `onnx` / `trt` / `custom`，必须与实际模型格式一致 |
| `input_schema` | JSON Schema | 定义请求体结构，用于自动生成 API 文档和校验，详见 [原文标题](../../raw/model-user-guide/asset-center-page.md) 的 Schema 示例章节 |

## 使用方式

1. **控制台操作路径**：登录百炼控制台 → 进入「模型资产」→ 「资产中心」→ 点击「新建模型」或选择已有模型进入详情页；
2. **API 调用方式**：调用 `POST /v1/assets/models` 注册新模型，或 `PUT /v1/assets/models/{model_id}/versions/{version}` 发布新版本；
3. **CLI 辅助工具**：使用 `bailian-cli asset upload --model-id my-llm --version v1.0.0 --path ./model.onnx` 命令快速上传（需提前配置 AK/SK）。

## 限制和注意事项

- 单个模型文件大小上限为 10 GB；超限需分片上传或使用对象存储预置 URL；
- 同一 `model_id` 最多保留 50 个历史版本，超出后旧版本将被自动归档（不可恢复）；
- 自定义容器模型必须暴露 `/health` 和 `/predict` 两个 HTTP 端点，且响应延迟需 ≤ 5s（P99），否则部署失败；
- 所有模型资产默认私有，共享需显式设置 `visibility: public` 并通过 IAM 策略授权，权限变更即时生效。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


