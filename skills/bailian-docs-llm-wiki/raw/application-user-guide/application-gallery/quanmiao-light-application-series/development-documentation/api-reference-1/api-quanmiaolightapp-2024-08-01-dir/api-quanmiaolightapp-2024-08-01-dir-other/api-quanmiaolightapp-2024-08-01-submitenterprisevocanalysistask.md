# SubmitEnterpriseVocAnalysisTask - 提交企业VOC挖掘异步任务

提交企业VOC异步任务

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitEnterpriseVocAnalysisTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitEnterpriseVocAnalysisTask)

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

quanmiaolightapp:SubmitEnterpriseVocAnalysisTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/submitEnterpriseVocAnalysisTask HTTP/1.1
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

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskDescription

string

否

任务描述

给你一条待分析文本数据，请你按照标签体系来对数据进行打标。

extraInfo

string

否

业务补充信息

额外信息

outputFormat

string

否

输出格式描述提示词(不传的话默认会根据任务描述生成 json 格式)

请直接输出json格式，不要输出其他内容：

modelId

string

否

模型 ID

qwen-max

tags

array<object>

否

内容标签

object

否

标签体系列表

tagName

string

否

标签名称

xxxx

tagDefinePrompt

string

否

给到大模型的标签定义 Prompt

xxxx

filterTags

array<object>

否

过滤标签

object

否

tagName

string

否

过滤标签名称

过滤标签名称

tagDefinePrompt

string

否

给到大模型的 筛选的标签定义 Prompt

标签抽取的定义的Prompt

contents

array<object>

否

待挖掘的素材内容列表（url、fileKey、contents 三选一）（此数组不超过 200 个，更多请走 fileKey 或 contents 文件形式）

object

否

素材对象

text

string

否

素材内容（字符数不能超过 1w 个）

xxxx

id

string

否

素材 ID

id-xxxxx

url

string

否

待挖掘的素材内容文件 URL(url、fileKey、contents 三选一)（整体文件大小不能超过 100M，素材个数不能超过 6w 条）

http://www.example.com/xxxx.txt

fileKey

string

否

待挖掘的素材内容文件 FileKey(url、fileKey、contents 三选一)（fileKey 是从全妙 SASS 页面上传所获取到的唯一 key）

oss://default/aimiaobi-service-prod/aimiaobi/temp/public/government\_service\_experience\_feedback\_summary.txt

apiKey

string

否

百炼 APIKEY

sk-xxxxxxxx

sourceTrace

boolean

否

是否启用溯源（启用溯源时不支持自定义 outputformat）

batchTask

boolean

否

是否走模型的 BATCH API （费用减半、时效性 24 小时内）

(支持 batchAPI 的模型有：通义千问 Max、Plus、Flash、Turbo、Long 的稳定版本及其部分 latest 版本，以及 QwQ 系列（qwq-plus、qwq-32b-preview）和部分第三方模型（deepseek-r1、deepseek-v3）。 )

positiveFilter

boolean

否

是否正向筛选（true-正向筛选，默认；false-反向筛选）

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

117F5ABE-CF02-5502-9A3F-E56BC9081A64

code

string

状态码

NoPermission

data

object

业务对象

taskId

string

任务 ID

a0cc71ec-fe07-47e5-bf12-6e1c46081c98

httpStatusCode

integer

http 状态码

403

message

string

错误说明

无权限访问接口

success

boolean

接口请求是否成功：true 成功，false 失败

false

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "NoPermission",
  "data": {
    "taskId": "a0cc71ec-fe07-47e5-bf12-6e1c46081c98"
  },
  "httpStatusCode": 403,
  "message": "无权限访问接口",
  "success": false
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitEnterpriseVocAnalysisTask#workbench-doc-change-demo)。
