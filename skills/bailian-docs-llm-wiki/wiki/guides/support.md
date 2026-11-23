# support

阿里云百炼平台的 `support` 体系涵盖技术咨询、故障诊断、计费与合规保障、售后响应等多维度服务，面向开发者提供从接入到生产运维的全周期支撑。核心支持能力基于官方控制台、API/SDK、CLI 工具链及法律协议框架展开，不依赖第三方工具或非平台原生能力。所有服务均以阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号为前提 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相（仅图像生成，**不支持百炼 API 调用**）及其他平台托管模型；Qwen3-VL-Plus 已支持图文多模态微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **功能范围**：
  - 模型推理（Completion / Assistant API）、RAG 应用构建、自定义模型微调（SFT）、体验中心交互；
  - 不支持：本地模型上传、训练后模型导出、结构化数据库（MySQL/Hive）直连（RDS 正在开发中）、Assistant API 的 memory 配置或连续 function call 调用；
  - 幻觉缓解能力依赖提示词工程、RAG、参数调优（如降低 `temperature`）及插件/MCP，**不提供隐式内容标识**。

## 关键参数

- **鉴权参数**：`Authorization: Bearer <API-Key>` 必须携带，API-Key 需在[北京或新加坡控制台](https://bailian.console.aliyun.com/settings/api-key)创建；
- **请求参数**（以 Completion API 为例）：
  - 必填：`AppId`, `Prompt`, `RequestId`；
  - 可选：`User`, `Bot`, `doc_reference_type`（**仅旧版应用生效**；新版需在控制台开启“展示回答来源”开关）；
- **CLI 凭据管理**：Token Plan 需显式使用 `--config token-plan` Profile，普通 `default` Profile 不触发 Token 扣减 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
- **限流参数**：按 RPS/RPM 控制，触发后需等待对应窗口剩余时间（如 120 RPM 下单次请求失败后约等待 0.8 秒）。

## 使用方式

- **开通**：无需手动开通，满足实名认证 + 主账号或 `AliyunBailianFullAccess` 权限 RAM 账号即可自动启用；
- **接入路径**：
  - Web：通过[百炼控制台](https://bailian.console.aliyun.com/)直接体验或配置应用；
  - API：参考 [错误码文档](raw/model-api-reference/preparations/error-code.md) 和 [SDK 安装指南](raw/model-api-reference/preparations/install-sdk.md)；
  - CLI：执行 `bl auth login --console` 登录控制台凭据，`bl auth login --config token-plan --api-key <sk>` 启用 Token Plan；
- **售后触达**：
  - 技术问题：通过[官网售后服务入口](https://smartservice.console.aliyun.com/service/robot-chat)提交工单；
  - 业务合作：拨打 4008013260 或使用[售前咨询通道](https://smartservice.console.aliyun.com/service/pre-sales-chat)；
  - 法律协议：所有服务条款以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中公布的正式文本为准。

## 限制和注意事项

- **数据与安全**：
  - 百炼**不将用户数据用于模型训练**，传输全程 AES-256 加密；
  - 对话记录仅在登录状态下保存，控制台最多保留 **100 条历史记录**，无时间限制；
  - 数据隔离通过业务空间权限实现，不同子账号间数据物理隔离 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **计费与账户**：
  - 后付费按分钟出账、按月结算；账户余额必须 ≥ 0 元方可开通服务；
  - 万相会员权益**完全独立于百炼计费体系**，不可用于抵扣 API 调用费用；
  - 预付费支持节省计划与资源包，详情见 [节省计划与资源包文档](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **第三方工具支持边界**：
  > **注意**：阿里云百炼**仅对自身服务端行为负责**。对于 Cursor、Windsurf 等第三方工具的安装、配置、内部报错、Token 统计差异、本地网络/代理/防火墙问题，百炼仅提供方向性建议（如连通性测试、API 示例核查），不承担排查与解决责任 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **模型能力边界**：
  > **注意**：`doc_reference_type` 参数在新版本应用中已失效，其功能由控制台“展示回答来源”开关统一控制；若该开关关闭，该参数设置无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


