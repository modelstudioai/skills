# Memory

使用阿里云百炼 CLI 写入和检索长期记忆、管理记忆节点与画像模板、读取用户画像，并导出技能记忆。

**说明**长期记忆相关能力目前仅对中国站（aliyun.com）账号开放。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl memory search --help`。删除类高危操作未显式追加 `--yes` 时会阻断执行（退出码 7）；如需预览请求，改用 `--dry-run`。

本页命令适用于阿里云百炼 CLI 2.5.0 及以上版本。2.5.0 对 Memory 命令有不兼容变更，从早期版本升级时请先查看[更新日志](raw/cli/changelog-group/changelog.md)。记忆库的概念、计费和 API 详见[记忆库](raw/application-user-guide/agent-context/memory-library-overview/overview.md)。

## 配置业务空间

Memory 命令通过业务空间专属域名调用记忆库 API，所有命令都必须提供业务空间 ID（Workspace ID），且 API Key 须属于同一业务空间。业务空间 ID 的获取方式见[认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

按以下任一方式提供业务空间 ID，优先级从高到低：

-   命令参数 `--workspace-id <id>`
-   环境变量 `BAILIAN_WORKSPACE_ID`
-   配置项 `workspace_id`，例如 `bl config set workspace_id <id>`

```
export DASHSCOPE_API_KEY='<your-api-key>'
export BAILIAN_WORKSPACE_ID='<your-workspace-id>'
```

记忆库 API 有阿里云账号级别的限流：add 120 QPM、search 300 QPM，全部接口合计 3000 QPM。收到 HTTP 429 时退避重试，两次调用之间至少间隔 1 秒。详见[限流说明](raw/application-user-guide/agent-context/memory-library-overview/integration-overview/limits.md)。

## 命令速查

能力

命令

说明

写入与检索

`bl memory add`

从对话消息抽取记忆，或直接保存自定义内容（异步抽取）

`bl memory search`

按查询文本或对话上下文检索记忆节点

记忆节点管理

`bl memory list`

分页列出用户的记忆节点

`bl memory node show`

查看单个记忆节点的完整详情

`bl memory update`

更新记忆节点内容

`bl memory delete`

删除单个记忆节点

画像模板与用户画像

`bl memory profile create`

创建画像模板

`bl memory profile list`

分页列出画像模板

`bl memory profile show`

查看画像模板定义及属性 ID

`bl memory profile update`

更新画像模板、抽取场景或策略版本

`bl memory profile delete`

删除画像模板

`bl memory profile get`

读取用户在某个模板下已抽取的画像

技能记忆

`bl memory skill export`

导出技能记忆节点

下文各命令的参数表不重复 `--workspace-id`、`--api-key` 及 `--output`、`--dry-run` 等全局参数。

## 写入与检索

### bl memory add

从对话消息或自定义内容添加记忆。命令提交异步抽取任务后在本地轮询，直到全部任务结束或等待预算耗尽。

**语法**

```
bl memory add --user-id <id> [--messages <json>] [--content <text>] [flags]
```

参数

类型

必填

说明

`--user-id <id>`

string

是

记忆实体 ID，标识记忆的归属对象

`--messages <json>`

string

否

消息 JSON 数组，例如 `[{"role":"user","content":"..."}]`。role 支持 user、assistant、tool，兼容 OpenAI tool\_calls，最多 50 条

`--content <text>`

string

否

原样保存的自定义内容。同时传入 `--messages` 时，服务端以 `--content` 为准

`--profile-schema <id>`

string

否

画像模板 ID。不传则不抽取用户画像

`--extract-mode <profile_only>`

string

否

仅抽取用户画像。需同时传入 `--profile-schema` 和 `--messages`，不能传入 `--content`

`--skill-name <name>`

string

否

技能名称，用于技能记忆。需与 `--skill-description`、`--skill-tags` 同时传入

`--skill-description <text>`

string

否

技能描述，用于技能记忆。需与 `--skill-name`、`--skill-tags` 同时传入

`--skill-tags <tag>`

array

否

技能标签，可重复传入。需与 `--skill-name`、`--skill-description` 同时传入

`--meta-data <json>`

string

否

自定义信息 JSON 对象，例如 `{"location_name":"北京"}`

`--wait <seconds>`

number

否

轮询等待预算（秒），默认 120。设为 0 时提交后立即返回 `event_id`

`--project-id <id>`

array

否

记忆片段规则 ID，可重复传入。消息抽取最多 5 个，自定义内容仅支持 1 个

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
# 保存一条明确的事实，并等待抽取完成
bl memory add --user-id user1 --content "用户喜欢骑行" --output json

# 从对话中抽取事实记忆
bl memory add --user-id user1 --messages '[{"role":"user","content":"我住在杭州，周末喜欢骑行。"}]'

# 只提交任务，不等待抽取完成
bl memory add --user-id user1 --content "用户喜欢摄影" --wait 0
```

-   `--content` 和 `--messages` 至少传入一项，建议只传其中一种。
-   一次调用可能同时新增、更新或删除多条记忆节点。等待预算耗尽时命令按超时退出，抽取可能仍在后台继续；先用 `bl memory list`、`bl memory search` 或 `bl memory profile get` 核对结果，再决定是否重新提交。
-   `--wait 0` 只返回提交回执和 `event_id`，不代表抽取已完成。`event_id` 不是记忆节点 ID，节点 ID 以 list 或 search 结果中的 `memory_node_id` 为准。
-   部分抽取任务失败时，命令返回非零退出码，输出中仍可能包含已完成部分的结果。
-   写入用户画像和技能记忆的用法分别见[画像模板与用户画像](#profile)和[技能记忆](#skill-memory)。

### bl memory search

通过查询文本或对话上下文检索记忆节点。

**语法**

```
bl memory search --user-id <id> [--query <text>] [flags]
```

参数

类型

必填

说明

`--user-id <id>`

string

是

记忆实体 ID，标识记忆的归属对象

`--query <text>`

string

否

检索文本，作为单条 user 消息发送

`--messages <json>`

string

否

用于上下文检索的消息 JSON 数组，优先于 `--query`

`--top-k <n>`

number

否

最大召回数量，取值范围 1～100，默认 10

`--min-score <score>`

number

否

最小相似度分数阈值，取值范围 0～1，默认 0.3，仅在 pro 策略下生效

`--memory-types <observation|skill>`

array

否

检索的记忆类型，可重复传入。不传时服务端只检索 observation

`--memory-type <observation|skill>`

string

否

已弃用，`--memory-types` 的别名，不能与 `--memory-types` 同时使用

`--project-ids <id>`

array

否

记忆片段规则 ID，可重复传入

`--project-id <id>`

array

否

已弃用，`--project-ids` 的别名，不能与 `--project-ids` 同时使用

`--plan-version <pro|lite>`

string

否

策略版本：pro 开启 Rerank，lite 关闭 Rerank，两者计费不同。不传时服务端默认 pro

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
# pro 策略，按分数阈值过滤
bl memory search --user-id user1 --query "用户喜欢什么运动？" --plan-version pro --min-score 0.5

# lite 策略不按 --min-score 过滤，只限制召回数量
bl memory search --user-id user1 --query "周末活动" --plan-version lite --top-k 5

# 按对话上下文同时检索事实记忆和技能记忆
bl memory search --user-id user1 --messages '[{"role":"user","content":"帮我整理会议记录"}]' --memory-types observation --memory-types skill
```

-   `--query` 和 `--messages` 至少传入一项；同时传入时以 `--messages` 为准。
-   不同策略版本的检索方式和计费不同，不要跨策略比较分数。策略差异见[Pro 与 Lite 策略版本说明](raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
-   空结果不是错误。检索不到刚写入的记忆时，先确认异步抽取已完成，再核对 `--user-id`、`--library-id`、规则 ID 和记忆类型是否与写入时一致。

## 记忆节点管理

节点 ID 取自 list 或 search 结果中的 `memory_node_id`。

### bl memory list

分页列出用户的记忆节点。

**语法**

```
bl memory list --user-id <id> [flags]
```

参数

类型

必填

说明

`--user-id <id>`

string

是

记忆实体 ID，标识记忆的归属对象

`--page-size <n>`

number

否

每页结果数，默认 10

`--page <n>`

number

否

页码，默认 1

`--project-id <id>`

string

否

记忆片段规则 ID，默认使用记忆库的默认规则

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
bl memory list --user-id user1 --page-size 20 --page 2
bl memory list --user-id user1 --project-id <project-id> --output json
```

-   不传 `--project-id` 时只列出默认规则下的节点；其他事实记忆规则和技能记忆规则需指定对应的规则 ID。
-   每次只返回一页，需要更多结果时调整 `--page`。

### bl memory node show

查看单个记忆节点的完整详情，包括类型、状态、内容和元数据。

**语法**

```
bl memory node show --node-id <id> [flags]
```

参数

类型

必填

说明

`--node-id <id>`

string

是

记忆节点 ID

**示例**

```
bl memory node show --node-id <node-id> --output json
```

-   更新节点前，可先用此命令确认节点是否为技能记忆。
-   已删除的节点仍可能返回 `status` 为 `delete` 的详情。

### bl memory update

更新记忆节点内容。

**语法**

```
bl memory update --node-id <id> --content <text> [flags]
```

参数

类型

必填

说明

`--node-id <id>`

string

是

记忆节点 ID

`--content <text>`

string

是

记忆节点的新内容，最多 512 个字符

`--meta-data <json>`

string

否

自定义信息 JSON 对象，增量合并，例如 `{"key":"value"}`

`--skill-name <name>`

string

否

技能名称，用于技能记忆。需与 `--skill-description`、`--skill-tags` 同时传入

`--skill-description <text>`

string

否

技能描述，用于技能记忆。需与 `--skill-name`、`--skill-tags` 同时传入

`--skill-tags <tag>`

array

否

技能标签，可重复传入。需与 `--skill-name`、`--skill-description` 同时传入

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
bl memory update --node-id <node-id> --content "用户现在更喜欢游泳" --meta-data '{"source":"user_correction"}'
```

-   `--content` 整体替换节点内容，`--meta-data` 增量合并，节点原有时间戳保留不变。
-   目标节点为技能记忆时，即使只修改内容，也必须同时传入 `--skill-name`、`--skill-description` 和 `--skill-tags`。
-   此命令不更新已抽取的用户画像。

### bl memory delete

删除单个记忆节点。

**语法**

```
bl memory delete --node-id <id> [flags]
```

参数

类型

必填

说明

`--node-id <id>`

string

是

记忆节点 ID

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

`--yes`

switch

实际执行时必填

确认删除。使用 `--dry-run` 预览时不需要

**示例**

```
bl memory delete --node-id <node-id> --dry-run
# 确认节点 ID 后执行
bl memory delete --node-id <node-id> --yes
```

-   只删除指定节点，不删除已抽取的用户画像值或画像模板，也不会清空用户的全部记忆。
-   删除后，节点详情仍可能显示 `status` 为 `delete`。可结合 list 和 search 结果确认删除效果。

## 画像模板与用户画像

画像模板定义要抽取的属性，可被多个用户共享；用户画像是某个用户在某个模板下已抽取的属性值。完整流程见[使用用户画像](raw/application-user-guide/agent-context/memory-library-overview/create-memory/user-profile.md)。

### bl memory profile create

创建画像模板。

**语法**

```
bl memory profile create --name <name> --attributes <json> [flags]
```

参数

类型

必填

说明

`--name <name>`

string

是

模板名称

`--description <text>`

string

否

模板描述

`--attributes <json>`

string

是

属性 JSON 数组，例如 `[{"name":"age","description":"年龄","default_value":"18"}]`。每个属性必须包含 name，description 和 default\_value 可选

`--plan-version <pro|lite>`

string

否

策略版本：pro 开启 Rerank，lite 关闭 Rerank，两者计费不同

`--extract-scene <efficient|intelligent>`

string

否

抽取场景，创建时默认 efficient

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
bl memory profile create --name travel_profile --attributes '[{"name":"city","description":"常住城市"},{"name":"hobby","description":"兴趣爱好"}]' --output json
```

创建模板本身不会抽取用户画像。记录返回的 `profile_schema_id`，在 `bl memory add` 中通过 `--profile-schema` 传入后，才会按该模板抽取画像。后续写入和读取应使用同一个 `--library-id`。

### bl memory profile list

分页列出画像模板。

**语法**

```
bl memory profile list [flags]
```

参数

类型

必填

说明

`--page-size <n>`

number

否

每页结果数，默认 10

`--page <n>`

number

否

页码，默认 1

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
bl memory profile list --page-size 20 --page 2
```

此命令只返回模板定义，不返回用户的画像值。

### bl memory profile show

查看画像模板定义及属性 ID。

**语法**

```
bl memory profile show --schema-id <id> [flags]
```

参数

类型

必填

说明

`--schema-id <id>`

string

是

画像模板 ID

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
bl memory profile show --schema-id <schema-id> --output json
```

返回结果中的 `attribute_id` 用于 `bl memory profile update` 更新或删除属性。

### bl memory profile update

更新画像模板的名称、描述、属性、抽取场景或策略版本。

**语法**

```
bl memory profile update --schema-id <id> [flags]
```

参数

类型

必填

说明

`--schema-id <id>`

string

是

画像模板 ID

`--name <name>`

string

否

新的模板名称

`--description <text>`

string

否

新的模板描述

`--attributes-operations <json>`

string

否

属性操作 JSON 数组，例如 `[{"op":"add","name":"plan"}]`

`--plan-version <pro|lite>`

string

否

策略版本：pro 开启 Rerank，lite 关闭 Rerank，两者计费不同

`--extract-scene <efficient|intelligent>`

string

否

抽取场景

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
# 新增属性
bl memory profile update --schema-id <schema-id> --attributes-operations '[{"op":"add","name":"travel_style","description":"旅行偏好"}]'

# 删除属性前先预览请求
bl memory profile update --schema-id <schema-id> --attributes-operations '[{"op":"delete","attribute_id":"<attribute-id>"}]' --dry-run
```

-   除 `--schema-id` 外，至少传入一个更新字段：`--name`、`--description`、`--attributes-operations`、`--plan-version` 或 `--extract-scene`。
-   每个属性操作需指定 `op`：`add` 需提供 `name`，`update` 和 `delete` 需提供 `attribute_id`。属性 ID 通过 `bl memory profile show` 获取。
-   此命令修改的是共享模板，而不是某个用户的画像值。`delete` 操作会删除属性定义且没有 `--yes` 确认，执行前先用 `bl memory profile show` 核对模板并用 `--dry-run` 预览请求。

### bl memory profile delete

删除画像模板。

**语法**

```
bl memory profile delete --schema-id <id> [flags]
```

参数

类型

必填

说明

`--schema-id <id>`

string

是

画像模板 ID

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

`--yes`

switch

实际执行时必填

确认删除。使用 `--dry-run` 预览时不需要

**示例**

```
bl memory profile delete --schema-id <schema-id> --dry-run
# 确认影响范围后执行
bl memory profile delete --schema-id <schema-id> --yes
```

删除不可恢复：模板及其属性定义被永久移除，所有用户在该模板下已抽取的画像都将无法访问。

### bl memory profile get

读取用户在某个画像模板下已抽取的画像。

**语法**

```
bl memory profile get --schema-id <id> --user-id <id> [flags]
```

参数

类型

必填

说明

`--schema-id <id>`

string

是

画像模板 ID

`--user-id <id>`

string

是

记忆实体 ID，标识画像的归属对象

`--library-id <id>`

string

否

记忆库 ID，默认使用账号的默认记忆库

**示例**

```
# 仅抽取画像，再读取结果
bl memory add --user-id user1 --profile-schema <schema-id> --extract-mode profile_only --messages '[{"role":"user","content":"我常住杭州，喜欢骑行。"}]'
bl memory profile get --schema-id <schema-id> --user-id user1 --output json
```

-   只有通过 `bl memory add --profile-schema` 使用同一个模板 ID 写入过消息，才会抽取出属性值；否则所有属性返回空值。
-   用户画像值通过消息抽取更新，CLI 不提供直接编辑、删除单个属性值或清空单个用户画像的命令。

## 技能记忆

技能记忆是记忆库中的一种记忆类型，写入、检索和更新沿用 `add`、`search`、`update` 命令，并通过技能类型的记忆片段规则 ID 指定范围。CLI 不提供规则的创建和管理命令，需使用已有规则 ID。

```
# 写入技能记忆：传入技能规则 ID 和完整的技能名称、描述、标签
bl memory add --user-id user1 --content "整理会议记录：提取议题、决策、待办和负责人" --project-id <skill-project-id> --skill-name meeting-summary --skill-description "整理会议行动清单" --skill-tags office --skill-tags meeting

# 检索技能记忆：需显式指定记忆类型
bl memory search --user-id user1 --query "整理会议记录" --memory-types skill --project-ids <skill-project-id>
```

### bl memory skill export

导出技能记忆节点。

**语法**

```
bl memory skill export --node-id <id> [flags]
```

参数

类型

必填

说明

`--node-id <id>`

string

是

技能记忆节点 ID

**示例**

```
bl memory skill export --node-id <skill-node-id> --output text > meeting-summary.md
bl memory skill export --node-id <skill-node-id> --output json > meeting-summary.json
```

-   文本输出为不含 frontmatter 的技能正文；JSON 输出还包含 `skill_name`、`skill_description` 和 `skill_tags`。
-   命令不直接写文件，可通过重定向保存。导出不会将技能安装到任何 Agent。
