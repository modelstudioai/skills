# 认证

OpenAI 兼容 API 的 API Key 获取、Endpoint 和 OpenAI SDK 配置方式。

## 获取 API Key

1.  打开[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)，登录阿里云账号并开通百炼。
2.  在 **API Key** 页面创建并复制 API Key。

**警告**API Key 具有账号级权限，请妥善保管，不要在公开渠道分享或提交到代码仓库。

## 使用 API Key

将 API Key 配置为环境变量，每个请求携带 `Authorization` Header：

```
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

`OpenAI-Beta: agents=v1` 用于兼容 OpenAI Agents API 客户端；该接口不依赖该 Header 选择默认值。

## Endpoint

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

通过工作空间专属域名访问，API Key 需要属于目标工作空间。当前地域为 `cn-beijing`。将 `{workspace_id}` 替换为实际工作空间 ID。

## OpenAI SDK 配置

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
```

配置完成后，可以从[快速开始](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-quickstart.md)或[Agent](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-agent.md)开始调用。

## 权限说明

-   **阿里云主账号**：可以直接调用全部接口。
-   **RAM 子账号**：需要获得相应权限授权后调用。
-   API Key 的权限范围由控制台配置。API Key 只能访问其归属工作空间下的资源。

## 请求标识

响应头携带 `x-request-id`，排查问题时保留该值。业务错误正文的结构见[错误码](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。
