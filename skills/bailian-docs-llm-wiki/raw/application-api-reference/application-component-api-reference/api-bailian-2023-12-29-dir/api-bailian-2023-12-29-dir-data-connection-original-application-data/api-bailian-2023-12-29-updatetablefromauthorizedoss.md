# UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格

使用已授权OSS Bucket中的文件更新阿里云百炼数据连接中表格连接器中的表格。

## 接口说明

-   请确保该 OSS Bucket 与阿里云百炼同属一个阿里云账号（主账号），并已按[从 OSS 导入数据配置说明](https://help.aliyun.com/zh/model-studio/data-import-instructions)完成授权。
    
    -   支持的 Bucket 存储类型不包括归档、冷归档或深度冷归档。支持内容加密的 Bucket。支持公共读写/公共读/私有的 Bucket。
        
    -   如需使用开启 [Referer 防盗链](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)的 Bucket，须参考[仅允许受信任的网站访问](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)将域名`*.console.aliyun.com`添加到白名单 Referer 中。
        
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:UpdateTableFromAuthorizedOss 权限点）并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/UpdateTableFromAuthorizedOss)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/UpdateTableFromAuthorizedOss)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
PUT /{WorkspaceId}/datacenter/table/fromoss/{TableId} HTTP/1.1
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

llm-3z7uw7fwz0vxxxx

TableId

string

是

更新的表格 ID

table\_100b51399c404966b7d49f71e388a3fd\_12738336

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

OssBucket

string

是

OSS Bucket 名称，详见[存储空间](https://help.aliyun.com/zh/oss/user-guide/oss-bucket-overview)。

yinghuo-ai

OssRegionId

string

是

OSS Bucket 的地域 ID。获取方式请参见 [OSS 地域和访问域名](https://help.aliyun.com/zh/oss/user-guide/regions-and-endpoints)。

cn-beijing

OssKey

string

是

导入文件在 OSS Bucket 中的键名（Key），详见[对象命名](https://help.aliyun.com/zh/oss/user-guide/object-naming-conventions)。

a0deedbce4a8162b8d66c63ace28330c

UpdateMode

string

是

更新模式，仅支持 APPEND（追加）和 OVERWRITE（覆盖）

OVERWRITE

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

DataCenter.FileTooLarge

Data

object

接口业务数据字段。

TableId

string

和入参 TableId 一致

table\_df96ebd5da8640e5a0991b3d15f39d4d\_12792097

Status

string

当前表格状态，一般上传之后会变成“TO\_IMPORT”，表示系统已经接收上传的文件，等待调度写入到数据表中

TO\_IMPORT

Message

string

错误信息

Required parameter(%s) missing or invalid, please check the request parameters.

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

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataCenter.FileTooLarge",
  "Data": {
    "TableId": "table_df96ebd5da8640e5a0991b3d15f39d4d_12792097",
    "Status": "TO_IMPORT"
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "7BA8ADD9-53D6-53F0-918F-A1E776AD230E",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/UpdateTableFromAuthorizedOss#workbench-doc-change-demo)。
