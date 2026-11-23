# support

阿里云百炼平台的 `support` 体系涵盖计费、API/SDK、产品使用、模型能力、法律协议及售后服务等维度，为开发者提供全链路技术支撑。本文档结构化梳理核心支持能力与约束条件，聚焦可操作信息，避免冗余说明。所有引用均指向原始文档权威出处，矛盾处已明确标注。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相等多模态模型；其中 Qwen3-VL-Plus 已支持图片训练微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **功能范围**：提供 Completion API、Assistant API、Realtime API 及 CLI 工具；支持 RAG、Function Calling（当前仅限单次调用）、文档引用（`doc_reference_type` 仅在旧版应用生效）[常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据隔离**：通过业务空间（Workspace）实现租户级数据隔离，不同子账号分配独立空间后数据完全不互通 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

> **注意**：文档 1 中称“Assistant API 当前暂不支持 memory 配置功能”，但未说明是否计划支持；若需会话状态管理，须由调用方自行维护上下文。

## 关键参数

- `temperature` / `top_p` / `top_k`：用于控制输出随机性与确定性，降低幻觉可设 `temperature=0.1`、`top_p=0.8` 等保守值；
- `max_tokens`：限制生成长度，防止模型在关键信息后持续捏造内容；
- `doc_reference_type`：仅在旧版应用中生效，新版需在控制台开启「展示回答来源」开关才起作用；
- `RequestId`：必须参数，用于问题排查与计费追溯（见 Completion API 示例）。

## 使用方式

- **开通服务**：无需手动开通，主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台并完成实名认证后自动启用；
- **API 调用**：需使用有效 API Key（北京或新加坡地域），Header 中携带 `Authorization: Bearer <api_key>`；
- **CLI 工具**：Token Plan 需显式切换 Profile（如 `bl config use --name token-plan`），普通 API Key 不触发 Token 扣减 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
- **售后接入**：7×24 小时支持渠道包括官网智能在线、电话（95187 / 4008013260）及标准工单；深度定制需求（如代码级集成指导）需联系商务经理订购增值服务 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **功能限制**：
  - Assistant API 不支持连续调用两个本地函数，也不支持 memory 配置；
  - 不支持将百炼 API 直接对接 MySQL/Hive 等结构化数据库（RDS 对接已在开发中）；
  - 万相会员权益**不适用于**百炼 API 调用，二者计费体系完全独立；
  - 训练完成的开源模型**不支持导出**；
  - 控制台体验中心最多保留 100 条历史对话，未登录或报错对话不保存。

- **安全与合规**：
  - 所有传输数据经 AES-256 加密，阿里云**绝不使用客户数据训练模型**；
  - 数据存储受《阿里云百炼服务协议》约束，详情见 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)；
  - 应用上架需单独完成备案与合作协议申请，流程见 [应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

- **第三方工具免责**：
  > **注意**：阿里云仅保障百炼服务端可用性与接口规范，对 Cursor、Windsurf 等第三方工具的安装、配置、兼容性及内部统计差异**不提供技术支持**，亦不承担其行为导致的责任 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


