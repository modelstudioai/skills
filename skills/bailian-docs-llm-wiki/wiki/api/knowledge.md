# knowledge

百炼平台「知识检索与问答」相关的 HTTP REST API 概览，提供跨知识库语义检索与基于知识库的智能问答两个接口。这两个接口属于 DashScope 应用网关体系，通过 [API Key](../concepts/api-key.md) Bearer 鉴权调用，与 `CreateIndex`、`Retrieve` 等 OpenAPI RPC 接口不同。详见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 接口列表

| 接口 | 描述 | 路径 |
| --- | --- | --- |
| 知识检索 | 跨多个知识库执行联合语义检索，返回按相关性排序的切片 | `POST /api/v1/indices/knowledge/search` |
| 知识问答 | 基于知识库的智能问答，通过 SSE [流式输出](../concepts/streaming-output.md)，依次返回规划、工具调用、生成三个阶段 | `POST /api/v2/apps/knowledge/chat` |

## 鉴权与 Base URL

所有请求须在请求头携带 `Authorization: Bearer <API-Key>`，并使用[业务空间](../concepts/workspace.md) ID 拼接的 Base URL：

```
https://{workspaceId}.cn-beijing.maas.aliyuncs.com
```

其中 `{workspaceId}` 为[业务空间](../concepts/workspace.md) ID。[API Key](../concepts/api-key.md) 在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey) 获取，[业务空间](../concepts/workspace.md) ID 在控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取。

## 限流

默认用户维度 25 QPS。如遇限流，请稍后重试。更多信息参见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 与 OpenAPI 的区别

知识检索与问答接口属于 **DashScope 应用网关** 体系，与 OpenAPI（如 `CreateIndex`、`ListIndices`、`Retrieve` 等 RPC 接口）不同：

- 调用方式：HTTP REST，而非 RPC 风格
- 鉴权方式：[API Key](../concepts/api-key.md) Bearer
- Base URL：使用[业务空间](../concepts/workspace.md) ID 拼接的专属域名

## 使用建议

- 知识检索接口适合需要自定义生成流程的场景：拿到排序后的切片后，自行拼接 [prompt](../guides/prompt.md) 调用大模型。
- 知识问答接口适合开箱即用的问答场景：服务端自动完成规划、检索、生成，通过 SSE 流式返回三个阶段的结果。
- 调用前确认 API Key 与[业务空间](../concepts/workspace.md) ID 已正确配置，详见 [知识检索与问答](../../raw/application-api-reference/knowledge.md)。

## 来源文档

- [知识检索与问答](../../raw/application-api-reference/knowledge.md)











