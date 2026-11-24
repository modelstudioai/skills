# support

阿里云百炼平台为开发者提供覆盖模型调用、应用构建、计费管理及故障排查的全链路技术支持。支持形式包括自助文档、API/SDK 工具链、7×24 小时工单与电话服务，以及面向企业客户的付费增值服务。所有服务均以《阿里云百炼服务协议》和《SLA》为法律与服务质量基准。

## 支持的模型/功能

- **模型范围**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen3-vl-plus 等）、开源模型及三方模型（详见[三方模型服务协议和使用条款清单](../../raw/model-user-guide/support/related-agreements.md)）；其中 qwen3-vl-plus 已支持图片微调训练。
- **核心能力**：
  - Completion / Assistant API 调用（含 function call 基础支持，但**不支持连续调用两个本地函数**）；
  - RAG 应用构建与 doc_reference_type 参数控制（仅在旧版应用中生效，新版需通过控制台开关启用）；
  - CLI 工具（`bl`）支持模型推理、[Token](../concepts/token.md) Plan 切换及多 Profile 管理；
  - 业务空间（Workspace）级数据隔离，保障多租户数据不关联。

> **注意**：文档 2 中称“Assistant API 当前暂不支持 memory 配置功能”，但未说明是否计划支持；该限制应视为当前稳定行为，非临时缺陷。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `temperature`, `top_p`, `top_k` | 控制生成随机性与确定性 | 降低可减少幻觉，但可能削弱创造性；需结合人工评估验证效果 |
| `max_tokens` | 限制响应长度 | 过长易引发后半段捏造，建议按任务需求设合理上限 |
| `doc_reference_type` | 指定答案来源展示格式 | **仅在旧版应用中生效**；新版必须开启控制台「展示回答来源」开关才生效（见[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)） |
| `RequestId`, `AppId` | 必填请求标识字段 | 缺失或格式错误将返回错误码 `100004`（参数缺失） |

## 使用方式

- **开通服务**：无需手动开通，主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台并完成实名认证后自动启用；
- **API 调用**：使用 Bearer [Token](../concepts/token.md) 认证，Header 中携带 `Authorization: Bearer <api_key>`，Body 为 JSON 格式（示例见[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)）；
- **SDK 安装**：DashScope SDK 支持 Python/Java；多模态 Realtime API 需单独参考对应文档；
- **CLI 鉴权**：支持多 Profile（如 `default`、`token-plan`、`console`），需显式切换（`bl config use --name token-plan`）方可使用 [Token](../concepts/token.md) Plan 扣减；
- **售后接入**：
  - 基础咨询：官网[售后服务](https://smartservice.console.aliyun.com/service/robot-chat)、电话 95187 / 4008013260；
  - 工单与深度支持：参见[阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **功能限制**：
  - Assistant API 不支持 memory 配置、不支持连续 function call；
  - 不支持导出训练完成的开源模型；
  - 不支持直接对接 MySQL/Hive 等结构化数据库（RDS 对接已在开发中）；
  - 未登录状态下的体验对话、推理报错对话**不保存**；控制台最多保留 100 条历史记录。
  
- **计费与账户**：
  - 万相会员权益**不适用于百炼 API 调用**；
  - 后付费按分钟出账、按月结算；账户余额须 ≥ 0 元方可开通服务；
  - CLI 调用 Token Plan 需使用订阅 API Key 并切换至 `token-plan` Profile，否则不扣减。

- **数据与安全**：
  - 百炼**不会将用户数据用于模型训练**，传输全程 AES-256 加密；
  - 数据存储依据《阿里云百炼服务协议》执行，详情见[相关协议](../../raw/model-user-guide/support/related-agreements.md)；
  - 第三方工具（如 Cursor、Windsurf）的部署、配置及故障排查**不在标准售后范围内**，仅提供方向性接入建议。

- **模型行为**：
  - 模型重复输出、幻觉等问题与训练数据质量、prompt 设计、参数配置强相关；
  - 降低 `temperature` 等参数可缓解幻觉，但最终效果须以人工评估为准（loss 不是可靠过拟合指标）。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


