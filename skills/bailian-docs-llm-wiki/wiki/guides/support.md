# support

阿里云百炼平台为开发者提供覆盖模型调用、部署、训练及运维全链路的技术支持服务，包括基础咨询、故障诊断、API/SDK 使用指导及计费答疑。支持渠道涵盖 7×24 智能在线、电话（95187 / 4008013260）、工单系统及官方文档。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》和《[阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)》为法律依据。

## 支持的模型/功能

- **模型范围**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相（文生图）、实时语音（Realtime API）等多模态模型；但需注意，[**万相会员**](https://tongyi.aliyun.com/wan/pricing?whereToMemberShip=upgrade)权益**不适用于百炼 API 调用**，二者计费体系完全独立 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - Completion / Assistant API 调用与调试；
  - RAG 应用构建与 `doc_reference_type` 参数行为（仅旧版应用生效，新版需在控制台开启「展示回答来源」开关）；
  - 模型微调（SFT）、结构化数据对接（RDS 正在开发中，当前不支持 MySQL/Hive）；
  - CLI 工具鉴权与 Profile 切换（如 `token-plan` Profile 用于 [Token](../concepts/token.md) Plan 扣减）；
  - 业务空间权限隔离、多账号数据隔离方案。

> **注意**：文档 1 中提到“qwen-plus-latest 属于 Qwen3 系列”，而文档 1 同时列出 Qwen3.5、Qwen3.7 为并列独立系列；该表述易引发版本归属歧义。实际应以控制台模型市场页面显示的 `model_id` 和发布说明为准，避免依赖 `latest` 后缀做版本兼容性判断 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

- `temperature` / `top_p` / `top_k`：用于控制输出随机性与确定性，降低幻觉可设为较低值（如 `temperature=0.1`, `top_p=0.8`）；
- `max_tokens`：限制生成长度，防止冗余续写导致幻觉加剧；
- `doc_reference_type`：**仅在旧版应用中生效**；新版应用需通过控制台开关启用答案溯源，参数设置无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
- `RequestId`：必须传入且全局唯一，用于问题排查与日志追踪；
- `User` / `Bot`：用于会话上下文标识，影响部分带 memory 的实验性能力（当前 Assistant API **暂不支持 memory 配置**）。

## 使用方式

- **接入路径**：
  - Web 控制台：开通服务 → 创建应用 → 获取 `AppId` 和 API Key → 调用 `/v2/app/completions` 等接口；
  - CLI：通过 `bl auth login` 配置 Profile（如 `default` 或 `token-plan`），再执行 `bl app invoke`；
  - SDK：Python/Java SDK 安装见 [安装SDK](raw/model-api-reference/preparations/install-sdk.md)，多模态 Realtime API 参考 [Realtime API 概览](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。
- **错误排查**：
  - 错误码 `100004`（参数缺失）：检查必填字段（`AppId`, `Prompt`, `RequestId`）及 JSON 格式；
  - 限流触发：根据 RPS/RPM 阈值计算等待时间（如 120 RPM ≈ 每 0.5 秒 1 次请求）；
  - 扣费异常：确认 CLI 当前 Profile 是否为 `token-plan`（`bl auth status --output json` 查看）。

## 限制和注意事项

- **服务开通与关闭**：百炼服务按地域开通，开通后**不支持主动关闭**；如需停用，须删除对应地域的 API Key [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据与隐私**：
  - 所有传输数据经 AES-256 加密；
  - 百炼**绝不会将您的数据用于模型训练**；
  - 调用日志依法规留存，详情见《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》。
- **第三方工具边界**：阿里云仅保障百炼服务端可用性与 API 正确性，**不支持第三方工具（如 Cursor、Windsurf）的安装、配置、本地环境（代理/防火墙/VPN）或业务代码调试** [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **模型能力限制**：
  - Assistant API 当前**不支持连续调用多个 function call**，需拆分为多个独立 Assistant 实例；
  - 不支持隐式内容标识、手机端独立 App、训练数据导出；
  - 体验中心历史记录最多保留 100 条，未登录/报错对话不保存。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


