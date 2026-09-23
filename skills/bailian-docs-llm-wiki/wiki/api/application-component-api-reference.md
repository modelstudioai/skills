# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该接口面向开发者提供统一的 RESTful 接口规范，支持同步响应与[流式输出](../concepts/streaming-output.md)两种模式。所有请求需通过 RAM 授权并使用指定服务接入点发起。

## 支持的模型与功能

当前支持调用百炼平台托管的全部公开模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）及用户私有微调模型（需已部署为服务）。功能覆盖文本生成、多轮对话（含历史上下文维护）、[函数调用](../concepts/function-calling.md)（Function Calling）、结构化输出（JSON Schema 约束）及文件内容解析（PDF/DOCX/TXT 等）。详细能力列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为已开通权限的模型，如 `qwen-max`；私有模型需使用完整服务路径（如 `acs:baichuan:cn-hangzhou:123456789:service/qwen-finetuned-v1`） |
| `input.messages` | array | 是 | 对话消息数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`（字符串或 `file` 对象） |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；取值范围 `[0.0, 2.0]`，详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) |
| `parameters.stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时返回 SSE 格式数据 |

> **注意**：`input.messages` 中 `system` 角色仅支持首条消息，后续出现将被忽略——该行为与 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中“多轮 system 指令支持”的描述存在不一致，以实际 API 行为为准（2024 Q2 版本已确认移除多 system 支持）。

## 使用方式

1. 获取 RAM 凭据（AccessKey ID/Secret），确保已授予 `AliyunBaiChuanFullAccess` 或最小权限策略（参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）  
2. 构造 HTTPS POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（中国内地）或对应区域接入点  
3. 设置 Header：`Authorization: Bearer ${api_key}`（推荐）或 `X-DashScope-Access-Key: ${access_key_id}` + 签名  
4. 发送 JSON body，示例见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)

## 限制和注意事项

- 单次请求 `input.messages` 总长度上限为 32768 token（按模型 tokenizer 计算）；超限将返回 `400 Bad Request`  
- 流式响应（`stream=true`）下，`system` 消息不可用，且 `messages` 数组长度必须 ≥ 1（不允许空会话）  
- 私有模型调用需确保模型服务处于 `ACTIVE` 状态，状态查询请参考 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的健康检查章节  
- 所有请求受账户级 QPS 与并发数限制，具体配额请在控制台「API 调用配额」页查看

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


