# 获取构建状态

查询模版的镜像构建状态。构建状态变为 ready 后才能基于该模版创建实例。

<a id="前提"></a>

<a id="h-sbxapi-tpl-build-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../sandbox-api-overview.md)。

<a id="接口"></a>

<a id="h-sbxapi-tpl-build-endpoint"></a>

## 接口

**GET** `/templates/{templateCode}/builds/{buildID}/status`

查询模版的镜像构建状态。兼容路由 `GET /templates/{templateCode}/builds/{buildID}`。`buildID` 来自创建/更新模版接口的响应。构建状态变为 `ready` 后才能基于该模版创建实例。

<a id="路径参数"></a>

<a id="h-sbxapi-tpl-build-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `templateCode` | 是 | string | 模版唯一 code（即 `templateID`） |
| `buildID` | 是 | string | 构建 ID，来自创建/更新模版接口的响应 |

<a id="请求示例"></a>

<a id="h-sbxapi-tpl-build-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X GET "$BASE_URL/templates/your-template-id/builds/your-build-id/status" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-sbxapi-tpl-build-resp"></a>

## 响应示例

构建失败时返回 `reason` 对象说明失败原因。

<a id="code-block-2"></a>

```json
{
  "templateID": "your-template-id",
  "buildID": "your-build-id",
  "status": "ready",
  "logs": ["build started", "build finished"],
  "logEntries": []
}
```

<a id="响应字段"></a>

<a id="h-sbxapi-tpl-build-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `templateID` | string | 模版 ID |
| `buildID` | string | 构建 ID |
| `status` | string | 构建状态，取值为 `building`、`ready`、`error`。最终为 `ready`；失败时为 `error` |
| `logs` | array<string> | 构建日志 |
| `logEntries` | array<object> | 结构化构建日志条目 |
| `reason` | object | 构建失败原因；成功时省略。子字段 `code`（string，失败原因码，例如 `InvalidArgument`）、`message`（string，失败原因说明） |
