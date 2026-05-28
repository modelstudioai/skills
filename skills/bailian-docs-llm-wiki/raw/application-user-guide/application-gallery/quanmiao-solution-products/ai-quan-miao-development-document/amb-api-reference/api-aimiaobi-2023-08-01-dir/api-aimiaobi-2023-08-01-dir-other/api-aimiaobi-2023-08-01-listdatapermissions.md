# ListDataPermissions - 权限-列表

权限-列表 - 数据集

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDataPermissions)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDataPermissions)

## **授权信息**

当前API暂无授权信息透出。

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/use-workspace)

llm-xx

DataType

string

否

数据类型：

-   dataset：数据集
    

dataset

DataId

string

否

数据权限数据唯一标识

-   dataset：SystemSearch.QuarkCommonNews
    

SystemSearch.QuarkCommonNews

PageSize

integer

否

每页条数

10

PageNumber

integer

否

当前页：默认 1

1

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

Data

array<object>

业务数据

object

业务数据

Id

integer

主键 ID

1

CreateUser

string

创建者

xxx

CreateTime

string

创建时间

2024-11-12 21:46:24

UserId

string

有权限用户唯一标识

CustomSemanticSearch

Username

string

有权限用户名称

xxx

DataType

string

数据类型：

-   dataset：数据集
    

xxx

DataId

string

数据权限数据唯一标识

-   dataset：SystemSearch.QuarkCommonNews
    

SystemSearch.QuarkCommonNews

Permission

string

权限定义：默认只读 read

read

PageNumber

integer

当前页码

1

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

Code

string

状态码

NoData

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

TotalCount

integer

总条数

100

PageSize

integer

每页条数

10

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": [
    {
      "Id": 1,
      "CreateUser": "xxx",
      "CreateTime": "2024-11-12 21:46:24",
      "UserId": "CustomSemanticSearch",
      "Username": "xxx",
      "DataType": "xxx",
      "DataId": "SystemSearch.QuarkCommonNews\n",
      "Permission": "read"
    }
  ],
  "PageNumber": 1,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "TotalCount": 100,
  "PageSize": 10
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDataPermissions#workbench-doc-change-demo)。
