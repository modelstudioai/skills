# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、故障排查、协议合规及售后响应等全链路支持能力。本文档面向开发者，聚焦可操作的技术支持要点，明确能力边界与关键约束，不包含营销性描述。所有引用均指向原始技术文档，确保信息可追溯。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相（文生图）及其他第三方模型；其中 Qwen3-VL-Plus 已支持图片微调训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能**：提供 Completion API、Assistant API、Realtime API 及 CLI 工具链；支持 RAG、Function Calling（当前仅限单次调用）、答案来源展示（需在应用配置中开启开关，`doc_reference_type` 参数在新版本中已失效）[常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据隔离**：通过业务空间（Workspace）实现多租户数据隔离，不同空间间数据完全不互通 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

> **注意**：文档 1 中第 4 条称“Assistant API 当前暂不支持 memory 配置功能”，但未说明是否计划支持；文档 3 未涉及该能力。该限制仍为当前事实，开发者需自行维护会话状态。

## 关键参数

- `temperature` / `top_p` / `top_k`：用于控制输出随机性与确定性，降低这些值可缓解幻觉，但可能牺牲创造性 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `max_tokens`：限制生成长度，防止模型在关键信息后继续捏造内容。
- `doc_reference_type`：**仅在旧版应用中生效**；新版应用需在控制台显式开启「展示回答来源」开关，否则该参数无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `RequestId`、`AppId`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004`。

## 使用方式

- **开通服务**：无需手动开通，使用主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台并完成实名认证即可自动启用 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：推荐使用 DashScope SDK（Python/Java），安装方式见 [安装SDK](raw/model-api-reference/preparations/install-sdk.md)；CLI 工具需区分 Profile（如 `token-plan`）以正确扣减资源包 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **错误排查**：所有 API 错误码定义及处理建议详见 [错误码](raw/model-api-reference/preparations/error-code.md)；CLI 凭据状态可通过 `bl auth status --output json` 查看。
- **售后服务入口**：技术问题请通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat) 提交工单；业务合作请联系 4008013260 或 [售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat) [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 限制和注意事项

- **服务关闭**：百炼服务开通后**不支持主动关闭**；如需停用，仅能删除全部 API-Key [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **第三方工具支持边界**：阿里云仅对百炼服务端本身（接口可用性、计费明细、标准连通性测试）提供支持；不负责 Cursor、Windsurf 等第三方工具的安装、配置、本地环境（代理/防火墙/VPN）、业务代码调试或其内部统计与阿里云计费的差异解释 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **数据与合规**：
  - 所有调用数据经 AES-256 加密传输，**绝不用于模型训练**；
  - 历史对话记录在控制台最多保留 100 条，无时间限制，但未登录或报错时的对话不保存；
  - 万相会员权益**不适用于百炼 API 调用**，二者计费体系完全独立 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **协议依据**：服务条款、SLA、体验功能特别说明等法律文件详见 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)，开发者应主动查阅并遵守。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


