# support

阿里云百炼平台为开发者提供覆盖模型调用、应用构建、计费与运维的全链路技术支持。本文档系统梳理了平台支持的核心能力范围、关键参数配置、标准使用方式，以及明确的服务边界与限制条件，帮助开发者快速定位问题并高效对接支持资源。所有内容均基于官方最新发布的技术文档整理，适用于生产环境集成与问题排查。

## 支持的模型/功能

百炼平台支持调用千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相等多模态模型，涵盖文本生成、图像理解、[函数调用](../concepts/function-calling.md)（Function Calling）、RAG 增强推理等核心能力。其中，qwen3-vl-plus 已支持图片训练微调；但 Assistant API 当前**不支持连续调用多个本地函数**，也**暂不支持 memory 配置功能**（详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）。RAG 场景下，`doc_reference_type` 参数仅在旧版应用中生效，新版需通过控制台开启「展示回答来源」开关（同上文）。

> **注意**：文档 1 中提到“当前不支持对接 MySQL 和 Hive 等结构化数据”，而文档 2 明确说明“已在开发中，优先对接 RDS 服务”。该功能尚未上线，开发者应以控制台实际可用能力为准，避免依赖未发布的接口。

## 关键参数

- `temperature`、`top_k`、`top_p`：用于控制输出随机性与确定性，降低幻觉可适当减小 `temperature`（如设为 0.1–0.3）和 `top_p`（如设为 0.8）；
- `max_tokens`：限制响应长度，防止模型在关键信息后继续捏造内容；
- `doc_reference_type`：仅对旧版应用有效，新版需通过控制台开关启用答案溯源（参见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）；
- CLI 使用中需注意 Profile 隔离：Token Plan 必须通过 `--config token-plan` 显式指定，否则不会扣减订阅额度（参见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）。

## 使用方式

- **开通服务**：需使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号，在目标地域控制台开通（[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）；
- **API 调用**：推荐使用 DashScope SDK（Python/Java），或直接调用 RESTful 接口（如 `/v2/app/completions`），需携带 `Authorization: Bearer <API-Key>` 及必要字段（`AppId`, `Prompt` 等）；
- **CLI 工具**：通过 `bl auth login` 配置凭据，`bl config use` 切换 Profile，`bl auth status --output json` 查看当前生效凭证；
- **售后接入**：技术问题优先通过官网[售后服务](https://smartservice.console.aliyun.com/service/robot-chat)提交工单；业务合作请联系 4008013260 或[售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)。

## 限制和注意事项

- **服务不可关闭**：开通后无法主动关闭百炼服务，如需停用，仅能删除 API-Key（[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）；
- **数据隔离**：通过业务空间（Workspace）实现租户级数据隔离，不同空间间数据完全不互通；
- **第三方工具支持边界**：阿里云仅对百炼服务端本身（API 可用性、计费明细、连通性测试）提供支持；第三方工具（如 Cursor、Windsurf）的安装、配置、本地环境（代理/防火墙/VPN）及业务代码问题**不在支持范围内**（详见 [售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)）；
- **协议约束**：所有使用行为须遵守《[阿里云百炼服务协议](../../raw/model-user-guide/support/related-agreements.md)》及《SLA 协议》，特别是数据隐私、加密存储（AES-256）与禁止用于模型训练等条款；
- **模型幻觉应对**：除参数调优外，强烈建议结合 RAG、插件/MCP 或后处理验证机制，单一参数调整无法根治幻觉（参见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


