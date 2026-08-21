# ListEnterprisePptTemplates - 查询企业专属PPT模板列表

查询企业专属PPT模板列表

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListEnterprisePptTemplates)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListEnterprisePptTemplates)

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

下一次请求需要的 token（暂未生效）

XXXX

MaxResults

integer

否

最大数量（暂未生效）

null

Skip

integer

否

要跳过的单个资源的数量（暂未生效）

10

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

文档

object

业务数据

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

数量

10

Success

boolean

是否成功：true 成功，false 失败

true

TotalCount

integer

总数

100

NextToken

string

下一次请求需要的 token（暂未生效）

CAESGgoSChAKDGNvbXBsZXRlVGltZRABCgQiAggAGAAiQAoJANEQ4AACjMDLgAAADFTNzMyZDMwMzAzMDM4NzA3MjZjN2E2NDYyNzUzODMxMzY3ODM0NmIzNTZkNjc=

MaxResults

integer

最大数量（暂未生效）

4

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
  "TotalCount": 100,
  "NextToken": "CAESGgoSChAKDGNvbXBsZXRlVGltZRABCgQiAggAGAAiQAoJANEQ4AACjMDLgAAADFTNzMyZDMwMzAzMDM4NzA3MjZjN2E2NDYyNzUzODMxMzY3ODM0NmIzNTZkNjc=",
  "MaxResults": 4
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListEnterprisePptTemplates#workbench-doc-change-demo)。
