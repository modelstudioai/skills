# Sandbox

阿里云百炼 CLI 管理沙箱实例与模版生命周期的命令速查。

在终端管理阿里云百炼沙箱实例与模版：创建、查询、连接、暂停、恢复、释放实例，以及创建、更新、查询、删除模版和查看构建状态。

**说明**Sandbox 相关能力目前仅对中国站（aliyun.com）账号开放，要求 cn-beijing 地域并完成 Sandbox SLR 授权。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl sandbox create --help`。连接凭据默认脱敏，需要时使用 `--show-credentials` 获取。本文命令明细以 bl 2.2.1 为基准核实。

## 实例管理

### bl sandbox list

列出 Sandbox 实例。需要 API Key 鉴权。

**语法**

```
bl sandbox list [--template-id <id>] [--sandbox-id <id>] [--state <state>] [--limit <n>]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--template-id <id>`

string

否

按模版 ID 筛选

`--sandbox-id <id>`

string

否

按 Sandbox ID 筛选

`--state <state>`

string

否

按状态筛选，例如 running 或 paused

`--limit <n>`

number

否

最大返回数量（1–50）

**示例**：筛选并列出最多 20 个运行中的 Sandbox 实例

```
bl sandbox list --state running --limit 20
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox get

获取 Sandbox 实例详情。需要 API Key 鉴权。

**语法**

```
bl sandbox get --sandbox-id <id> [--show-credentials]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--sandbox-id <id>`

string

是

Sandbox 实例 ID

`--show-credentials`

switch

否

输出 envd 与流量访问 Token 原值，不进行脱敏

**示例**：获取指定 Sandbox 实例的详细信息

```
bl sandbox get --sandbox-id sbx-xxx
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox create

创建 Sandbox 实例。需要 API Key 鉴权。

**语法**

```
bl sandbox create (--template-id <id> | --body <json|@path>) [flags]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--body <json|@path>`

string

否

JSON 请求体，可内联或从 @文件路径读取；显式 Flag 优先

`--template-id <id>`

string

否

已就绪的模版 ID；也可通过 --body 中的 templateID 提供

`--instance-timeout <seconds>`

number

否

本次操作后的 Sandbox 存活时间（300–604800 秒）

`--allow-internet-access <bool>`

boolean

否

允许访问公网

`--metadata <key=value>`

array

否

实例 Metadata 键值；可重复传入

`--env <key=value>`

array

否

实例环境变量；可重复传入

`--auto-pause <bool>`

boolean

否

实例超时后自动暂停

`--auto-resume <bool>`

boolean

否

连接已暂停实例时自动恢复

`--allow-out <address>`

array

否

出站白名单条目；可重复传入

`--deny-out <address>`

array

否

出站黑名单条目；可重复传入

`--mask-request-host <host>`

string

否

覆盖出站请求的 Host Header

`--show-credentials`

switch

否

输出 envd 与流量访问 Token 原值，不进行脱敏

**示例**：使用模板创建 Sandbox 实例并设置超时时间

```
bl sandbox create --template-id tpl-xxx --instance-timeout 3600
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox connect

连接 Sandbox 实例并返回连接信息。需要 API Key 鉴权。

**语法**

```
bl sandbox connect --sandbox-id <id> [--instance-timeout <seconds>] [--show-credentials]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--sandbox-id <id>`

string

是

Sandbox 实例 ID

`--body <json|@path>`

string

否

JSON 请求体，可内联或从 @文件路径读取；显式 Flag 优先

`--instance-timeout <seconds>`

number

否

本次操作后的 Sandbox 存活时间（300–604800 秒）

`--show-credentials`

switch

否

输出 envd 与流量访问 Token 原值，不进行脱敏

**示例**：连接 Sandbox 实例并设置超时时间

```
bl sandbox connect --sandbox-id sbx-xxx --instance-timeout 3600
```

### bl sandbox pause

暂停 Sandbox 实例。需要 API Key 鉴权。

**语法**

```
bl sandbox pause --sandbox-id <id>
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--sandbox-id <id>`

string

是

Sandbox 实例 ID

**示例**：暂停指定的 Sandbox 实例

```
bl sandbox pause --sandbox-id sbx-xxx
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox resume

恢复 Sandbox 实例并返回连接信息。需要 API Key 鉴权。

**语法**

```
bl sandbox resume --sandbox-id <id> [--instance-timeout <seconds>] [--show-credentials]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--sandbox-id <id>`

string

是

Sandbox 实例 ID

`--body <json|@path>`

string

否

JSON 请求体，可内联或从 @文件路径读取；显式 Flag 优先

`--instance-timeout <seconds>`

number

否

本次操作后的 Sandbox 存活时间（300–604800 秒）

`--show-credentials`

switch

否

输出 envd 与流量访问 Token 原值，不进行脱敏

**示例**：恢复指定 Sandbox 实例并设置超时时间

```
bl sandbox resume --sandbox-id sbx-xxx --instance-timeout 3600
```

### bl sandbox delete

释放 Sandbox 实例。需要 API Key 鉴权。

**语法**

```
bl sandbox delete --sandbox-id <id>
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--sandbox-id <id>`

string

是

Sandbox 实例 ID

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久释放 Sandbox 实例，且无法撤销。

**示例**：预览释放指定 Sandbox 实例的资源

```
bl sandbox delete --sandbox-id sbx-xxx --dry-run
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

## 模版管理

### bl sandbox template list

列出 Sandbox 模版。需要 API Key 鉴权。

**语法**

```
bl sandbox template list [--limit <n>] [--cursor <cursor>]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--limit <n>`

number

否

最大返回数量（1–100）

`--cursor <cursor>`

string

否

服务端分页 Cursor

**示例**：列出最多 100 个 Sandbox 模版并输出 JSON 格式

```
bl sandbox template list --limit 100 --output json
```

-   API 响应未提供下一页 Cursor，因此不支持自动 --all 翻页。

### bl sandbox template get

获取 Sandbox 模版详情。需要 API Key 鉴权。

**语法**

```
bl sandbox template get --template-id <id>
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--template-id <id>`

string

是

Sandbox 模版 ID

**示例**：获取指定 Sandbox 模版的详情

```
bl sandbox template get --template-id tpl-xxx
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox template create

创建 Sandbox 模版。需要 API Key 鉴权。

**语法**

```
bl sandbox template create (--name <name> --cpu-count <cores> --memory-mb <mb> | --body <json|@path>) [flags]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--body <json|@path>`

string

否

JSON 请求体，可内联或从 @文件路径读取；显式 Flag 优先

`--image <preset>`

string

否

内置镜像 ID 或中文名；自动填写 fromImage 和 imageName

`--name <name>`

string

否

模版名称

`--cpu-count <cores>`

number

否

vCPU 核数

`--memory-mb <mb>`

number

否

内存大小（MB）

`--from-image <image>`

string

否

基础镜像标识

`--image-name <name>`

string

否

基础镜像展示名称

`--env <key=value>`

array

否

模版环境变量；可重复传入

`--allow-out <address>`

array

否

出站白名单条目；可重复传入

`--deny-out <address>`

array

否

出站黑名单条目；可重复传入

`--auto-pause-time <seconds>`

number

否

在 300–604800 秒后自动暂停

`--max-running-time <seconds>`

number

否

最大运行时间（秒，300–604800）

`--description <text>`

string

否

模版描述

`--tag <tag>`

array

否

E2B Tag；可重复传入

`--alias <alias>`

string

否

E2B 模版别名

`--async`

switch

否

提交后立即返回 templateID/buildID，不轮询构建状态

`--poll-interval <seconds>`

number

否

模版构建轮询间隔（默认：5 秒）

**示例**：创建名为 browser 的 Sandbox 模版并配置资源

```
bl sandbox template create --name browser --image browser --cpu-count 1 --memory-mb 2048
```

-   \--image 覆盖 body 中的 fromImage/imageName；显式 --from-image/--image-name 再覆盖对应预设字段。不传 --image 时保持原有镜像行为。
-   挂载本地文件前先调用 sandbox file upload；将可用文件的 id 填入 --body 的 mntConfig\[\].originFileId，并传入 mountPath 和可选的 originFileName。上传和模版须位于同一工作空间。其他完整嵌套结构也可通过 --body 提供。
-   默认等待构建状态变为 ready；--async 会立即返回已提交的构建信息。

### bl sandbox template update

更新 Sandbox 模版。需要 API Key 鉴权。

**语法**

```
bl sandbox template update --template-id <id> (--body <json|@path> | [fields])
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--template-id <id>`

string

是

Sandbox 模版 ID

`--body <json|@path>`

string

否

JSON 请求体，可内联或从 @文件路径读取；显式 Flag 优先

`--image <preset>`

string

否

内置镜像 ID 或中文名；自动填写 fromImage 和 imageName

`--name <name>`

string

否

模版名称

`--cpu-count <cores>`

number

否

vCPU 核数

`--memory-mb <mb>`

number

否

内存大小（MB）

`--from-image <image>`

string

否

基础镜像标识

`--image-name <name>`

string

否

基础镜像展示名称

`--env <key=value>`

array

否

模版环境变量；可重复传入

`--allow-out <address>`

array

否

出站白名单条目；可重复传入

`--deny-out <address>`

array

否

出站黑名单条目；可重复传入

`--auto-pause-time <seconds>`

number

否

在 300–604800 秒后自动暂停

`--max-running-time <seconds>`

number

否

最大运行时间（秒，300–604800）

`--description <text>`

string

否

模版描述

`--async`

switch

否

提交后立即返回 templateID/buildID，不轮询构建状态

`--poll-interval <seconds>`

number

否

模版构建轮询间隔（默认：5 秒）

**示例**：更新指定 Sandbox 模版的镜像信息

```
bl sandbox template update --template-id tpl-xxx --image all-in-one
```

-   \--image 覆盖 body 中的 fromImage/imageName；显式 --from-image/--image-name 再覆盖对应预设字段。不传 --image 时保持原有镜像行为。
-   传入 envConfig 或 --env 会整体替换模版的环境变量 Map。
-   本地挂载文件先通过 sandbox file upload 上传。在 --body 的 mntConfig\[\] 中，将 originFileId 设为可用文件的 id 并传入 mountPath；上传和模版须位于同一工作空间。
-   默认等待构建状态变为 ready；--async 会立即返回已提交的构建信息。

### bl sandbox template build-status

获取 Sandbox 模版构建状态。需要 API Key 鉴权。

**语法**

```
bl sandbox template build-status --template-id <id> --build-id <id>
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--template-id <id>`

string

是

Sandbox 模版 ID

`--build-id <id>`

string

是

模版构建 ID

**示例**：获取指定模版构建状态的详细信息

```
bl sandbox template build-status --template-id tpl-xxx --build-id build-xxx
```

-   鉴权：使用百炼 API Key 作为 Authorization Bearer Token；不会发送 E2B Key。
-   Base URL 优先级：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。CLI 取其 origin 并追加 /api/v1/agentstudio/sandbox；未配置时使用工作空间的 cn-beijing Endpoint。
-   未配置 Base URL 时必须提供 Workspace：--workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id。
-   Sandbox 当前仅支持 cn-beijing，首次使用前需完成 SLR 授权。
-   全局 --timeout 限制 HTTP 请求和模版构建总轮询时间；--instance-timeout 映射到 Sandbox API 的实例存活时间字段。

### bl sandbox template delete

删除 Sandbox 模版。需要 API Key 鉴权。

**语法**

```
bl sandbox template delete --template-id <id>
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--template-id <id>`

string

是

Sandbox 模版 ID

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除 Sandbox 模版，且无法撤销。

**示例**：预览删除指定模版

```
bl sandbox template delete --template-id tpl-xxx --dry-run
```

-   仍有运行中或已暂停实例使用该模版时，服务端会拒绝删除。

## 内置镜像与文件

### bl sandbox official-images

列出 CLI 内置的 Sandbox 基础镜像（离线）。无需鉴权。

**语法**

```
bl sandbox official-images
```

该命令仅支持全局参数。

**示例**：JSON 输出内置基础镜像列表

```
bl sandbox official-images --output json
```

-   在 template create/update 中通过 --image 传入预设 ID 或中文名。这些是固定版本的 cn-beijing 镜像，其他环境可能不同；自定义镜像使用 --from-image。

### bl sandbox file upload

上传工作空间文件，供 Sandbox 模版挂载使用。需要 API Key 鉴权。

**语法**

```
bl sandbox file upload --path <path> [--filename <name>] [--mime-type <type>]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--path <path>`

string

是

本地文件路径

`--filename <name>`

string

否

覆盖远端文件名

`--mime-type <type>`

string

否

Multipart 文件部分的 MIME 类型（默认：application/octet-stream）

**示例**：上传文件并输出 JSON 结果

```
bl sandbox file upload --path ./config.json --output json
```

-   向 /api/v1/agentstudio/files 发送 multipart 字段 file 和 source=sandbox\_template。使用百炼 Bearer API Key，不使用 Console 鉴权或 E2B Key；无需 agents.yaml。
-   Base URL 沿用 Sandbox：--base-url > DASHSCOPE\_BASE\_URL > 登录/Profile 的 base\_url。未配置时，按 --workspace-id > BAILIAN\_WORKSPACE\_ID > 配置项 workspace\_id 选择 cn-beijing 地址。上传路径不带 /sandbox 前缀。
-   上传响应返回后立即输出，--quiet 仅输出 id。不会等待安全审核：status=checking 不代表已可挂载。在同一工作空间的 template create/update --body 中，将可用文件的 id 填入 mntConfig\[\].originFileId，同时传入 mountPath 和可选的 originFileName。此命令不向运行中的实例传文件。
-   文件最大 50 MB。类型按扩展名校验：`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 不支持；`.yaml` 可以。完整范围以接口返回为准。
-   模版挂载时，`mntConfig[].mountPath` 必须以 `/home/user/workspace/uploads/` 开头，推荐写完整文件路径。路径不在该目录下时，接口接受配置，但实例中不会出现文件。
-   上传参数、文件类型与完整示例详见[文件上传](https://help.aliyun.com/zh/model-studio/sandbox-api-overview#h-sandbox-api-file-upload)。
-   \--dry-run 仅预览 Endpoint、source 和本地路径，不读取或上传文件。MIME 类型检测和上传限制由服务端执行。
