# RunAiHelperWriting - AI帮写

妙笔：AI助手写作

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunAiHelperWriting)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunAiHelperWriting)

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

aimiaobi:RunAiHelperWriting

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runAiHelperWriting HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxxx

WritingScene

string

是

写作场景：government(政务)、media(传媒)、market(营销)、office(办公)、custom(自定义)

media

WritingStyle

string

是

写作文体唯一标识 KEY，可通过 [ListWritingStyles](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwritingstyles) 接口获取对应写作场景下的文体列表

通知

Prompt

string

是

提示词，需要帮写的主题

请帮我写一篇关于人工智能发展趋势的文章

PromptMode

string

否

提示词模式，如：PE：高级模式，Template：模板模式

Template

DistributeWriting

boolean

否

是否分步骤写作文体

false

WritingParams

object

否

上一次表单的写作参数，键值对形式

{"wordCount": "1000", "tone": "formal"}

string

否

写作参数 KEY VALUE

{"topic":"写作主题"}

## 示例数据

```
{
    "WorkspaceId": "llm-xxx",
    "WritingScene": "office",
    "WritingStyle": "speech",
    "Prompt": "关于“人工智能伦理与社会影响”主题的演讲稿"
}
```

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Header

object

SSE 响应头信息

ErrorCode

string

错误码

InvalidParameter

ErrorMessage

string

错误信息

参数错误

Event

string

事件类型

result-generated

SessionId

string

会话 ID

session-xxxxx

StatusCode

integer

状态码

200

TaskId

string

任务 ID

task-xxxxx

TraceId

string

链路追踪 ID

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Payload

object

响应载荷

Output

object

输出内容

Text

string

生成文本

人工智能正在深刻改变我们的生活...

WritingParams

object

AI 帮写的写作参数

{"wordCount": "1000"}

string

KEY VALUE 形式的键值对

{"topic":"写作主题xxx"}

Usage

object

Token 使用量

InputTokens

integer

输入 Token 数

256

OutputTokens

integer

输出 Token 数

1024

TotalTokens

integer

总 Token 数

1280

RequestId

string

请求 ID

1813ceee-7fe5-41b4-87e5-982a4d18cca5

HttpStatusCode

string

HTTP 状态码

200

Code

string

业务状态码

successful

Message

string

返回信息

success

Success

boolean

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "InvalidParameter",
    "ErrorMessage": "参数错误",
    "Event": "result-generated",
    "SessionId": "session-xxxxx",
    "StatusCode": 200,
    "TaskId": "task-xxxxx",
    "TraceId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5"
  },
  "Payload": {
    "Output": {
      "Text": "人工智能正在深刻改变我们的生活...",
      "WritingParams": {
        "key": "{\"topic\":\"写作主题xxx\"}"
      }
    },
    "Usage": {
      "InputTokens": 256,
      "OutputTokens": 1024,
      "TotalTokens": 1280
    }
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "HttpStatusCode": "200",
  "Code": "successful",
  "Message": "success",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunAiHelperWriting#workbench-doc-change-demo)。
