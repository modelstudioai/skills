# SaveOrUpdateOssConfig - 配置-云存储-参数配置

配置-云存储-参数配置

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveOrUpdateOssConfig)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveOrUpdateOssConfig)

## **授权信息**

当前API暂无授权信息透出。

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

BucketName

string

否

oss 的 bucketName

xxx

EndPoint

string

否

oss 的 endPoint

oss-cn-shanghai.aliyuncs.com

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

状态码

DataNotExists

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

Id of the request

F2F366D6-E9FE-1006-BB70-2C650896AAB5

Success

boolean

是否成功：true 成功，false 失败

true

Data

object

业务数据

BucketName

string

oss 的 bucketname

xxx

Endpoint

string

oss 的 endpoint

oss-cn-shanghai.aliyuncs.com

Enable

string

oss 配置是否可用：1 可用，0 不可用

1

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "Success": true,
  "Data": {
    "BucketName": "xxx",
    "Endpoint": "oss-cn-shanghai.aliyuncs.com",
    "Enable": "1"
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SaveOrUpdateOssConfig#workbench-doc-change-demo)。
