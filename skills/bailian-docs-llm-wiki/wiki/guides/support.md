# support

阿里云百炼平台为开发者提供覆盖模型调用、部署、训练及运维全链路的技术支持能力，包括基础咨询、故障诊断、API/SDK 使用指导与计费答疑。支持渠道涵盖 7×24 智能在线、工单系统、电话热线（95187 / 4008013260）及控制台内嵌帮助。所有服务均以《阿里云百炼服务协议》及 SLA 为法律与质量基准，第三方工具集成问题仅限方向性建议。

## 支持的模型/功能

- **模型范围**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相等多模态模型，但需注意：**万相会员权益不适用于百炼 API 调用**，二者计费体系完全独立 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - 模型推理（Completion、Assistant API）、RAG 应用构建、自定义模型微调（SFT）；
  - 图片训练（qwen3-vl-plus 已支持），但暂不支持结构化数据源（如 MySQL、Hive）直连，RDS 对接正在开发中；
  - CLI 工具（`bl` 命令）的鉴权、Profile 切换与 [Token](../concepts/token.md) Plan 使用；
  - 控制台体验中心（最多保留 100 条登录态历史对话）及业务空间权限隔离。

> **注意**：文档 1 中“模型训练中的自定义模型怎么上传？”明确指出“若您自己在本地训练的模型不支持上传”，而文档 2 未提及该限制；此处以文档 1 的明确声明为准，即**百炼平台不接受用户本地训练模型的上传与二次微调**。

## 关键参数

- `doc_reference_type`：仅在旧版应用中生效；新版应用需在控制台开启「展示回答来源」开关，否则该参数无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_p` / `top_k` / `max_tokens`：可用于抑制幻觉——降低随机性参数可使输出更保守，缩短 `max_tokens` 可防止关键信息后捏造内容。
- 请求级标识：`RequestId` 为必填字段（见 Completion API 示例），用于问题定位与计费追溯；`AppId`、`User`、`Bot` 同样为必需参数。

## 使用方式

- **开通服务**：需使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号，在目标地域控制台开通；RAM 用户须提前由主账号授权，且账户余额 ≥ 0 元 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：推荐使用 DashScope SDK（Python/Java），安装与配置详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；CLI 用户需通过 `bl auth login --config token-plan` 显式切换 Profile 才能使用 [Token](../concepts/token.md) Plan 席位。
- **售后响应**：基础服务提供 7×24 小时智能在线与工单支持；复杂问题（如定制化集成、业务代码调试）需联系商务经理评估付费增值服务 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **服务不可关闭**：开通后无法主动关闭百炼服务，如需停用，仅能删除 API-Key 避免后续调用。
- **数据隐私与存储**：所有传输数据经 AES-256 加密；调用数据依法律法规留存，**绝不用于模型再训练**；具体条款详见 [《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)。
- **第三方工具边界**：阿里云仅对百炼服务端状态、API 可达性、官方 SDK 示例及计费明细提供支持；Cursor、Windsurf 等第三方工具的部署、配置、内部报错及本地环境（代理/防火墙/OS）问题不在支持范围内 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **限流与重试**：触发限流后，等待时间取决于您的 RPS/RPM 配置（例如 120 RPM 即每秒 2 次请求，超频后需等待约 0.8 秒）；错误码详情请查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


