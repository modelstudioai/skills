# support

阿里云百炼平台的 `support` 模块涵盖模型服务使用过程中的全链路支持能力，包括售后服务范围、问题排查路径、计费与权限咨询、API/SDK 故障诊断等。开发者可通过官方渠道获取 7×24 基础技术支持，同时需明确平台责任边界——阿里云仅保障百炼服务端（API、控制台、计费系统）的可用性与一致性，不承担第三方工具、本地环境或业务代码层面的问题。所有法律与合规依据以签署的服务协议为准。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、开源模型及三方模型，其中 Qwen3-VL-Plus 已支持图像微调训练 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - Completion / Assistant API 调用与 function call 逻辑（当前不支持单次调用中连续触发两个本地函数）；
  - RAG 应用配置（`doc_reference_type` 参数仅在旧版应用生效，新版需通过控制台开启「展示回答来源」开关）；
  - CLI 工具的鉴权与 Profile 切换（如 `token-plan` Profile 专用于 Token Plan 扣减）；
  - 业务空间（Workspace）级数据隔离，实现多租户数据物理分离 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

> **注意**：文档 2 中称“qwen-plus-latest 属于 Qwen3 系列”，但未明确其与 Qwen3.5/Qwen3.7 的版本关系；而文档 2 第 17 条明确指出“Qwen3.5、Qwen3.7 是独立并列的模型系列，非 Qwen3 子版本”。因此 `qwen-plus-latest` 与 Qwen3.5 无继承关系，该命名易引发误解，实际应以控制台模型市场实时列表为准。

## 关键参数

- `doc_reference_type`：仅对旧版应用生效；新版应用须在控制台启用「展示回答来源」开关，否则该参数无效 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_p` / `top_k` / `max_tokens`：可用于抑制模型幻觉，降低随机性输出，但需结合人工评估验证效果，不可仅依赖 loss 曲线判断过拟合 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `RequestId`、`AppId`、`User`、`Bot`：Completion API 必填字段，缺失或格式错误将返回错误码 `100004`。

## 使用方式

- **开通服务**：无需手动开通，主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台后自动启用；RAM 用户需由主账号预先授权 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **API 调用**：
  - 使用 Bearer Token 认证，Header 中必须包含 `Authorization: Bearer <api_key>`；
  - 错误码详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
  - SDK 安装参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)，多模态 Realtime API 另有专用文档。
- **CLI 工具**：
  - 需区分 Profile：`default`（普通 API Key）与 `token-plan`（订阅 Key），后者需显式登录并切换；
  - `bl auth status --output json` 查看当前凭据，`bl config use --name token-plan` 切换生效 Profile。

## 限制和注意事项

- **数据隐私与存储**：阿里云不将用户数据用于模型训练，传输全程 AES-256 加密；但根据法规要求，调用日志等元数据会被保留，具体条款详见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。
- **服务关闭**：百炼服务开通后不可主动关闭，如需停用，仅能删除全部 API Key 阻断调用入口。
- **第三方集成边界**：
  - 阿里云仅提供百炼服务端连通性验证、标准 API 示例、计费明细核查等方向性建议；
  - 不支持 Cursor/Windsurf 等第三方工具的部署、配置、故障排查，亦不解释其内部 Token 统计与阿里云账单的差异 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **模型幻觉应对**：优先采用 RAG + 提示词约束 + 强模型选型组合策略；单纯调参（如降 `temperature`）可能牺牲响应多样性，须实测权衡。
- **体验中心限制**：控制台体验对话最多保留 100 条历史记录，未登录或报错会话不保存。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


