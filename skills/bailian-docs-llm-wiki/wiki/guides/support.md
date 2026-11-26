# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、故障排查、法律协议及售后服务等全链路支持能力。开发者可通过控制台、API、CLI 或官方渠道获取技术协助，所有支持行为均以《阿里云百炼服务协议》[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)和SLA为基准。本文档结构化梳理核心支持维度，便于快速定位解决方案。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、开源模型及部分三方模型；Qwen3-VL-Plus 已支持图片微调训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能**：
  - Completion API 与 Assistant API（含 function call 基础能力，但**不支持单次调用中依次执行两个本地函数**）；
  - RAG（[检索增强生成](../concepts/rag.md)）与 doc_reference_type 参数（仅在旧版应用生效，新版需在控制台开启“展示回答来源”开关）；
  - CLI 工具（支持 `bl auth`、`bl config` 等命令，[Token](../concepts/token.md) Plan 需显式切换 profile）；
  - 体验中心（北京/新加坡）、业务空间权限隔离、数据加密（AES-256）与合规备案支持。

> **注意**：文档 1 中称“Assistant API 当前暂不支持 memory 配置功能”，但未说明是否计划支持；文档 3 未涉及该功能描述，建议以最新控制台行为或 [API 参考文档](../../model-api-reference/preparations/error-code.md) 为准。

## 关键参数

- `doc_reference_type`：仅对旧版应用生效；新版应用需在控制台开启“展示回答来源”开关，否则该参数无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_k` / `top_p` / `max_tokens`：用于抑制幻觉，降低随机性可提升事实一致性，但可能削弱创造性。
- `RequestId`、`AppId`、`User`、`Bot`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004`。
- CLI Profile 名称（如 `default`、`token-plan`）：决定凭据类型与计费归属，`bl auth status --output json` 可验证当前生效凭据 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **开通服务**：无需手动开通，主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台并完成实名认证后自动启用 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：使用 Bearer [Token](../concepts/token.md) 认证，Header 包含 `Authorization: Bearer <api_key>`；参考 [错误码文档](../../model-api-reference/preparations/error-code.md) 解析响应。
- **SDK 集成**：支持 Python/Java，安装指引见 [安装SDK](../../model-api-reference/preparations/install-sdk.md)；多模态 Realtime API 另有独立文档。
- **CLI 操作**：
  - [Token](../concepts/token.md) Plan 使用：`bl auth login --config token-plan --api-key <sk-sp-Key>`；
  - 切换 Profile：`bl config use --name token-plan`；
  - 注意：控制台类命令（如 `app list`）需先执行 `bl auth login --console`。
- **售后反馈**：
  - 技术问题：通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat?spm=a2cwt.28446455.0.0.5bc14e0btuByqM) 提交工单；
  - 业务合作：拨打 4008013260 或使用 [售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat?spm=a2ty02.30260209.aillm.1.d8bb74a10sknig)。

## 限制和注意事项

- **服务关闭**：开通后**不支持主动关闭**，仅能通过删除 API Key 阻止后续调用。
- **数据留存**：
  - 控制台体验中心最多保留 **100 条历史对话记录**，无时间限制；未登录或报错对话不保存；
  - 所有调用数据依规加密存储，但**不用于模型训练**；详情见 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。
- **第三方工具支持边界**：
  - 仅提供阿里云百炼侧接口连通性、调用示例、计费核查等方向性建议；
  - **不支持**第三方工具（如 Cursor、Windsurf）的部署、配置、代码调试、本地环境（代理/防火墙/VPN）问题排查 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **模型能力限制**：
  - 不支持隐式标识文本生成；
  - 不支持直接对接 MySQL/Hive 等结构化数据库（RDS 对接开发中）；
  - 万相会员权益**不适用于百炼 API 调用**，计费体系完全独立。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


