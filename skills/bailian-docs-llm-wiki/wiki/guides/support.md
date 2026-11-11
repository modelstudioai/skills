# support

阿里云百炼平台的 `support` 模块涵盖面向开发者的全链路技术支持体系，包括服务开通与计费、API/SDK 使用问题排查、模型能力边界说明、售后服务范围界定及法律协议依据。本文档结构化梳理核心支持信息，聚焦可操作性，避免重复引用控制台操作路径或营销性描述。所有技术细节均以最新公开文档为准，矛盾处已标注。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相等多模态模型；其中 Qwen3-VL-Plus 明确支持图片训练微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **功能范围**：提供 Completion API、Assistant API（含 function call 基础能力）、RAG、插件/MCP 集成、模型微调（SFT）及业务空间隔离能力；但 Assistant API 当前不支持 memory 配置，且不支持单次调用中依次执行两个本地函数 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据对接**：当前不支持直接对接 MySQL、Hive 等结构化数据源，RDS 接入正在开发中；万相会员权益与百炼 API 调用完全独立，不可复用 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

> **注意**：文档 1 中“qwen-plus-latest 属于 Qwen3 系列”与部分内部命名习惯存在偏差，实际应以控制台模型市场展示的版本标识为准；Qwen3.5、Qwen3.7 为并列独立系列，非 Qwen3 子版本。

## 关键参数

- **`doc_reference_type`**：仅在旧版应用中生效；新版需在控制台应用配置中开启「展示回答来源」开关，否则该参数无效。
- **随机性控制**：`temperature`、`top_k`、`top_p` 可降低幻觉，但需权衡输出多样性；`max_tokens` 过大可能加剧无依据续写。
- **CLI 凭据切换**：Token Plan 需显式使用 `bl auth login --config token-plan` 登录专属 Profile，普通 `default` Profile 不触发 Token 扣减 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **服务开通**：须使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号，在目标地域控制台开通；RAM 用户需提前由主账号授权，且账户须完成实名认证 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：必须携带 `Authorization: Bearer <API-Key>` 及必要字段（如 `AppId`, `Prompt`），缺失或格式错误将返回错误码 `100004`；错误码详情见 [错误码文档](raw/model-api-reference/preparations/error-code.md)。
- **售后接入**：
  - 基础咨询：通过官网[售后服务](https://smartservice.console.aliyun.com/service/robot-chat)提交工单或拨打 95187/4008013260；
  - 技术支持范围严格限定于百炼平台自身服务（API、SDK、控制台、计费系统），不包含第三方工具部署、用户代码调试或本地网络环境问题 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **服务关闭**：百炼服务开通后暂不支持主动关闭；如需停用，仅能删除 API-Key 避免后续调用。
- **数据留存**：控制台体验中心最多保留 100 条历史对话（无时间限制），未登录状态及推理报错对话不保存；所有调用数据按《阿里云百炼服务协议》存储，加密方式为 AES-256 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **法律与合规**：模型调用须遵守《阿里云百炼服务协议》《SLA 协议》《体验功能特别说明》等条款，开源模型使用需额外遵循对应 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)；商业化上架需单独申请备案与合作协议 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。
- **第三方责任边界**：阿里云不为 Cursor、Windsurf 等第三方工具的安装、配置、故障或其与百炼集成中的兼容性问题担责；仅提供方向性建议（如接口连通性测试、官方 SDK 示例） [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


