# ListPptTemplates - 查询PPT模板列表

查询PPT模板列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPptTemplates)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPptTemplates)

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

llm-xx

NextToken

string

否

下一页的 Token

+CBOXvu2YLxC6DOua8Qupg==

MaxResults

integer

否

最大返回结果数

暂不支持修改，固定为10

SceneId

integer

否

模板场景 ID

7

StyleId

integer

否

风格 id

1

ColourId

integer

否

颜色 ID

1

CareerId

integer

否

职业 ID

1

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Code

string

状态码

NoData

Current

integer

当前页码

1

Data

array<object>

业务数据

object

模板数据

Id

integer

ID

10

CoverImg

string

封面图

http://xxx.com/a.png

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

Size

integer

每页条数：默认 10

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

100

NextToken

string

下一页的 Token

+CBOXvu2YLxC6DOua8Qupg==

MaxResults

integer

最大返回结果数

10

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Current": 1,
  "Data": [
    {
      "Id": 10,
      "CoverImg": "http://xxx.com/a.png"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100,
  "NextToken": "+CBOXvu2YLxC6DOua8Qupg==",
  "MaxResults": 10
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListPptTemplates#workbench-doc-change-demo)。
