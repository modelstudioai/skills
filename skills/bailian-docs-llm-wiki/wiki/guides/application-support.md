# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、参数配置、请求调度与错误处理等核心环节。它面向通过 API 或 SDK 集成百炼应用的开发者，提供统一的运行时支撑。该能力不直接暴露底层模型实例，而是以应用（Application）为单位进行封装和管控。

## 支持的模型/功能

- 支持所有已发布至百炼控制台「应用」模块的托管应用（即通过 `Create Application` 创建并部署成功的应用），包括基于 Qwen 系列、Qwen-VL、Qwen-Audio 等模型构建的[多模态](../concepts/multi-modal.md)或文本应用；
- 支持同步推理（`/v1/applications/{app_id}/chat`）、流式响应（`stream=true`）及历史会话上下文管理（需显式传入 `conversation_id`）；
- 不支持直接调用未绑定至应用的裸模型（如 `qwen-max` 模型 ID），此类调用应使用 [模型 API](../../raw/model-api.md) 而非本服务。  
> **注意**：原始文档中未明确列出支持的模型列表，但根据 [服务支持](../../raw/application-user-guide/application-support.md) 的上下文结构，其实际能力依赖于控制台中「应用」模块的可用模型范围，而非独立模型目录。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用详情」页获取；对应 [服务支持](../../raw/application-user-guide/application-support.md) 中定义的应用实体ID |
| `messages` | array | 是 | 对话消息数组，格式同 OpenAI；首条 `user` 消息为必填输入 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流，详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `temperature` | number | 否 | 控制生成随机性（0.0–2.0），仅当应用配置允许覆盖时生效 |

## 使用方式

1. 在百炼控制台创建并发布应用，确保状态为「已上线」；
2. 获取 `app_id`（非模型 ID）及鉴权 `API-Key`；
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat`，Body 为 JSON 格式，示例：
   ```json
   {
     "messages": [{"role": "user", "content": "你好"}],
     "stream": true
   }
   ```
4. 错误响应遵循标准 HTTP 状态码（如 `401 Unauthorized`、`404 App Not Found`），详细错误码见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- 单次请求 `messages` 总长度（字符数）上限为 32768，超长将返回 `400 Bad Request`；
- 流式响应下，`conversation_id` 必须在首次请求中生成并复用于后续轮次，否则上下文不延续；
- 应用若启用了「敏感词过滤」或「自定义后处理」，其行为由应用配置决定，不在 API 层透出控制开关；  
> **注意**：[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 明确要求应用输出内容须符合中国法律法规，但该约束未在接口文档中体现具体技术拦截逻辑，开发者需自行校验业务合规性。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


