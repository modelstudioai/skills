# ListWritingStyles - 获取写作文体列表

获取文体列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListWritingStyles)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListWritingStyles)

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

aimiaobi:ListWritingStyles

list

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

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxxx

Scene

string

是

写作场景筛选

枚举值：

-   market：营销写作。
-   government：法定公文 。
-   custom：自定义写作。
-   media：传媒类。
-   office：事务公文。

media

MaxResults

integer

否

返回的最大结果数

100

NextToken

string

否

写一页 Token

下一页token

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

TotalCount

integer

总记录数

58

MaxResults

integer

最大返回结果数

100

NextToken

string

下一个 token

下一页token

Code

string

错误码

successful

Message

string

错误消息

数据不存在

Success

string

此次请求是否成功

true

Data

array<object>

文体列表

data

object

文体对象

StyleName

string

文体名称

文体名称

StyleKey

string

文体唯一标识 KEY

文体唯一标识

StyleDescription

string

文体描述

文体描述

DistributeWriting

boolean

是否支持分步骤写作

false

StyleImage

string

文体图片

文体图片

Emoji

string

文体小图标（字符符号表示）

小图标

TemplateDefine

[WritingStyleTemplateDefine](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-struct-writingstyletemplatedefine)

文体模板定义

DistributeStepTemplateDefine

[WritingStyleTemplateDefine](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-struct-writingstyletemplatedefine)

分步骤模板定义

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "TotalCount": 58,
  "MaxResults": 100,
  "NextToken": "下一页token",
  "Code": "successful",
  "Message": "数据不存在",
  "Success": true,
  "Data": [
    {
      "StyleName": "文体名称",
      "StyleKey": "文体唯一标识",
      "StyleDescription": "文体描述",
      "DistributeWriting": false,
      "StyleImage": "文体图片\n\n",
      "Emoji": "小图标",
      "TemplateDefine": {
        "Fields": [
          {
            "MinItemLength": 1000,
            "Max": 2000,
            "MinLength": 20,
            "MaxLength": 2000,
            "MaxItemLength": 4000,
            "Name": "字段名称",
            "BuildIn": true,
            "Enums": [
              {
                "CascadingFields": [
                  "级联字段"
                ],
                "Key": "枚举KEY",
                "Name": "枚举名称"
              }
            ],
            "Min": 1,
            "Required": false,
            "MaxItem": 10,
            "InitialValue": "初始值",
            "CascadingFields": [
              {
                "MinItemLength": 1000,
                "Max": 2000,
                "MinLength": 20,
                "MaxLength": 2000,
                "MaxItemLength": 4000,
                "Name": "字段名称",
                "BuildIn": true,
                "Enums": [
                  {
                    "CascadingFields": [
                      "级联字段"
                    ],
                    "Key": "枚举KEY",
                    "Name": "枚举名称"
                  }
                ],
                "Min": 1,
                "Required": false,
                "MaxItem": 10,
                "InitialValue": "初始值",
                "CascadingFields": [
                  {
                    "MinItemLength": 1000,
                    "Max": 2000,
                    "MinLength": 20,
                    "MaxLength": 2000,
                    "MaxItemLength": 4000,
                    "Name": "字段名称",
                    "BuildIn": true,
                    "Enums": [
                      {
                        "CascadingFields": [
                          "级联字段"
                        ],
                        "Key": "枚举KEY",
                        "Name": "枚举名称"
                      }
                    ],
                    "Min": 1,
                    "Required": false,
                    "MaxItem": 10,
                    "InitialValue": "初始值",
                    "CascadingFields": [],
                    "Style": {
                      "Placeholder": "清输入Prompt",
                      "Type": "media",
                      "ShowTime": true,
                      "Suffix": "后缀",
                      "Description": "输入框提示文案",
                      "Format": "yyyy-mm-dd"
                    },
                    "Key": "topic"
                  }
                ],
                "Style": {
                  "Placeholder": "清输入Prompt",
                  "Type": "media",
                  "ShowTime": true,
                  "Suffix": "后缀",
                  "Description": "输入框提示文案",
                  "Format": "yyyy-mm-dd"
                },
                "Key": "topic"
              }
            ],
            "Style": {
              "Placeholder": "清输入Prompt",
              "Type": "media",
              "ShowTime": true,
              "Suffix": "后缀",
              "Description": "输入框提示文案",
              "Format": "yyyy-mm-dd"
            },
            "Key": "topic"
          }
        ],
        "Example": [
          {
            "Value": 123,
            "Key": "topic"
          }
        ]
      },
      "DistributeStepTemplateDefine": {
        "Fields": [],
        "Example": [
          {
            "Value": 123,
            "Key": "topic"
          }
        ]
      }
    }
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
