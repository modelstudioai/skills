# 长期记忆API 参考

长期记忆的完整 API 接口目录：公共请求信息、全部接口一览与使用限制，各接口的请求参数、返回结果和示例代码见对应分页。

本文档是长期记忆（记忆库）全部 API 的目录总览。功能介绍和使用指南参见[记忆库](raw/application-user-guide/memory-library-overview/memory-library.md)与[长期记忆 API](raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 公共请求信息

参数

说明

Base URL

`https://dashscope.aliyuncs.com/api/v2/apps/memory/`

认证方式

在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`。API Key 的获取方式请参见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)

Content-Type

`application/json`

协议约定、通用请求/响应格式与分页说明参见 [API 概览](raw/application-api-reference/long-term-memory-new/api-overview.md)，鉴权细节参见[鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)，错误响应参见[错误码](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

## 接口概览

**重要**记忆库将于 **2026 年 8 月 20 日 10:00**（北京时间）正式商业化计费。Add 和 Search 调用均区分 **Pro** 和 **Lite** 版本：Add 的版本对应不同质量的记忆抽取模型，Search 的版本决定是否开启 Rerank。详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

**事实记忆**：

接口名称

HTTP 方法

路径

说明

[AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)

POST

`/add`

添加事实记忆

[AddMemoryAsync](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)

POST

`/add-async`

异步提交记忆抽取任务

[GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)

GET

`/events/{event_id}`

查询异步任务事件详情

[ListMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)

GET

`/memory_nodes`

列出事实记忆

[SearchMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)

POST

`/memory_nodes/search`

搜索事实记忆

[GetMemoryNode](raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)

GET

`/memory_nodes/{memory_node_id}`

获取单个记忆节点详情

[GetSkillExport](raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)

GET

`/skill/export/{memory_node_id}`

导出技能记忆节点

[UpdateMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)

PATCH

`/memory_nodes/{memory_node_id}`

更新事实记忆

[DeleteMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)

DELETE

`/memory_nodes/{memory_node_id}`

删除事实记忆

**用户画像**：

接口名称

HTTP 方法

路径

说明

[CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)

POST

`/profile_schemas`

创建画像模板

[ListProfileSchemas](raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)

GET

`/profile_schemas`

获取画像模板列表

[GetProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)

GET

`/profile_schemas/{profile_schema_id}`

获取画像模板详情

[UpdateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)

PATCH

`/profile_schemas/{profile_schema_id}`

更新画像模板

[GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)

GET

`/profile_schemas/{profile_schema_id}/user_profile`

获取用户画像

## 使用限制

限流（阿里云账号级别）：

API 接口

限流

全部接口

总计不超过 3000 QPM

事实记忆 add 接口

120 QPM

事实记忆 search 接口

300 QPM

生成的记忆片段与用户画像暂无失效日期。如需扩容限流额度，请[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请，详见[限流说明](raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。
