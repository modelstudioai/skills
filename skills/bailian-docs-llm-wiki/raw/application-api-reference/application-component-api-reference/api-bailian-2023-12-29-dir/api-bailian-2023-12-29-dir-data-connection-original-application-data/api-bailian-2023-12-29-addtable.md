# AddTable - 添加表格

为表格数据连接器添加表格。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:AddTable 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/AddTable)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/AddTable)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
POST /{WorkspaceId}/datacenter/table HTTP/1.1
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

文件所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

TableName

string

是

表名。

ads\_wjjr\_basc\_enterprise\_di

ConnectorId

string

是

连接器 ID。

connector-d51861492df64257

TableColumns

array<object>

是

表格的列信息

object

是

单个列信息

ColumnName

string

是

列名称

column1

ColumnDesc

string

否

列描述

desc

DataType

string

是

数据类型

string

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码。

Index.Forbidden

Data

object

返回内容

TableId

string

表格 ID

table\_b6ddc67e7df14db38b74ef5e2e0fe24e\_12792097

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

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
    
-   false：失败。
    

True

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.Forbidden",
  "Data": {
    "TableId": "table_b6ddc67e7df14db38b74ef5e2e0fe24e_12792097"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddTable#workbench-doc-change-demo)。
