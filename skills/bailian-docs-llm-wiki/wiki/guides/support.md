# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、故障排查、售后响应范围及法律合规依据等全链路支持能力。它面向开发者提供标准化的技术支持入口与明确的服务边界，不包含对第三方工具或用户侧环境的深度运维责任。所有服务均以阿里云主账号权限体系和《阿里云百炼服务协议》为前提。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen3-vl-plus 等）、开源模型及三方模型，其中 qwen3-vl-plus 已支持图像训练 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **核心功能**：Completion API、Assistant API（当前不支持连续 function call 或 memory 配置）、RAG 增强生成、模型微调（SFT）、体验中心对话（最多保留 100 条历史记录）；  
- **数据隔离**：通过业务空间（Workspace）实现多租户数据物理隔离，不同子账号可被授予独立空间权限 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **安全与合规**：所有传输数据经 AES-256 加密，不用于模型训练；数据存储与处理条款详见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。

> **注意**：文档 2 中提到“qwen-plus-latest 属于 Qwen3 系列”，但未明确其与 Qwen3.5/Qwen3.7 的版本关系；而 Qwen3.5、Qwen3.7 实为并列独立系列，并非 Qwen3 子版本——该表述易引发歧义，实际应以控制台模型市场展示的 `model_id` 和版本标签为准。

## 关键参数

- `doc_reference_type`：仅在旧版应用中生效；新版需在控制台开启「展示回答来源」开关，否则该参数无效 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- `temperature` / `top_p` / `top_k` / `max_tokens`：可用于抑制幻觉（如降低 `temperature` 提高确定性，限制 `max_tokens` 防止冗余捏造）；  
- 请求头必需字段：`Authorization: Bearer <API-Key>`、`Content-Type: application/json`；  
- 必填请求体字段（Completion API）：`AppId`、`Prompt`、`RequestId`；缺失或格式错误将返回错误码 `100004`。

## 使用方式

- **开通服务**：无需手动开通，使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台，完成实名认证后自动启用；RAM 账号需由主账号显式授权 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **API 调用**：推荐使用 DashScope SDK（Python/Java），安装方式见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；CLI 工具需区分 Profile（如 `token-plan`）以正确扣减资源包 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **错误排查**：所有 API 错误码含义及解决方案参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- **售后接入**：7×24 小时支持渠道包括电话（95187 / 4008013260）、智能在线、标准工单；业务合作请通过[售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；产品问题反馈请使用[售后服务](https://smartservice.console.aliyun.com/service/robot-chat) [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **服务关闭**：开通后暂不支持主动关闭服务；如需停用，仅需删除控制台中已创建的 API-Key 即可终止调用 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **第三方工具支持边界**：阿里云仅提供方向性建议（如接口连通性测试、官方 SDK 示例、计费明细核查），**不负责**第三方工具（如 Cursor、Windsurf）的安装配置、本地环境（代理/防火墙/VPN）、业务代码调试或跨云服务集成问题 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)；  
- **模型幻觉应对**：无法完全消除，但可通过更强模型选型、RAG、提示词约束、参数调优（如 `temperature=0.1`）及后处理验证组合降低 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **数据导出与训练**：训练完成的开源模型暂不支持导出；自定义模型仅支持百炼平台内训练产出的模型二次微调，不支持本地训练模型上传 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **万相会员限制**：万相会员权益与百炼 API 调用完全隔离，不可用于抵扣百炼计费 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


