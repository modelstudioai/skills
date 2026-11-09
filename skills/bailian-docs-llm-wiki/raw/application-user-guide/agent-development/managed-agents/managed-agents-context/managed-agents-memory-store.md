# 记忆库

记忆库是跨会话持久化的挂载资源，支持内置文件记忆和百炼记忆库。创建会话时挂载，智能体按挂载配置读取和写入记忆。

## 概念

记忆库是独立于会话管理的挂载资源，用于跨会话保留智能体的记忆。Managed Agents 支持两种提供方：

**项目**

**内置记忆**

**百炼记忆库**

`provider`

省略或 `default`

`agentstudio_memory`

使用方式

挂载文件，通过文件工具读写

通过百炼记忆服务存储和检索

数据范围

由内置 Memory Store 决定

由记忆库和实体 ID 共同决定

挂载路径

保留现有 `/mnt/memory/...` 路径

无文件路径

记忆能力

保留现有文件记忆、版本及 Dreaming 能力

事实记忆、技能记忆和用户画像

**说明**`provider=default` 表示内置记忆，不是百炼记忆服务的默认库。创建请求省略 `provider` 时使用内置记忆，与原有请求保持兼容。

## 配额与限制

-   单个内置记忆文件最大 **102400 UTF-8 bytes**。
-   一个会话最多挂载 **8 条**记忆。
-   同一会话的记忆挂载必须使用同一种提供方，不能同时挂载内置记忆和百炼记忆库。
-   一个内置记忆库可同时挂载到多个会话，记忆内容跨会话共享。
-   百炼记忆库允许挂载多个库，也允许同一库绑定不同实体 ID；同一库与实体 ID 的组合不能重复挂载。
-   内置记忆的单条挂载说明最长 **4096 字符**。
-   记忆挂载仅在创建会话时设置，创建后不可新增、卸载或修改；需要调整时创建新会话。

## 内置记忆

内置记忆用于保存智能体的长期工作笔记，是带路径的文件树：

**层次**

**说明**

记忆库（Memory Store）

逻辑容器，含名称与描述。一个工作空间可创建多个记忆库

记忆（Memory）

记忆库内的一个文件，由路径和 UTF-8 文本正文组成，例如 Markdown 笔记

版本（Version）

记忆每次创建、修改、删除时自动产生的历史版本，可查询、可回看

### 创建记忆库

在[记忆库](https://bailian.console.aliyun.com/managed-agent/memory-stores)页面点击**创建记忆**，填写名字和描述。名字 1～255 字符。

**说明**控制台提供记忆库的创建、编辑与归档。记忆文件的写入、版本查询与删除通过 API 完成，详见下文与 [Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api.md)。

通过 API 创建，返回 `memstore_` 前缀的 ID。完整参数与响应字段详见[创建 Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-create.md)。

bash

```
curl -X POST "$AGENTSTUDIO_URL/memory_stores" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "项目知识库",
    "description": "项目约定、决策记录与排查笔记"
  }'
```

### 写入与管理记忆

记忆文件通过 API 管理，路径以 `/` 开头，例如 `/notes/project.md`。

写入一条记忆，返回 `mem_` 前缀的 ID。完整参数与响应字段详见[创建 Memory API](raw/application-api-reference/managed-agents-api/memory-store-api/memory-create.md)。

bash

```
curl -X POST "$AGENTSTUDIO_URL/memory_stores/memstore_xxx/memories" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/notes/project.md",
    "content": "# 项目约定\n默认开发环境为预发环境。\n"
  }'
```

读取与修改：

-   **读取**：`GET /memory_stores/{memory_store_id}/memories/{memory_id}` 返回正文；归档但未删除的记忆库仍可读取。
-   **修改**：`POST /memory_stores/{memory_store_id}/memories/{memory_id}`，传入新 `content` 改正文，或传入新 `path` 重命名，也可同时传入原子修改。真实变更自动产生 `modified` 版本。
-   **并发保护**：修改时可在 `precondition` 中携带读取时的 `content_sha256`，内容被他人改过则返回冲突，重读后合并重试。
-   **列表**：`GET /memory_stores/{memory_store_id}/memories`，支持 `path_prefix` 前缀过滤、`depth`（0 递归 / 1 当前层）、`view`（basic 不含正文 / full 含正文）。按路径排序，不支持按正文关键词搜索。
-   **删除**：`DELETE /memory_stores/{memory_store_id}/memories/{memory_id}` 删除当前文件，历史版本保留，可通过版本接口查询。

写入操作要求记忆库未归档。完整参数与响应字段详见 [Memory API](raw/application-api-reference/managed-agents-api/memory-store-api/memory-create.md)。

### 挂载到会话

#### 控制台

在**新建会话**的**资源**区点击 **+**，选择**记忆**，再选择**内置记忆**，配置以下选项后点击**创建会话**：

**配置项**

**说明**

记忆

选择要挂载的内置记忆库

权限

只读（仅可检索）或读写（还可在会话结束后通过 Dreaming 把本次对话整理回库）

说明

会随挂载信息提供给智能体，帮助其判断何时检索该记忆

#### API

创建会话时在 `resources` 中指定内置记忆。`provider` 可省略，省略时为 `default`；`access` 省略时默认 `read_write`：

bash

```
curl -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": {"type": "agent", "id": "agent_xxx"},
    "resources": [
      {
        "type": "memory_store",
        "memory_store_id": "memstore_xxx",
        "access": "read_write",
        "instructions": "优先查询该库中的项目约定；新发现保存到相关笔记中。"
      }
    ]
  }'
```

内置记忆的响应 `resources` 中返回服务端生成的 `mount_path`，例如 `/mnt/memory/<名称>`。在系统提示词中可直接引用该路径。

### 智能体如何使用记忆

会话存在内置记忆挂载时，平台自动向智能体注入记忆使用说明，包含挂载路径、权限与填写的说明。智能体的使用方式：

-   通过 Glob、Grep 在挂载路径下查找，用 Read 读取相关文件，完成任务后用 Write、Edit 把值得保留的信息写回。
-   只读挂载仅支持查询与读取；读写挂载支持全部文件操作。
-   shell 命令不能访问记忆路径，只能使用上述文件工具。

**警告**记忆中不要保存密钥、Token 等凭证。挂载说明属于业务自定义内容，不能覆盖平台安全策略。

### 历史版本

内置记忆的创建、修改、删除自动产生版本记录，版本查询不要求当前记忆仍存在：

-   **列出版本**：`GET /memory_stores/{memory_store_id}/memory_versions`，可按 `memory_id` 过滤单条记忆，或按 `operation`（`created` / `modified` / `deleted`）与创建时间范围过滤，按创建时间倒序。
-   **查看版本**：`GET /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}` 返回该版本正文，用于回看旧内容，不回滚当前记忆。
-   **擦除正文**：`POST /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact` 将指定版本的正文擦除，不可逆且不影响当前记忆。

完整参数与响应字段详见 [Memory Version API](raw/application-api-reference/managed-agents-api/memory-store-api/memory-version-list.md)。

### 归档

在[记忆库](https://bailian.console.aliyun.com/managed-agent/memory-stores)页面点击**归档**，或调用 `POST /memory_stores/{memory_store_id}/archive`。归档不可逆：归档后不可写入，不能绑定新会话，已有会话的挂载变为只读。列表默认不返回已归档记忆库，传 `include_archived=true` 可同时返回。重复归档幂等。

## 百炼记忆库

百炼记忆库由百炼记忆服务提供事实记忆、技能记忆和用户画像。记忆库、记忆规则和画像模板在记忆服务中管理，Managed Agents 负责挂载和使用。

### 前提

已开通百炼记忆服务，并创建百炼记忆库。按需配置记忆规则和画像模板。创建会话时需要使用记忆库 ID；记忆规则和画像模板按需传入规则 ID 和画像模板 ID：

-   记忆库与规则：详见[百炼记忆库](raw/application-user-guide/agent-context/memory-library-overview/memory-library.md)和[配置记忆规则](raw/application-user-guide/agent-context/memory-library-overview/create-memory/configure-rules.md)。
-   画像模板：详见[创建画像模板](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。

**说明**未开通记忆服务时，调用记忆服务 API（例如 `AddMemoryAsync`）返回 403 `ServiceNotOpened`，控制台也不会展示百炼记忆库挂载选项。

### 挂载到会话

#### 控制台

在**新建会话**的**资源**区点击 **+**，选择**记忆**，再选择**百炼记忆库**（该选项是否展示取决于记忆服务开通状态），配置以下选项后点击**创建会话**：

**配置项**

**说明**

记忆库

选择要挂载的百炼记忆库

实体 ID

该条挂载绑定的实体 ID，不同挂载可以使用不同值

权限

只读（仅可检索）或读写（可检索和写入）

描述

挂载用途说明，帮助模型判断何时检索该记忆库

记忆规则

选择事实记忆和技能记忆的规则，每条挂载合计最多 5 个

画像模板

选择一个画像模板；不选时不启用画像能力

#### API

创建会话时在 `resources` 中指定 `type` 为 `memory_store`、`provider` 为 `agentstudio_memory`。示例 ID 需替换为实际资源：

```
{
  "agent": {
    "type": "agent",
    "id": "agent_xxx"
  },
  "environment_id": "env_xxx",
  "resources": [
    {
      "type": "memory_store",
      "provider": "agentstudio_memory",
      "memory_store_id": "0123456789abcdef0123456789abcdef",
      "entity_id": "customer_001",
      "access": "read_write",
      "description": "保存客户确认的业务约定、可复用经验和沟通偏好",
      "project_ids": ["fact_rule_demo", "skill_rule_demo"],
      "profile_schema": "profile_schema_demo"
    }
  ]
}
```

字段说明：

**字段**

**必填**

**类型**

**说明**

`type`

是

string

固定为 `memory_store`

`provider`

否

string

`agentstudio_memory` 表示百炼记忆库。省略时为 `default`（内置记忆）；创建请求不接受显式 `null`、空串或其他值

`memory_store_id`

是

string

百炼记忆库 ID，不要求 `memstore_` 前缀

`entity_id`

是

string

该条挂载绑定的实体 ID，去除首尾空白后不能为空。它不是云账号 UID，也不是 Session 顶层字段；不同挂载可以使用不同实体 ID

`access`

否

string

`read_only`（只读）或 `read_write`（读写），默认 `read_write`

`description`

否

string

挂载用途描述，由调用方填写并保存，帮助模型选库；不会被记忆库元数据中的描述覆盖

`project_ids`

否

string\[\]

事实记忆和技能记忆的规则 ID，合并在一个数组中，每条挂载合计最多 5 个，数组中的规则 ID 不能为空或重复

`profile_schema`

否

string

画像模板 ID，必须为非空字符串。只支持一个，不接受数组或模板对象，也不计入上述 5 条规则

规则与画像模板的默认行为：

-   `project_ids` 省略或为空数组时，使用百炼默认记忆规则；空数组不表示关闭抽取。
-   `profile_schema` 省略时不启用该挂载的画像能力，不自动补入默认模板。

### 智能体如何使用百炼记忆

挂载后，平台向智能体提供该记忆库的检索和写入能力。智能体按需检索事实记忆、技能记忆和用户画像；只读挂载仅支持检索，读写挂载支持检索与写入。记忆的抽取规则和画像模板在记忆服务中管理。

## 常见错误

**HTTP**

**error.code**

**原因**

400

`invalid_request_error`

参数、路径、limit、分页游标非法

401

`InvalidApiKey`

API Key 缺失、错误或失效

403

`permission_error`

身份或资源访问权限不足

404

`not_found_error`

记忆库、记忆或版本不存在或不属于当前工作空间

409

`memory_path_conflict_error`

文件重名或路径与已有文件/目录冲突

409

`memory_precondition_failed_error`

并发修改导致条件更新冲突

409

`memory_store_archived_error`

对已归档记忆库发起写入

429

`rate_limit_error`

请求限流

## 下一步

-   [委派任务给 Agent](raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)：创建会话时挂载记忆库。
-   [Agent 上下文管理](raw/application-user-guide/agent-development/managed-agents/managed-agents-context.md)：了解全部挂载资源类型。
-   [Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api.md)：内置记忆库、记忆与版本的完整接口。
-   [百炼记忆库](raw/application-user-guide/agent-context/memory-library-overview/memory-library.md)：管理百炼记忆库、记忆规则与画像模板。
