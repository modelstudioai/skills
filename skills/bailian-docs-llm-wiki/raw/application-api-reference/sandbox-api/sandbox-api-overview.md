# 概览

Sandbox API 的前提条件、Endpoint 拼装、鉴权方式，以及实例与模版管理的可用接口和错误响应。

**说明**调用前请先配置[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；错误处理见[错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

Sandbox API 兼容 [E2B](https://e2b.dev/docs) 协议，提供沙箱实例的生命周期管理、模版管理与文件上传能力。管控面请求经阿里云百炼 AI 网关转发。

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。
2.  **完成服务授权**：首次使用 Sandbox 需完成 SLR 授权，详见[快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)。
3.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `{workspace_id}`。

## Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sandbox
```

-   `workspace_id`：工作空间 ID
-   `region`：地域 ID，当前仅支持 `cn-beijing`

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

**说明**创建或更新模版时，`mntConfig` 中的文件需先按[文件上传](https://help.aliyun.com/zh/model-studio/sandbox-api-overview#h-sandbox-api-file-upload)章节上传，并带 `source=sandbox_template`；上传后等待 `status` 变为 `available`。

## 文件上传

挂载文件需通过文件上传接口上传，并在请求中指定 `source=sandbox_template`。

### Endpoint

```
POST https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/files
```

### 表单上传

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -F "file=@./config.json" \
  -F "source=sandbox_template"
```

响应：

```
{
  "id": "file_xxx",
  "type": "file",
  "filename": "config.json",
  "downloadable": false,
  "mime_type": "application/json",
  "size_bytes": 128,
  "status": "checking",
  "created_at": "2026-10-21T15:00:00+08:00",
  "request_id": "xxx"
}
```

### 预签名地址上传

适合大文件或直传 OSS。

1.  申请上传地址。

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "config.json",
    "mimeType": "application/json",
    "sizeBytes": 128,
    "source": "sandbox_template"
  }'
```

2.  将文件内容 PUT 到响应中的 `upload_url`。不要额外设置 `Content-Type`，否则可能返回 `403 SignatureDoesNotMatch`。
    
3.  调用 `POST /api/v1/agentstudio/files/{file_id}/complete` 完成上传。
    
4.  轮询 `GET /api/v1/agentstudio/files/{file_id}`，待 `status` 变为 `available`。
    

### 文件限制

维度

限制

单文件大小

50 MB

工作空间文件总容量

100 GB

保存时效

30 天

文件类型按扩展名校验：`.yaml` 可上传；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 不支持；`.ts` 返回视频格式错误。完整范围以接口返回为准。

**说明**只有 `source=sandbox_template` 且 `status=available` 的文件可写入 `mntConfig`。文件相关错误码见[错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

## E2B 官方参考

Sandbox 当前对外提供兼容 E2B 协议的 HTTP API。各接口的方法、路径与响应结构贴近 E2B 官方定义，除更新模版为阿里云百炼自定义协议外，其余接口的通用字段与语义可参阅 E2B 官方 API 文档：

-   [E2B API Reference](https://docs.e2b.dev/api-reference)

**说明**本文仅列出阿里云百炼侧已支持的接口与阿里云百炼扩展字段。阿里云百炼侧的鉴权、Endpoint 与扩展配置以本文为准；通用协议字段可对照 E2B 官方文档理解。

## SDK

除直接调用 REST 接口外，还可通过 E2B 官方 SDK 接入。详见[实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。
