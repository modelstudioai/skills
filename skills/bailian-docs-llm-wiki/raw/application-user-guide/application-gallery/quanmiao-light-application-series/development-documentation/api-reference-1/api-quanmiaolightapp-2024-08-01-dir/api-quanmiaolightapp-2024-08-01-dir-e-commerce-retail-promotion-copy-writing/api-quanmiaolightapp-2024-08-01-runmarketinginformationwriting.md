# RunMarketingInformationWriting - 电商零售推广文案写作

电商零售推广文案写作。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunMarketingInformationWriting)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunMarketingInformationWriting)

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

quanmiaolightapp:RunMarketingInformationWriting

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runMarketingInformationWriting HTTP/1.1
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

路径参数，[业务空间 id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

w-26ca1703f6d71e6e

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

modelId

string

否

大模型 ID。

qwen-max qwen-plus

writingType

string

否

写作类型： generateProductTitle - 生成商品标题 productTitleTranslation - 商品标题翻译 generateProductSummary - 生成商品摘要 productRedBook-生成关于某产品的小红书笔记 productEvaluating-商品使用测评文案 circleOfFriends-适合发朋友圈的推广营销文案 marketingActivities-营销活动的宣传文案 productAdvertisement-某公司/产品的广告词 travel-旅游类营销推广文章 other-其他类型的营销文案

productRedBook

customPrompt

string

否

自定义写作要求

语言要精美。

sourceMaterial

string

否

写作参考内容

ps5是sony新一代的游戏机，他创新性的...

customLimitation

string

否

自定义写作限制

不要有错别字

inputExample

string

否

自定义写作输入素材样例

产品名字：xxx 产品特点：xxx

outputExample

string

否

自定义写作输出格式样例

写作输出内容样例

language

string

否

目标语言（用于商品标题翻译）

en

keywords

string

否

关键词（用于生成商品标题和商品摘要）

运动鞋 透气 减震 跑步

generateCount

string

否

生成数量（用于生成商品标题和商品摘要，取值范围：1-15）

5

wordCountRange

string

否

字数范围（用于商品标题翻译，格式：最小字数-最大字数）

10-20

otherRequirements

string

否

其他要求（用于三种新的写作类型：generateProductTitle、generateProductSummary、productTitleTranslation）

要求标题简洁有力，突出产品特点

prompt

string

否

自定义提示词（用于可控式生成模型，适用写作类型：generateProductTitle、generateProductSummary、productTitleTranslation）

请根据关键词生成吸引人的商品标题

extParameters

object

否

扩展参数（Map 结构，所有参数值均为 String 类型）：

-   enableThinking：是否启用思考模式，取值为 "true" 或 "false"
    
-   thinkingBudget：思考预算，用于控制思考模式的预算（整数，字符串形式）
    
-   resultFormat：结果格式，用于设置输出格式
    
-   incrementalOutput：是否启用增量输出，取值为 "true" 或 "false"
    

{ "minWordLength": "10", "maxWordLength": "50", "enableThinking": "true", "thinkingBudget": "2000" }

string

否

参数 KEY

大模型参数KEY

apiKey

string

否

集成接入的 API 密钥。获取[API- KEY](https://help.aliyun.com/zh/model-studio/get-api-key)

sk-8de1d655ee27496c88b320fbcbc15d73

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

end

boolean

是否结束

2024-06-21T10:29:52+08:00

header

object

HTTP 请求头。格式为 key1:value1，通过回车键换行。

event

string

event 名称

result-generated

eventInfo

string

event 描述

可空

requestId

string

请求 RequestId

436BC5AE-0573-59D8-9803-6B5FDCD3BBA1

sessionId

string

对应的会话 id

uqubxgqzlnf4exfektij032lgb3yvix678p232n56387aqxdo4uutdt9wstqzovvz6j3ho7wnbgye785u79yn5q3euqmsvzmqdn3nmfq2826oscjvsi43kof8b8uxufpp1x97jjukk6jd3183hy8ni6hqpskuhuascpd

taskId

string

任务 ID

13312125943232

traceId

string

跟踪 ID

213e20e517049392478441155e8b2a

errorMessage

string

错误消息

错误消息

payload

object

返回结果的 payload,json 结构，不同 event 结构不同

output

object

输出

text

string

写作内容返回

playstation5新时代的...

reasonContent

string

模型推理内容

推理内容

usage

object

token 描述

inputTokens

integer

输入 token 数

100

outputTokens

integer

输出 token 数

100

totalTokens

integer

总 token 数

200

## 示例

正常返回示例

`JSON`格式

```
{
  "end": true,
  "header": {
    "event": "result-generated",
    "eventInfo": "可空",
    "requestId": "436BC5AE-0573-59D8-9803-6B5FDCD3BBA1",
    "sessionId": "uqubxgqzlnf4exfektij032lgb3yvix678p232n56387aqxdo4uutdt9wstqzovvz6j3ho7wnbgye785u79yn5q3euqmsvzmqdn3nmfq2826oscjvsi43kof8b8uxufpp1x97jjukk6jd3183hy8ni6hqpskuhuascpd",
    "taskId": "13312125943232",
    "traceId": "213e20e517049392478441155e8b2a",
    "errorMessage": "错误消息"
  },
  "payload": {
    "output": {
      "text": "playstation5新时代的...",
      "reasonContent": "推理内容"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunMarketingInformationWriting#workbench-doc-change-demo)。
