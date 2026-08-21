# SubmitEnterpriseVocAnalysisTask - 提交企业VOC分析任务

提交VOC异步任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitEnterpriseVocAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitEnterpriseVocAnalysisTask)

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

aimiaobi:SubmitEnterpriseVocAnalysisTask

get

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

FileKey

string

否

文件 FileKey

oss://default/bucket-name/materialDocument/tenant\_agent/fileName

MaterialType

string

否

素材类型（shortContent：长短评论、或工单，dialogue：对话）

shortContent

ModelId

string

是

模型 ID

qwen-max

ContentTags

array<object>

是

内容标签

object

是

内容标签对象

TagName

string

否

标签名称

一级标签-二级标签

TagValueDefinePrompt

string

否

标签值定义（如果是标签挖掘任务，则此 Prompt 是逗号分隔的枚举值、如果是总结概括人物则是总结概括的 Prompt）

是,否

TagDefinePrompt

string

否

标签定义

一级标签-二级标签

TagTaskType

string

否

标签挖掘任务类型（单标签：singleTagValue，多标签：multiTagValues，总结概括：summaryAndOverview，筛选：filter）

singleTagValue

FilterTags

array<object>

否

过滤标签列表

object

否

过滤标签对象

TagName

string

否

标签名称

一级标签-二级标签

TagValueDefinePrompt

string

否

标签值定义（如果是标签挖掘任务，则此 Prompt 是逗号分隔的枚举值、如果是总结概括人物则是总结概括的 Prompt）

是,否

TagDefinePrompt

string

否

标签定义

一级标签-二级标签

TagType

string

否

标签挖掘任务类型（单标签：singleTagValue，多标签：multiTagValues，总结概括：summaryAndOverview，筛选：filter）

singleTagValue

PositiveSample

string

否

正面样本内容

正面样本

PositiveSampleFileKey

string

否

正面样本文件 FileKey

oss://default/bucket-name/path/xxx.xlsx

TaskType

string

否

任务类型：lightAppSass（Sass 页调用）、sdkBatchTask（SDK 批量调用任务）

lightAppSass

Contents

array<object>

否

待挖掘的素材内容列表

object

否

待挖掘的素材内容对象

Text

string

否

待挖掘的素材

内容文本

ExtraInfo

string

否

额外补充信息，直接给到大模型

额外信息

ApiKey

string

否

集成接入的 API 密钥。获取[API- KEY](https://help.aliyun.com/zh/model-studio/get-api-key)

sk-sdfs2-wewerwe-ere

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

模板校验结果

TaskId

string

任务 ID

xxxxx

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
    "TaskId": "xxxxx"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
