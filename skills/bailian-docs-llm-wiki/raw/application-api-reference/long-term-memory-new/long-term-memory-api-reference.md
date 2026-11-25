# 长期记忆API 参考

长期记忆的完整 API 接口目录：公共请求信息、全部接口一览与使用限制，各接口的请求参数、返回结果和示例代码见对应分页。

本文档是长期记忆（记忆库）全部 API 的目录总览。功能介绍和使用指南参见[记忆库](../../application-user-guide/agent-context/memory-library-overview/memory-library.md)与[长期记忆 API](../../application-user-guide/agent-context/memory-library-overview/long-term-memory-2-0.md)。

<a id="公共请求信息"></a>

## 公共请求信息

| 参数 | 说明 |
| --- | --- |
| Base URL | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`。调用时请将 `{WorkspaceId}` 替换为真实的[业务空间 ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain) |
| 认证方式 | 在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`。API Key 的获取方式请参见[获取 API Key](../../model-api-reference/preparations/get-api-key.md) |
| Content-Type | `application/json` |

协议约定、通用请求/响应格式与分页说明参见 [API 概览](api-overview.md)，鉴权细节参见[鉴权](api-overview/authentication.md)，错误响应参见[错误码](api-overview/errors.md)。

<a id="接口概览"></a>

## 接口概览

> **重要**
>
> 记忆库将于 **2026 年 8 月 20 日 10:00**（北京时间）正式商业化计费。Add 和 Search 调用均区分 **Pro** 和 **Lite** 版本：Add 的版本对应不同质量的记忆抽取模型，Search 的版本决定是否开启 Rerank。详见[计费说明](../../application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。

**记忆管理**：

记忆节点的类型（`memory_type`）为事实记忆 `observation` 或技能记忆 `skill`，写入时抽取哪一类由 `project_id` 对应的记忆规则决定；传入 `profile_schema` 时额外抽取用户画像，画像通过下方的用户画像接口读取。

| 接口名称 | HTTP 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| [AddMemory](fragments-overview/add-memory.md) | POST | `/add` | 同步添加记忆，在响应中直接返回抽取结果 |
| [AddMemoryAsync](fragments-overview/add-memory-async.md) | POST | `/add-async` | 异步提交记忆抽取任务 |
| [GetEvent](fragments-overview/get-event.md) | GET | `/events/{event_id}` | 查询异步任务事件详情 |
| [ListMemory](fragments-overview/list-memory.md) | GET | `/memory_nodes` | 分页列出记忆节点 |
| [SearchMemory](fragments-overview/search-memory.md) | POST | `/memory_nodes/search` | 相似度检索记忆节点，默认仅检索事实记忆 |
| [GetMemoryNode](fragments-overview/get-memory-node.md) | GET | `/memory_nodes/{memory_node_id}` | 获取单个记忆节点详情 |
| [GetSkillExport](fragments-overview/get-skill-export.md) | GET | `/skill/export/{memory_node_id}` | 导出技能记忆节点 |
| [UpdateMemory](fragments-overview/update-memory.md) | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆节点内容 |
| [DeleteMemory](fragments-overview/delete-memory.md) | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆节点 |

**用户画像**：

| 接口名称 | HTTP 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| [CreateProfileSchema](profiles-overview/create-schema.md) | POST | `/profile_schemas` | 创建画像模板 |
| [ListProfileSchemas](profiles-overview/list-schemas.md) | GET | `/profile_schemas` | 获取画像模板列表 |
| [GetProfileSchema](profiles-overview/get-schema.md) | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| [UpdateProfileSchema](profiles-overview/update-schema.md) | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| [GetUserProfile](profiles-overview/get-user-profile.md) | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

<a id="使用限制"></a>

## 使用限制

限流（阿里云账号级别）：

| API 接口 | 限流 |
| --- | --- |
| 全部接口 | 总计不超过 3000 QPM |
| add 接口 | 120 QPM |
| search 接口 | 300 QPM |

生成的记忆片段与用户画像暂无失效日期。如需扩容限流额度，请[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请，详见[限流说明](../../application-user-guide/agent-context/memory-library-overview/integration-overview/limits.md)。
