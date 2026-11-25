# 列举模版

列举当前工作空间下的沙箱模版，支持按游标分页。

<a id="前提"></a>

<a id="h-sbxapi-tpl-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../sandbox-api-overview.md)。

<a id="接口"></a>

<a id="h-sbxapi-tpl-list-endpoint"></a>

## 接口

**GET** `/v2/templates`

列举当前工作空间下的模版。兼容路由 `GET /templates`。

<a id="查询参数"></a>

<a id="h-sbxapi-tpl-list-query"></a>

## 查询参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `limit` | 否 | integer | 单页条数，默认 100，最大 100 |
| `cursor` | 否 | string | 分页位置标识 |

<a id="请求示例"></a>

<a id="h-sbxapi-tpl-list-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X GET "$BASE_URL/v2/templates?limit=100" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-sbxapi-tpl-list-resp"></a>

## 响应示例

响应体直接返回模版数组，不封装为分页对象。

<a id="code-block-2"></a>

```json
[
  {
    "templateID": "your-template-id",
    "templateName": "my-template",
    "cpuCount": 1,
    "memoryMB": 2048,
    "public": false,
    "aliases": [],
    "names": ["my-template"],
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z",
    "spawnCount": 2,
    "buildCount": 1,
    "envdVersion": "your-envd-version"
  }
]
```

<a id="响应字段"></a>

<a id="h-sbxapi-tpl-list-dto"></a>

### 响应字段

数组元素字段如下。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `templateID` | string | 模版 ID |
| `templateName` | string | 模版名称 |
| `cpuCount` | integer | vCPU 数量 |
| `memoryMB` | integer | 内存大小，单位 MB |
| `public` | boolean | 是否公开 |
| `aliases` | array<string> | 别名列表 |
| `names` | array<string> | 模版名称列表 |
| `createdAt` | string | 创建时间，date-time 格式 |
| `updatedAt` | string | 更新时间，date-time 格式 |
| `spawnCount` | integer | 当前模版实例数量 |
| `buildCount` | integer | 模版版本数量 |
| `envdVersion` | string | envd 版本 |
