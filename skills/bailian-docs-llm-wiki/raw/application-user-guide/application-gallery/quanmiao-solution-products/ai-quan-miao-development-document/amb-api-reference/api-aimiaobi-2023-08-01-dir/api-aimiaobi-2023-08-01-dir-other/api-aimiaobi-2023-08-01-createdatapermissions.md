# CreateDataPermissions - 权限-批量添加

权限-批量添加： - 数据集权限：

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateDataPermissions)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateDataPermissions)

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

llm-xxx

DataType

string

是

权限类型：目前支持：dataset

dataset

DataId

string

是

权限唯一标识：

SystemSearch.QuarkCommonNews

PermissionUserInfos

array<object>

是

分配权限的用户

object

否

用户

PermissionUserId

string

是

用户 id：

-   ram 子账号：账号 aliuid
    
-   角色用户：AssumedRoleUser${roleId}
    

1

PermissionUsername

string

否

用户名称

xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应结果

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

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/CreateDataPermissions#workbench-doc-change-demo)。
