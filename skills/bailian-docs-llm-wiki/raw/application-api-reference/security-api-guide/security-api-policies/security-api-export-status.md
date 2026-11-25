# 查询导出状态

查询导出任务状态与下载链接。仅 export\_status 为 success 且 link 非空时可下载。

<a id="前提"></a>

<a id="h-secapi-exportstatus-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../security-api-overview.md)。

<a id="接口"></a>

<a id="h-secapi-exportstatus-endpoint"></a>

## 接口

**GET** `/export_status`

查询导出任务状态与下载链接。仅 `export_status` 为 `success` 且 `link` 非空时可下载。

<a id="请求参数"></a>

<a id="h-secapi-exportstatus-params"></a>

## 请求参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `export_id` | 是 | integer | 导出任务 ID，取自导出告警接口返回值 |

<a id="请求示例"></a>

<a id="h-secapi-exportstatus-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X GET "$BASE_URL/export_status?export_id=131231" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应体"></a>

<a id="h-secapi-exportstatus-resp"></a>

## 响应体

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `export_status` | string | `init` / `exporting` / `success`。仅 `success` 且 `link` 非空时可下载 |
| `progress` | integer | 导出进度百分比，0-100 |
| `current_count` | integer | 当前已导出条数 |
| `total_count` | integer | 导出任务记录总数 |
| `link` | string | Excel 下载链接，任务未完成或失败时为 `null` |
| `message` | string | 结果提示，成功时固定为 `success` |

<a id="响应示例"></a>

<a id="h-secapi-exportstatus-resp-eg"></a>

## 响应示例

<a id="code-block-2"></a>

```json
{
  "success": true,
  "data": {
    "export_status": "exporting",
    "progress": 20,
    "current_count": 20,
    "total_count": 100,
    "link": null,
    "message": null
  }
}
```
