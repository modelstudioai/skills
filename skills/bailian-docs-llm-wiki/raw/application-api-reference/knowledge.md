# 知识检索与问答

知识检索与问答相关 API 概览，含知识检索与知识问答两个接口。

知识检索与问答接口属于 **DashScope 应用网关**体系，与OpenAPI（如 `CreateIndex`、`ListIndices`、`Retrieve` 等 RPC 接口）不同：通过 HTTP REST 调用，使用 API Key Bearer 鉴权，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，其中 `{workspaceId}` 为业务空间 ID。

## 接口列表

接口

描述

路径

[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)

跨多个知识库执行联合语义检索，返回按相关性排序的切片。

POST /api/v1/indices/knowledge/search

[知识问答](https://help.aliyun.com/zh/model-studio/knowledgechat)

基于知识库的智能问答，通过 SSE 流式输出，依次返回规划、工具调用、生成三个阶段。

POST /api/v2/apps/knowledge/chat

**鉴权**：所有请求须在请求头携带 `Authorization: Bearer <API-Key>`与使用业务空间ID拼接的Base URL。API Key 在控制台 [API Key 页面](https://rag.console.aliyun.com/settings/apikey)获取，业务空间在控制台[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)获取。

**限流**：默认用户维度 25 QPS。如遇限流，请稍后重试。
