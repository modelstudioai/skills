# UpdateVideoDetectShotConfig - 智能拆条-更新配置

智能拆条-更新配置

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoDetectShotConfig)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoDetectShotConfig)

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

quanmiaolightapp:UpdateVideoDetectShotConfig

update

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{workspaceId}/quanmiao/lightapp/videoAnalysis/updateVideoDetectShotConfig HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

asyncConcurrency

integer

是

视频理解-离线任务并发数，取值范围\[2, 10\]

2

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

1813ceee-7fe5-41b4-87e5-982a4d18cca5

code

string

状态码

xx

message

string

错误说明

ok

success

boolean

是否成功：true 成功，false 失败

True

httpStatusCode

integer

http 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "code": "xx",
  "message": "ok",
  "success": true,
  "httpStatusCode": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-10-20

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/UpdateVideoDetectShotConfig?updateTime=2025-10-20#workbench-doc-change-demo)
