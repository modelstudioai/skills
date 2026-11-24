# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置与生命周期管理等核心环节。它面向开发者提供统一的 API 接口和 SDK 封装，用于构建生产级 AI 应用。该能力依赖平台底层模型服务与资源调度系统，需配合具体模型实例使用。

## 支持的模型/功能

- 支持调用百炼平台托管的全部大语言模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型（需通过 [应用接入协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 授权）；
- 提供 Prompt 工程支持（含变量注入、模板版本管理）、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、多轮会话上下文维护；
- 支持异步任务提交（如长文本摘要、批量推理），结果通过回调或轮询获取；  
- 所有功能均以 `application` 为作用域进行权限隔离与配额控制，详情见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，须在控制台「模型管理」中启用后方可使用；不支持直接传入模型名称（如 `"qwen-max"`），必须使用平台分配的 ID |
| `input` | object | 是 | 输入结构体，包含 `messages`（标准 ChatML 格式）或 `prompt`（单 prompt 字符串），详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的格式示例 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 Server-Sent Events 流，注意客户端需处理 chunk 解析 |
| `max_tokens` | integer | 否 | 最大生成 token 数，硬上限受模型自身限制（如 Qwen2-72B 最高支持 8192） |

## 使用方式

1. 在百炼控制台创建应用，获取 `app_id` 和 `app_secret`；
2. 使用 SDK（推荐 Python/Java）或直接调用 HTTPS endpoint：`POST https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat/completions`；
3. 请求头携带 `Authorization: Bearer {app_secret}`，Body 按上述参数格式组织 JSON；
4. 错误响应遵循 RFC 7807 标准，`error.code` 包含 `InvalidParameter`、`QuotaExceeded` 等可编程识别码。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system/user/assistant 角色标记）不得超过模型 context 长度的 95%，否则触发 `ContextLengthExceeded` 错误；
- 异步任务最长保留结果 7 天，超期自动清理，不可恢复；
- > **注意**：原始文档中 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 提到“支持传入 `model_name` 字段”，但该字段已于 v2.3.0 版本废弃，实际仅接受 `model_id`，请以控制台模型列表页显示的 ID 为准；
- > **注意**：[售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中标注的“免费调用量包含 10 万 tokens/月”，该额度自 2024 年 6 月起已调整为按应用维度独立计算，不再与账号级额度合并；
- 调用失败时优先检查 `app_secret` 是否过期（默认 12 个月有效期），而非重试网络请求。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


