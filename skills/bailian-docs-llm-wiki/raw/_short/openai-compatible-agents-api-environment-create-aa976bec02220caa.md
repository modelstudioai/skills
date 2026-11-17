# 创建 Environment

创建托管运行环境，配置容器、依赖、网络、初始文件和 Skill。

## 接口

**POST** `/agents/environments`

创建一个托管运行环境。成功返回 `201`，表示环境已登记并开始异步准备；准备完成前创建引用该环境的 Session 可能失败。

## 请求体

**environment** `object` **（必选）**

环境配置，见下表

属性

**type** `string` **（必选）**

环境类型，固定为 `openai_hosted`

**environment\_template\_id** `string` **（可选）**

环境模板 ID；模板必须属于当前工作空间。模板通过[环境模板](raw/_short/openai-compatible-agents-api-environment-templat-e9481447eb2967a1.md)管理。

**env** `object` **（可选）**

环境变量；变量名需匹配 `[A-Za-z_][A-Za-z0-9_]*`，不能是 `PATH`，也不能以保留前缀开头；值不能包含 NUL

**packages** `object` **（可选）**

预装包，按 `npm`、`python`、`system` 分组

**network** `object` **（可选）**

网络策略，见下表

属性

**access** `string` **（可选）**

网络访问模式，`enabled`、`disabled` 或 `restricted`

**allowed\_domains** `array<string>` **（可选）**

允许的域名，`access=restricted` 时必须非空，只接受主机名，不能包含协议、端口或通配符

**files** `array` **（可选）**

初始文件，当前使用 `file_id` 引用源文件

属性

**type** `string` **（必选）**

文件引用类型，固定为 `file_id`

**path** `string` **（必选）**

环境内绝对路径，必须在 `/workspace/` 内

**file\_id** `string` **（必选）**

通过 `POST /agents/file` 上传后得到的源文件 ID

**desktop** `object` **（可选）**

桌面配置，当前只接受 `enabled=false`，`enabled=true` 返回 `400`

**setup\_commands** `array` **（可选）**

初始化命令，按顺序执行。每项包含必填的 `command` 和可选的 `cwd`，`cwd` 默认为 `/workspace`

**skills** `array` **（可选）**

Skill，当前使用 `skill_reference`，最多 32 项

属性

**type** `string` **（必选）**

Skill 引用类型，固定为 `skill_reference`

**skill\_id** `string` **（必选）**

技能资源 ID

**version** `string` **（可选）**

Skill 版本；省略时解析 `latest` 并冻结具体版本

**capability\_directories** `array` **（可选）**

能力发现目录，必须在 `/workspace/` 内

**vault\_ids** `array<string> / null` **（可选）**

挂载的 Vault，最多 10 个

`plugins` 非空时当前拒绝；`desktop.enabled=true` 当前拒绝。 `skill_id` 来自 Skill API。先通过[创建 Skill](raw/application-api-reference/managed-agents-api/skills-api/skill-create.md)或[列出 Skill](raw/application-api-reference/managed-agents-api/skills-api/skill-list.md)获取可用的 `skill_id` 和版本。

创建支持可选的 `Idempotency-Key` Header。同一工作空间内使用相同的键和请求正文时返回已有资源；键相同但正文不同返回 `409`。

挂载 `unrestricted` Credential 时，`network.access` 必须为 `restricted`，`allowed_domains` 必须非空且合法。

示例：`"skills": [{"type": "skill_reference", "skill_id": "skill_xxx", "version": "1.0"}]`

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/environments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "environment": {
      "type": "openai_hosted",
      "packages": {"python": ["pandas"]}
    }
  }'
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

environment = client.beta.agents.environments.create(
    environment={
        "type": "openai_hosted",
          "packages": {"python": ["pandas"]},
    },
)
print(environment.id, environment.status)
```

### 响应字段

**id** `string`

环境 ID

**object** `string`

Environment 对象类型，固定为 `agent.environment`

**type** `string`

环境类型，固定为 `openai_hosted`

**status** `string`

环境状态：`pending`、`ready`、`connected`、`disconnected`、`suspended`、`expired`、`failed`

**files** `array`

已安装文件的安全元数据，不返回文件内容。

属性

**id** `string`

环境文件 ID

**type** `string`

文件引用类型，固定为 `file_id`

**path** `string`

环境内文件路径

**size\_bytes** `integer`

文件字节数

**file\_id** `string`

原始源文件 ID

**skills** `array`

已安装 Skill 的安全元数据，不返回 Skill 包内容。

属性

**type** `string`

Skill 引用类型，固定为 `skill_reference`

**name** `string`

技能名称

**description** `string`

技能说明

**skill\_id** `string`

技能资源 ID

**version** `string`

已冻结的具体版本

**plugins** `array`

插件列表，当前托管环境返回 `[]`；历史记录中的插件字段不代表可以创建

创建返回 `201` 不表示环境已经 `ready`。使用环境前先获取状态并确认 `ready`。

## 响应示例

```
{
  "id": "ccarenv_xxx",
  "object": "agent.environment",
  "type": "openai_hosted",
  "status": "pending",
  "files": [],
  "skills": [],
  "plugins": []
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `missing_required_parameter`，`param=environment`

在请求体提供 `environment`

`400`

`invalid_request_error` / `invalid_request_error`

按 `environment` 字段说明修正 `type` 和配置

`404`

`not_found_error` / `not_found_error`

使用当前工作空间内存在且可访问的模板或环境

`409`

`conflict_error` / `conflict_error`

同一幂等键使用相同请求正文

`503`

`server_error` / `environment_unavailable` 或 `template_storage_unavailable`

稍后重试；持续失败时提交工单并提供 `x-request-id`

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 HTTP 状态、`x-request-id` 和脱敏后的请求正文。
