# Memory Store

记忆库是跨会话持久化的挂载资源，内部为带路径的文件树。创建会话时挂载，智能体通过文件工具读写，内容跨会话保留。

## 记忆模型

记忆库采用三层模型：

-   **记忆库（Memory Store）**：逻辑容器，含名称与描述。一个工作空间可创建多个记忆库。
-   **记忆（Memory）**：记忆库内的一个文件，由路径和 UTF-8 文本正文组成，例如 Markdown 笔记。每次创建、修改、删除自动产生历史版本。
-   **版本（Version）**：记忆的历史快照，可查询、可回看，支持擦除指定版本正文。

记忆库通过会话挂载使用：创建会话时在 `resources` 中指定，权限为只读（仅可检索）或读写（可写回记忆库）。挂载路径由服务端按记忆库名称生成，形如 `/mnt/memory/<名称>`。记忆库仅在创建会话时挂载，创建后不可新增、卸载或修改；需要调整时创建新会话。

## 记忆库操作

**操作**

**端点**

**说明**

[创建 Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-create.md)

`POST /memory_stores`

创建记忆库，返回 `memstore_` 前缀 ID

[列出 Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-list.md)

`GET /memory_stores`

按创建时间倒序分页列出，默认不含已归档

[获取 Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-get.md)

`GET /memory_stores/{memory_store_id}`

获取记忆库元数据

[更新 Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-update.md)

`POST /memory_stores/{memory_store_id}`

更新名称、描述与元数据

[归档 Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api/memory-store-archive.md)

`POST /memory_stores/{memory_store_id}/archive`

归档不可逆；归档后不可写入、不能绑定新会话，已有会话的挂载变为只读

## 记忆操作

写入操作要求记忆库未归档。

**操作**

**端点**

**说明**

[创建 Memory](raw/application-api-reference/managed-agents-api/memory-store-api/memory-create.md)

`POST /memory_stores/{memory_store_id}/memories`

新建记忆文件，返回 `mem_` 前缀 ID

[列出 Memory](raw/application-api-reference/managed-agents-api/memory-store-api/memory-list.md)

`GET /memory_stores/{memory_store_id}/memories`

按路径排序，支持路径前缀过滤；不支持按正文关键词搜索

[获取 Memory](raw/application-api-reference/managed-agents-api/memory-store-api/memory-get.md)

`GET /memory_stores/{memory_store_id}/memories/{memory_id}`

读取记忆正文；记忆库归档但未删除时可读取

[更新 Memory](raw/application-api-reference/managed-agents-api/memory-store-api/memory-update.md)

`POST /memory_stores/{memory_store_id}/memories/{memory_id}`

修改正文、重命名或同时原子修改；支持 `precondition` 乐观锁

[删除 Memory](raw/application-api-reference/managed-agents-api/memory-store-api/memory-delete.md)

`DELETE /memory_stores/{memory_store_id}/memories/{memory_id}`

删除当前文件，历史版本保留

## 版本操作

版本查询不要求当前记忆仍存在。

**操作**

**端点**

**说明**

[列出 Memory Version](raw/application-api-reference/managed-agents-api/memory-store-api/memory-version-list.md)

`GET /memory_stores/{memory_store_id}/memory_versions`

按创建时间倒序，支持按记忆、操作类型与时间范围过滤

[获取 Memory Version](raw/application-api-reference/managed-agents-api/memory-store-api/memory-version-get.md)

`GET /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}`

读取指定历史版本，用于回看旧内容，不回滚当前记忆

[擦除 Memory Version](raw/application-api-reference/managed-agents-api/memory-store-api/memory-version-redact.md)

`POST /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact`

擦除指定版本正文，不可逆且不影响当前记忆
