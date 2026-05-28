# ExportAnalysisTagDetailByTaskId - 根据任务ID导出分析明细

导出挖掘任务明细

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ExportAnalysisTagDetailByTaskId)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/ExportAnalysisTagDetailByTaskId)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

quanmiaolightapp:ExportAnalysisTagDetailByTaskId

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/exportAnalysisTagDetailByTaskId HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxxxxxx

taskId

string

是

任务 ID

a3d1c2ac-f086-4a21-9069-f5631542f5a2

category

string

否

分类筛选

标签分类

categories

array

否

多分类筛选

string

否

标签分类

标签分类列表

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

Id of the request

085BE2D2-BB7E-59A6-B688-F2CB32124E7F

code

string

状态码

xx

message

string

错误消息

ok

httpStatusCode

integer

http 响应码

200

data

string

URL（临时公网可下载的 URL，1 小时失效）

http://www.example.com/xxxx.xlsx

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "085BE2D2-BB7E-59A6-B688-F2CB32124E7F",
  "code": "xx",
  "message": "ok",
  "httpStatusCode": 200,
  "data": "http://www.example.com/xxxx.xlsx"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
