# 查询导出状态

查询导出任务状态与下载链接。仅 export\_status 为 success 且 link 非空时可下载。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 接口

**GET** `/export_status`

查询导出任务状态与下载链接。仅 `export_status` 为 `success` 且 `link` 非空时可下载。

## 请求参数

参数

必填

类型

说明

`export_id`

是

integer

导出任务 ID，取自导出告警接口返回值

## 请求示例

```
curl -X GET "$BASE_URL/export_status?export_id=131231" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

## 响应体

字段

类型

说明

`export_status`

string

`init` / `exporting` / `success`。仅 `success` 且 `link` 非空时可下载

`progress`

integer

导出进度百分比，0-100

`current_count`

integer

当前已导出条数

`total_count`

integer

导出任务记录总数

`link`

string

Excel 下载链接，任务未完成或失败时为 `null`

`message`

string

结果提示，成功时固定为 `success`

## 响应示例

```
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
