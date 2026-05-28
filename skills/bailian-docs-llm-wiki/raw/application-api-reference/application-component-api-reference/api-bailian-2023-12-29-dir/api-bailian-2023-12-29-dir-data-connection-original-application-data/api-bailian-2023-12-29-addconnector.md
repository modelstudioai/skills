# AddConnector - 新增连接器

创建连接器，当前接口仅支持创建文件类型连接器。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:AddCategory 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/AddConnector)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/AddConnector)

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

sfm:AddConnector

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/datacenter/connector HTTP/1.1
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

知识库所在工作空间 ID

llm-3shx2gu255oxxxx

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

ConnectorType

string

是

连接器类型

FILE

Description

string

是

描述

文件连接器

FileConnectorConfig

object

否

文件连接器参数

RegionId

string

否

存储 bucket 区域

cn-hangzhou

BucketName

string

否

存储 bucket 名称

zyb-docker-registry-jn

StorageType

string

否

文件存储位置 OSS\_CUSTOM：使用自有 OSS 存储 OSS\_PLATFORM：使用平台 OSS 存储

OSS\_CUSTOM

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

Success

Data

object

接口业务数据字段

ConnectorId

string

连接器 ID

conn\_file\_e0c9db4030b2465a9478028f7d76cd92\_1234

Message

string

错误信息

Current file status does not support delete.

RequestId

string

Id of the request

35A267BF-FBFA-54DB-8394-AA3B0742D833

Status

string

接口返回的状态码

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功
    
-   false：失败
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Success",
  "Data": {
    "ConnectorId": "conn_file_e0c9db4030b2465a9478028f7d76cd92_1234"
  },
  "Message": "Current file status does not support delete.",
  "RequestId": "35A267BF-FBFA-54DB-8394-AA3B0742D833",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddConnector#workbench-doc-change-demo)。
