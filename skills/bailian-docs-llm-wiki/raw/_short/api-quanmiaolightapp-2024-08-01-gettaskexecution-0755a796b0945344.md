# GetTaskExecutionStatistics

查询任务执行情况统计

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

当前API暂无授权信息透出。

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/quanmiao/lightapp/getTaskExecutionStatistics HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 否 | 百炼业务空间唯一标识：[获取 workspaceId](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | llm-xxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| taskCode | string | 是 | 任务类型标识 | EssayCorrectionTask |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| requestId | string | Id of the request | A1B2C3D4-E5F6-7890-GHIJ-KLMNOPQRST |
| code | string | 错误码 | Success |
| httpStatusCode | integer | Http 状态码 | 200 |
| message | string | 响应失败时的消息 | 成功 |
| success | boolean | true:此次接口响应成功,false:响应失败 | true |
| data | object | 结果对象 |  |
| runningCount | integer | 运行中的任务个数 | 5 |
| waitingCount | integer | 排队中的任务个数 | 10 |
| completedCount | integer | 已完成的任务个数 | 100 |
| tpmPerMinute | array<object> | 最近一天内 TPM 每分钟完成任务数量 |  |
|  | object | 每分钟完成任务数 |  |
| time | string | 时间点（分钟粒度），格式：yyyy-MM-dd HH:mm | 2024-08-01 10:00 |
| count | integer | 该分钟内完成任务数量 | 3 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "requestId": "A1B2C3D4-E5F6-7890-GHIJ-KLMNOPQRST",
  "code": "Success",
  "httpStatusCode": 200,
  "message": "成功",
  "success": true,
  "data": {
    "runningCount": 5,
    "waitingCount": 10,
    "completedCount": 100,
    "tpmPerMinute": [
      {
        "time": "2024-08-01 10:00",
        "count": 3
      }
    ]
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action , Please check the assignment of the workspaceId. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/GetTaskExecutionStatistics#workbench-doc-change-demo)。
