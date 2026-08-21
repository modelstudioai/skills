# AsyncEditTimeline - 编辑剪辑口播时间线

编辑剪辑任务的timeline

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncEditTimeline)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncEditTimeline)

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

aimiaobi:AsyncEditTimeline

update

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

TaskId

string

是

任务唯一标识

0dbf1055f8a2475d99904c3b76a0ffba

Timelines

array<object>

是

剪辑时间线数组结构

object

是

Clips

array<object>

是

剪辑片段数组

object

否

剪辑片段

OutEx

float

否

片段结束时间（毫秒）

3.66

ClipId

string

否

片段 ID。

123jjdax 新增可为空

VideoId

string

否

视频 ID

7036227ae3ab71efbb4a6733a68f0102 不可为空

VideoName

string

否

视频名称

123.mp4 不可为空

In

integer

否

开始时间（妙）已经废弃

0 不可为空

ContentInner

string

否

口播文案分段

口播文案分段 不可为空

InEx

float

否

片段开始时间（毫秒）

0.45

Out

integer

否

结束时间（妙）已经废弃

5 不可为空

TimelineId

string

否

时间线 Id

sdfjhks 新增可为空

WorkspaceId

string

是

[百炼业务空间 Id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-az2gglkjauwnnhpq

AutoClips

boolean

否

是否开启自动调整能力

false

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Code

string

状态码

successful

Data

object

业务数据

TaskId

string

唯一任务 ID

51e4efd1908242eb93ca9bbb7fc4359d

Message

string

返回信息

一些建议信息

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

此次请求是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "successful",
  "Data": {
    "TaskId": "51e4efd1908242eb93ca9bbb7fc4359d",
    "Message": "一些建议信息"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
