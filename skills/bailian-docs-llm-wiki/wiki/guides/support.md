# support

阿里云百炼平台为开发者提供覆盖模型调用、部署、训练及运维全链路的技术支持能力，包括基础咨询、故障诊断、API/SDK 使用指导及计费答疑。支持渠道涵盖 7×24 小时智能在线、电话（95187 / 4008013260）与标准工单系统。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》和《[阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)》为法律依据。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、多模态模型及部分第三方模型；其中 Qwen3-VL-Plus 已支持图片微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - Completion API 与 Assistant API 调用（含 function call 基础能力，但**不支持连续调用两个本地函数**）；
  - RAG 应用构建与 `doc_reference_type` 参数配置（仅在旧版应用中生效，新版需通过控制台开关启用）；
  - CLI 工具（`bl`）的鉴权、Profile 切换与 [Token](../concepts/token.md) Plan 使用；
  - 模型训练（SFT）、部署、效果评估及业务空间权限隔离；
  - 数据安全与隐私保护（AES-256 加密传输，数据不用于模型训练）。

> **注意**：文档 1 中提到“Assistant API 当前暂不支持 memory 配置功能”，但未说明是否计划支持；而文档 2 明确将“使用、配置阿里云百炼模型服务的最佳实践”纳入售后范围，建议以最新控制台行为或 SDK 文档为准，memory 功能状态请参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 的更新日志。

## 关键参数

- `temperature` / `top_p` / `top_k`：用于控制生成随机性与确定性，降低幻觉可设 `temperature < 0.5`；
- `max_tokens`：限制输出长度，防止冗余捏造；
- `doc_reference_type`：仅在旧版应用中生效，新版本需在应用配置中开启「展示回答来源」开关；
- `RequestId`、`AppId`：Completion API 必填字段，缺失将返回错误码 `100004`；
- CLI Profile 名称（如 `default`、`token-plan`）：决定凭据类型与计费归属，`bl auth status --output json` 可验证当前生效凭据 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **API 调用**：通过 `Authorization: Bearer <API-Key>` 认证，推荐使用 DashScope SDK（Python/Java）封装请求逻辑，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
- **CLI 工具**：需先执行 `bl auth login` 配置凭据；[Token](../concepts/token.md) Plan 用户须显式切换至 `token-plan` Profile；
- **控制台操作**：开通服务需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号，在目标地域同意协议后自动开通；关闭服务不可逆，仅可通过删除 API-Key 阻断调用；
- **问题反馈**：产品使用类问题请通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat) 提交；业务合作请拨打 4008013260 或联系商务经理。

## 限制和注意事项

- **服务开通与关闭**：百炼服务按地域开通，开通后**不支持主动关闭**，仅能通过删除 API-Key 控制访问；
- **数据保留策略**：控制台体验中心最多保留 **100 条历史对话记录**，无时间限制；未登录或推理报错的对话不保存；
- **第三方工具支持边界**：阿里云仅对百炼服务端本身（API 可用性、计费明细、连通性测试）提供支持；**不负责 Cursor、Windsurf 等第三方工具的安装、配置、调试或本地环境（代理/防火墙/VPN）问题排查** [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)；
- **模型幻觉应对**：优先选用高阶模型（如 Qwen-Max），结合 RAG、提示词约束（如“信息不足请说‘我不知道’”）及参数调优（降低 `temperature`）降低风险；
- **计费与额度**：后付费按分钟出账、月度结算；账户可用额度必须 ≥0 元方可开通服务；万相会员权益**不适用于百炼 API 调用**。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


