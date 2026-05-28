# GetConnector - 获取连接器信息

获取连接器信息。当前接口仅支持获取文件连接器信息。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:GetConnector 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)[阿里云百炼 SDK](https://api.alibabacloud.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/GetConnector)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/GetConnector)

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

sfm:GetConnector

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{WorkspaceId}/datacenter/connector HTTP/1.1
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

文件所属的业务空间 ID，获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)

llm-3z7uw7fwz0vxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

ConnectorName

string

否

查询的连接器名称，精确查询

连接器名称

ConnectorId

string

否

所属连接器 ID，请到[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)获取

conn\_file\_xxxx

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

success

Data

object

接口业务数据字段

ConnectorId

string

连接器 ID

conn\_file\_e0c9db4030b2465a9478028f7d76cd92\_1234

ConnectorName

string

连接器名称

name

ConnectorType

string

连接器类型

FILE

Description

string

连接器描述

Description

Message

string

错误信息

Requests throttling triggered.

RequestId

string

Id of the request

7BA8ADD9-53D6-53F0-918F-A1E776AD230E

Status

string

接口返回的状态码

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功
    
-   false：失败
    

True

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "success",
  "Data": {
    "ConnectorId": "conn_file_e0c9db4030b2465a9478028f7d76cd92_1234",
    "ConnectorName": "name",
    "ConnectorType": "FILE",
    "Description": "Description"
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "7BA8ADD9-53D6-53F0-918F-A1E776AD230E",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/GetConnector#workbench-doc-change-demo)。
