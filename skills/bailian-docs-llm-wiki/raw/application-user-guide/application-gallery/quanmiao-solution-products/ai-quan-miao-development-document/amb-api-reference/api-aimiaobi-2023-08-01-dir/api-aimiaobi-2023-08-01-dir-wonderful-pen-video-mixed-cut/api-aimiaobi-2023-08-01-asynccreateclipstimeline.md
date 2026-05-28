# AsyncCreateClipsTimeLine - 创建剪辑口播时间线

智能剪辑timeline

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncCreateClipsTimeLine)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncCreateClipsTimeLine)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:AsyncCreateClipsTimeLine

create

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

TaskId

string

是

任务唯一 ID

7AA2AE16-D873-5C5F-9708-15396C382EB1

ProcessPrompt

string

否

处理用 prompt

口播内容是乌镇旅游宣传广告，口播内容时长约为1分钟，开头要描述乌镇是千年文化传承的江南水乡，之后要体现乌镇的传统手工艺、美食和美景，最后要号召大家来乌镇旅游

WorkspaceId

string

是

[百炼工作空间 Id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-2setzb9x4ewsd

CustomContent

string

否

自定义口播内容

自定义口播内容

NoRefVideo

boolean

否

是否开启模仿能力

默认开启

AdditionalContent

string

否

素材附加信息，有助于口播文案的生成

素材附加信息

RecommendAudio

boolean

否

false

TimelineScene

integer

否

null - 通用口播 0-通用口播 1- 高光

HighLightConfig

object

否

HtPrompt

string

否

请从输入的音乐演出视频中，自动识别并提取出「最具视觉冲击力、情感爆发力或独特吸引力」...

HtHighQualityLabel

array

否

\[ "高清演员近景特写镜头【高优】", "演出高潮-沉浸表演【高优】", "演出高潮-近景表情【高优】" \]

string

否

"高清演员近景特写镜头【高优】"

HtLowQualityLabel

array

否

\[ "画面昏暗", "采访画面", "字幕画面" \]

string

否

"画面昏暗"

HtMinTimeLength

integer

否

10

HtMaxTimeLength

integer

否

20

HtSingleShotLen

integer

否

1.5

HtAnalyzeRhythm

boolean

否

false

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

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

任务 id

3f7045e099474ba28ceca1b4eb6d6e21

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

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "successful",
  "Data": {
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/AsyncCreateClipsTimeLine#workbench-doc-change-demo)。
