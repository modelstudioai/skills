# support

阿里云百炼平台为开发者提供覆盖模型调用、部署、训练及运维全链路的技术支持能力，包括基础咨询、故障诊断、API/SDK 使用指导与计费答疑。支持范围以服务协议和 SLA 为法律依据，同时明确区分平台原生能力与第三方集成场景的责任边界。所有服务均面向已实名认证并完成权限配置的主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen3-vl-plus 等）、开源模型及三方模型；其中 qwen3-vl-plus 已支持图像微调训练 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能**：Completion API、Assistant API（含 function call 基础能力）、RAG 应用构建、SFT 微调、体验中心对话、业务空间隔离等。
- **不支持能力**：Assistant API 当前暂不支持 memory 配置；不支持分别调用两个本地函数（需手动创建两个 Assistant 实例）；不支持结构化数据库（如 MySQL、Hive）直连，RDS 对接正在开发中 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

> **注意**：文档 2 中提及“qwen-plus-latest 属于 Qwen3 系列”，但未说明其与 Qwen3.5/Qwen3.7 的版本关系；经核实，Qwen3.5、Qwen3.7 是独立并列系列，并非 Qwen3 子版本，该表述易引发歧义，应以[相关协议](../../raw/model-user-guide/support/related-agreements.md)中模型命名规范为准。

## 关键参数

- `doc_reference_type`：仅在旧版本应用中生效；新版本需在控制台开启「展示回答来源」开关，否则该参数无效 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_p` / `top_k` / `max_tokens`：用于抑制幻觉，降低随机性可提升事实一致性，但可能削弱创造性输出。
- 请求头必需字段：`Authorization: Bearer <API-Key>`、`Content-Type: application/json`；请求体必需字段依接口而定（如 `AppId`、`Prompt`）。

## 使用方式

- **开通服务**：无需手动开通，使用主账号或已授权 `AliyunBailianFullAccess` 的 RAM 账号登录控制台，满足实名认证后自动启用。
- **API 调用**：推荐使用 DashScope SDK（Python/Java），安装指引见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；CLI 工具支持多 Profile 管理，[Token](../concepts/token.md) Plan 需显式切换至 `token-plan` Profile 才生效 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **错误排查**：报错 `100004（参数缺失）` 需检查必填字段及 JSON 格式；所有错误码含义及解决方案详见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档。
- **售后渠道**：7×24 小时支持通过官网智能在线、电话（95187 / 4008013260）、标准工单；生产环境问题建议优先提交工单 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **数据隐私**：百炼不会将用户输入数据用于模型训练；所有传输数据经 AES-256 加密；但根据法规要求，调用日志等元数据将被存储，具体条款参见 [《阿里云百炼服务协议》](../../raw/model-user-guide/support/related-agreements.md)。
- **历史记录**：控制台体验中心最多保留 100 条对话记录，无时间限制；未登录状态及推理失败的对话不保存。
- **服务关闭**：平台服务开通后不可关闭，如需停用，须在 API-Key 管理页删除全部 Key。
- **第三方集成**：阿里云仅对百炼服务端状态、API 可达性、官方 SDK 使用提供支持；第三方工具（如 Cursor、Windsurf）的安装、配置、本地网络/代理/防火墙问题、业务代码实现等不在支持范围内 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **模型幻觉**：属大模型固有现象，可通过选择更强模型（如 Qwen-Max）、优化 [prompt](prompt.md)、启用 RAG、调低 `temperature` 等方式缓解；但无法完全消除。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


