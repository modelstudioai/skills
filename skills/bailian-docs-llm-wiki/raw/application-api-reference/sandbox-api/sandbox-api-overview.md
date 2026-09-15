# API 总览与认证

Sandbox API 兼容 E2B 协议，提供沙箱实例的生命周期管理与模版管理能力，通过阿里云百炼 AI 网关转发。

Sandbox API 兼容 [E2B](https://e2b.dev/docs) 协议，提供沙箱实例的生命周期管理与模版管理能力。管控面请求经阿里云百炼 AI 网关转发。

## 前提条件

1.  **开通阿里云百炼并创建 API Key**：通过[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取。
2.  **完成服务授权**：首次使用 Sandbox 需完成 SLR 授权，详见[快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md)。
3.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `{workspace_id}`。

## Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sandbox
```

-   `workspace_id`：工作空间 ID
-   `region`：地域 ID，当前仅支持 `cn-beijing`

## 鉴权

全部请求通过 HTTP Header 携带阿里云百炼 API Key：

```
Authorization: Bearer <your-api-key>
```

使用 E2B SDK 时，SDK 必填的 `X-API-Key` / `api_key` 仅用于满足 E2B 协议格式，阿里云百炼侧不使用它做业务鉴权。推荐填写 `e2b_${ALIYUN_UID}`。

**说明**兼容 E2B 协议的接口返回体贴近 E2B 原生响应结构，不封装为阿里云百炼统一 `Result<T>` 结构。

## 可用 API

### 实例管理

**能力**

**方法**

**路径**

创建实例

`POST`

`/sandboxes`

列举实例

`GET`

`/v2/sandboxes`

获取实例

`GET`

`/sandboxes/{sandboxID}`

连接实例

`POST`

`/sandboxes/{sandboxID}/connect`

暂停实例

`POST`

`/sandboxes/{sandboxID}/pause`

恢复实例

`POST`

`/sandboxes/{sandboxID}/resume`

释放实例

`DELETE`

`/sandboxes/{sandboxID}`

### 模版管理

**能力**

**方法**

**路径**

创建模版

`POST`

`/v3/templates`

列举模版

`GET`

`/v2/templates`

获取模版

`GET`

`/templates/{templateCode}`

更新模版

`PUT`

`/templates/{templateCode}`

获取构建状态

`GET`

`/templates/{templateCode}/builds/{buildID}/status`

删除模版

`DELETE`

`/templates/{templateCode}`

## 错误响应

调用出错时，接口返回的错误响应如下：

```
{
  "code": 100004,
  "message": "参数缺失",
  "requestID": "request-id"
}
```

常见 HTTP 状态码含义如下：

HTTP 状态码

说明

400

参数缺失、格式错误、超出取值范围

401

API Key 无效

404

模版或实例不存在

409

当前资源状态不允许执行该操作

500

服务内部异常

501

当前版本暂不支持

## E2B 官方参考

Sandbox 当前对外提供兼容 E2B 协议的 HTTP API。各接口的方法、路径与响应结构贴近 E2B 官方定义，除更新模版为阿里云百炼自定义协议外，其余接口的通用字段与语义可参阅 E2B 官方 API 文档：

-   [E2B API Reference](https://docs.e2b.dev/api-reference)

**说明**本文仅列出阿里云百炼侧已支持的接口与阿里云百炼扩展字段。阿里云百炼侧的鉴权、Endpoint 与扩展配置以本文为准；通用协议字段可对照 E2B 官方文档理解。

## SDK

除直接调用 REST 接口外，还可通过 E2B 官方 SDK 接入。详见[实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)。
