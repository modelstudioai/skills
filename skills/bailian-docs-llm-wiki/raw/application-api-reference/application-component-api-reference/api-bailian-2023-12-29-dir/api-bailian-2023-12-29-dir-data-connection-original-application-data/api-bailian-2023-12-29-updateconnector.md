# UpdateConnector - 编辑连接器

编辑连接器

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:UpdateConnector 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/UpdateConnector)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/UpdateConnector)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
PUT /{WorkspaceId}/datacenter/connector/{ConnectorId} HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

业务空间 ID

llm-3z7uw7fwz0vexxxx

ConnectorId

string

是

所属数据连接（Connector）的实例 id，请到百炼控制台获取。

conn\_xxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

ConnectorName

string

是

连接器名称

test-connector

Description

string

是

描述

never\_delete\_aeip\_95\_us-west-1

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码

Index.Forbidden

Data

object

接口业务数据字段

ConnectorId

string

连接器 id

conn\_file\_e0c9db4030b2465a9478028f7d76cd92\_1234

Message

string

错误信息

Required parameter(%s) missing or invalid, please check the request parameters.

RequestId

string

Id of the request

778C0B3B-03C1-5FC1-A947-36EDD13606AB

Status

string

接口返回的状态码

200

Success

boolean

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.Forbidden",
  "Data": {
    "ConnectorId": "conn_file_e0c9db4030b2465a9478028f7d76cd92_1234"
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "778C0B3B-03C1-5FC1-A947-36EDD13606AB",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/UpdateConnector#workbench-doc-change-demo)。
