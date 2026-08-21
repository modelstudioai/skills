# BatchCancelTasks - 批量取消异步任务

批量取消任务

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/BatchCancelTasks)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/BatchCancelTasks)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
PUT /{workspaceId}/quanmiao/lightapp/batchCancelTasks HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

否

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskCode

string

是

任务类型标识

EssayCorrectionTask

taskIds

array

否

任务 ID 列表，最多 10000 条

\["xxxx1","xxxx2"\]

string

否

任务 ID

xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

requestId

string

Id of the request

A1B2C3D4-E5F6-7890-GHIJ-KLMNOPQRST

code

string

错误码

Success

httpStatusCode

integer

Http 状态码

200

message

string

响应失败时的消息

成功

success

boolean

true:此次接口响应成功,false:响应失败

true

data

object

结果对象

results

array<object>

取消结果列表

object

取消结果项

taskId

string

任务唯一 ID

xxxx

success

boolean

是否取消成功

true

errorMessage

string

错误信息（取消失败时）

错误信息（取消失败时）

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "A1B2C3D4-E5F6-7890-GHIJ-KLMNOPQRST",
  "code": "Success",
  "httpStatusCode": 200,
  "message": "成功",
  "success": true,
  "data": {
    "results": [
      {
        "taskId": "xxxx",
        "success": true,
        "errorMessage": "错误信息（取消失败时）"
      }
    ]
  }
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/BatchCancelTasks#workbench-doc-change-demo)。
