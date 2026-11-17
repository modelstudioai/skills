# 获取 Environment

根据环境 ID 查询准备状态和已安装资产的安全元数据。

## 接口

**GET** `/agents/environments/{environment_id}`

返回指定环境的当前状态和安全元数据。成功返回 `200`。

## 路径参数

**environment\_id** `string` **（必选）**

创建回执中的环境 ID，不是 Session ID、模板 ID 或 sandbox ID

无请求体。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/environments/ccarenv_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

environment = client.beta.agents.environments.retrieve("ccarenv_xxx")
print(environment.status)
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

`ready` 表示环境准备完成，可以创建引用该环境的 Session。`connected` 表示实例已经连接，不保证后续每条命令都成功。

## 响应示例

```
{
  "id": "ccarenv_xxx",
  "object": "agent.environment",
  "type": "openai_hosted",
  "status": "ready",
  "files": [],
  "skills": [],
  "plugins": []
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且可见的环境 ID

`503`

`server_error` / `environment_unavailable`

稍后重试；持续失败时提交工单并提供 `x-request-id`

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 HTTP 状态、`x-request-id` 和环境 ID。
