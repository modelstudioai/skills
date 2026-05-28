# GenerateUploadConfig - 生成上传配置

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

## 接口说明

通过这接口可以拿到文件上传的地址和凭证，参考如下文档可以完成文件上传： [OSS-表单上传](https://help.aliyun.com/zh/oss/user-guide/form-upload)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GenerateUploadConfig)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GenerateUploadConfig)

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

aimiaobi:GenerateUploadConfig

create

\*全部资源

`*`

无

无

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

FileName

string

否

文件名称

test.docx

ParentDir

string

是

父目录：

-   materialDocument: 妙笔-素材库
    
-   datasetUpload: 妙搜-数据集
    
-   intervenes：干预
    
-   temp: 临时上传目录(周期释放)
    

dataset

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

PlainResult

Code

string

状态码

successful

Data

object

业务数据

FileKey

string

文件唯一标识：可以当做 url 给到全妙

oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx

FormDatas

object

上传 oss 的凭证信息：

```
{
  "OSSAccessKeyId": "xxx",
  "Signature": "xxx+xxx=",
  "MaxSize": 31457280,
  "key": "aimiaobi/dataset/2_2/xx.txt",
  "policy": "xxx=="
}
```

string

PostUrl

string

上传 oss 的地址（妙笔自有的 OSS 域名，固定是：https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/）

https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 执行文件上传

拿到 PostUrl（妙笔官方 OSS） 、FormDatas （OSS 的临时鉴权）两个参数之后，需要手动上传 到 OSS 中。

**说明**

此步骤是核心上传步骤，一定要执行。 执行上传完毕之后：fileKey 即可用于其他接口。

示例请求 CURL 为：

**说明**

注意：此示例仅为 简单的 CURL 示例，具体 SDK 对接流程一般使用 **代码编写方式** 发起表单的文件上传。

```
curl -X POST --location "${PostUrl}" \
    -H "Content-Type: multipart/form-data; boundary=WebKitFormBoundarykFF1FqdGZn2nxzfb" \
    -F "key=${key};type=*/*" \
    -F "OSSAccessKeyId=${OSSAccessKeyId};type=*/*" \
    -F "Signature=${Signature};type=*/*" \
    -F "policy=${policy};type=*/*" \
    -F "file=@/Users/xxxx/xxx.text;filename=xxx.text;type=text/plain"
```

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "FileKey": "oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx",
    "FormDatas": {
      "key": ""
    },
    "PostUrl": "https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/"
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GenerateUploadConfig#workbench-doc-change-demo)。
