# GetVideoAnalysisConfig - 视频理解-获取配置

视频理解：获取基础配置。

## 接口说明

阿里云百炼轻应用-视频理解-获取配置：通过这个接口可以查看异步任务并发配置。欢迎前往[视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)体验。通过 SDK 方式调用 API 可参考控制台“API”下的示例。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisConfig)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisConfig)

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

quanmiaolightapp:GetVideoAnalysisConfig

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/videoAnalysis/getVideoAnalysisConfig HTTP/1.1
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

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

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

data

object

异步任务并发数

asyncConcurrency

integer

异步任务并发数：取值范围\[2~10\]

2

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "085BE2D2-BB7E-59A6-B688-F2CB32124E7F",
  "code": "xx",
  "message": "ok",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "asyncConcurrency": 2
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
