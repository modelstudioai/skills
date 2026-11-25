# support

阿里云百炼平台为开发者提供覆盖模型调用、应用构建、部署运维及计费管理的全链路技术支持。支持范围包括官方 API/SDK 使用、控制台操作、故障诊断与基础架构咨询，但不涵盖第三方工具运维、业务代码开发或本地环境问题。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及配套 SLA 为法律与服务基准。

## 支持的模型/功能

- **模型类型**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、开源模型及三方模型（需遵守对应[三方模型服务协议和使用条款清单](https://terms.alicdn.com/legal-agreement/terms/common_product_agreement/20260207131114217/20260207131114217.html)）；Qwen3-VL-Plus 已支持图片训练微调。
- **核心能力**：
  - Completion / Assistant API 调用（含 function call 基础支持，但**不支持单次调用中依次执行两个本地函数**）
  - RAG 应用构建与 `doc_reference_type` 参数控制（仅在旧版应用中生效，新版需通过控制台开关启用）
  - CLI 工具（`bl`）支持 Token Plan Profile 鉴权与模型调用
  - 业务空间权限隔离，实现多租户数据隔离
- **不支持能力**：
  - Assistant API 的 memory 配置（当前暂不支持）
  - 结构化数据库（如 MySQL、Hive）直连（RDS 对接已在开发中）
  - 训练后模型导出（当前不支持）
  - 隐式文本水印（不支持）

> **注意**：文档 2 中提及“qwen-plus-latest 属于 Qwen3 系列”，但未明确其与 Qwen3.5/Qwen3.7 的版本关系；而文档 2 第 17 条明确指出 *“qwen-plus-latest 是 qwen-plus 的最新版本，属于 Qwen3 系列，而非 Qwen3.5 或 Qwen3.7 系列”*，且 Qwen3.5、Qwen3.7 为并列独立系列。该表述已统一，以文档 2 第 17 条为准。

## 关键参数

| 参数名 | 说明 | 生效条件 | 参考 |
|--------|------|----------|------|
| `temperature` / `top_p` / `top_k` | 控制输出随机性与确定性；降低可抑制幻觉，但可能削弱创造性 | 所有 Completion/Assistant API 请求体中生效 | [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“模型幻觉问题”章节 |
| `max_tokens` | 限制响应最大 token 数；合理设置可防止模型在关键信息后捏造内容 | 全局生效 | 同上 |
| `doc_reference_type` | 控制答案来源展示格式（如 `inline` / `footnote`） | **仅在旧版应用中生效**；新版需在控制台开启“展示回答来源”开关 | [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“API/SDK相关”第 6 条 |
| `RequestId`, `AppId` | 必填请求标识字段；缺失或格式错误将返回错误码 `100004`（参数缺失） | 所有 `/v2/app/completions` 等标准接口 | 同上第 1 条 |

## 使用方式

- **开通服务**：无需手动开通。使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录 [百炼控制台](https://bailian.console.aliyun.com/)，完成实名认证后自动开通。
- **API 调用**：
  - Header 必须包含 `Authorization: Bearer <API-Key>` 和 `Content-Type: application/json`
  - 示例见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中 curl 调用片段
- **SDK 集成**：
  - Python/Java SDK 请参考 [安装SDK](../../model-api-reference/preparations/install-sdk.md)
  - 多模态 Realtime API 请参考 [Realtime API 概览](../../model-api-reference/realtime-api-directory/realtime-api-overview.md)
- **CLI 工具**：
  - Token Plan 需显式登录 `token-plan` Profile：`bl auth login --config token-plan --api-key <sk-sp-Key>`
  - 查看当前凭据：`bl auth status --output json`；切换 Profile：`bl config use --name <profile>`  
  - 注意：Token Plan Profile **仅支持模型调用类命令**，控制台类命令（如 `app list`）需额外完成 `bl auth login --console` | [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“CLI 相关”章节 |

## 限制和注意事项

- **服务可用性**：按分钟级出账、月度结算；后付费账户余额须 ≥ 0 元方可开通服务。
- **数据隐私与存储**：
  - 百炼**绝不会将您的数据用于模型训练**，传输全程 AES-256 加密；
  - 根据法律法规，调用数据会被存储，具体条款详见 [《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 中数据处理条款；
  - 控制台体验中心最多保留 **100 条历史对话记录**（未登录/报错对话不保存）。
- **售后支持边界**（依据 [售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)）：
  - ✅ 支持：API/SDK 故障诊断、控制台问题、账号/计费咨询、百炼服务端连通性测试；
  - ❌ 不支持：第三方工具（Cursor/Windsurf 等）部署配置、用户本地网络/代理/防火墙问题、业务代码编写、非百炼侧系统集成问题；
  - ⚠️ 方向性建议仅限：确认百炼 API 可用性、提供官方调用示例、协助核查调用明细与计费记录。
- **其他限制**：
  - 万相会员权益**不适用于百炼 API 调用**；
  - 百炼服务开通后**暂不支持关闭**，如需停用，应删除全部 API-Key；
  - 生成速度受服务负载与并发请求影响，非固定值；
  - 限流触发后重试等待时间取决于您的 RPS/RPM 配置（例如 120 RPM 下需等待约 0.8 秒）。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


