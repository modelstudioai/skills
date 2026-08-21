# GetSmartClipTask - 获取智能剪辑任务结果

查询一键成片剪辑任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartClipTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartClipTask)

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

aimiaobi:GetSmartClipTask

create

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

TaskId

string

是

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

task-03d46184ee7d8749

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

NoData

Data

object

任务响应结果

Status

string

任务状态： PENDING：待执行 RUNNING：执行中 SUCCESSED：成功 FAILED：失败 CANCELED：已取消

RUNNING

ErrorMessage

string

错误消息

错误信息

SubJobs

array<object>

子任务列表

subJobs

object

子任务

SubJobId

string

子任务 ID

xxxxx

Status

string

子任务状态 PENDING：待执行 RUNNING：执行中 SUCCESSED：成功 FAILED：失败 CANCELED：已取消

RUNNING

ErrorMessage

string

错误消息

文件名错误

FileKey

string

文件 FileKey

oss://default/bucket-name/path-xxx/xxx-1.mp4

FileAttr

object

文件属性

FileName

string

视频文件名称

2024-12-12.mp4

FileLength

string

视频文件大小

290804

TmpUrl

string

视频文件临时访问 URL。1 小时过期

http://www.example.com/tmp.mp4

Duration

double

视频时长，单位秒

120

Height

integer

视频高度

1080

Width

integer

视频宽度

1920

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "Status": "RUNNING",
    "ErrorMessage": "错误信息",
    "SubJobs": [
      {
        "SubJobId": "xxxxx",
        "Status": "RUNNING",
        "ErrorMessage": "文件名错误",
        "FileKey": "oss://default/bucket-name/path-xxx/xxx-1.mp4",
        "FileAttr": {
          "FileName": "2024-12-12.mp4",
          "FileLength": 290804,
          "TmpUrl": "http://www.example.com/tmp.mp4",
          "Duration": 120,
          "Height": 1080,
          "Width": 1920
        }
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
