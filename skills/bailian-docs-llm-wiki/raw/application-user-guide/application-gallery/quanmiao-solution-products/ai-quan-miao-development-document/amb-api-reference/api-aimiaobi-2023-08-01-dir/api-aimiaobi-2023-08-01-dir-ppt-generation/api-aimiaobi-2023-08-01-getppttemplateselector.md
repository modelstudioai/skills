# GetPptTemplateSelector - 查询PPT模板筛选器

查询PPT模板筛选器

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetPptTemplateSelector)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetPptTemplateSelector)

## **授权信息**

当前API暂无授权信息透出。

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

WorkspaceId

string

否

业务空间 ID

lm-xxxx

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

xxxxx

Success

boolean

此次请求是否成功

Code

string

错误码

DataNotExists

Message

string

错误消息

错误消息

HttpStatusCode

integer

http 错误码

400

Data

object

响应对象

Colour

array<object>

颜色

object

Id

integer

颜色 ID

1

Name

string

颜色名称

橙色

Code

string

颜色值

#FCC462

SuitStyle

array<object>

风格

object

Id

integer

风格 ID

1

Title

string

风格名称

扁平简约

SuitScene

array<object>

场景

object

Id

integer

场景 ID

1

Title

string

场景名称

教育培训

Career

array<object>

职业

object

Id

integer

职业 ID

1

Name

string

职业名称

教育培训

IsHot

integer

高热度

0

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "Colour": [
      {
        "Id": 1,
        "Name": "橙色",
        "Code": "#FCC462"
      }
    ],
    "SuitStyle": [
      {
        "Id": 1,
        "Title": "扁平简约"
      }
    ],
    "SuitScene": [
      {
        "Id": 1,
        "Title": "教育培训"
      }
    ],
    "Career": [
      {
        "Id": 1,
        "Name": "教育培训",
        "IsHot": 0
      }
    ]
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

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetPptTemplateSelector#workbench-doc-change-demo)。
