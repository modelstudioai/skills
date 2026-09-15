# GenerateFileUploadParams

获取文件上传信息

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

bailianvoicebot:GenerateFileUploadParams

update

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

BusinessUnitId

string

否

百炼业务空间 ID

llm-c11iig67g863rih8

FileName

string

否

文件名

test.wav

BusinessType

string

否

文件类型

**枚举值：**

-   Vocabulary :
    
    Vocabulary
    
-   CloneVoice :
    
    CloneVoice
    

CloneVoice

## 返回参数

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

内部错误码

OK

HttpStatusCode

integer

http 状态码

200

Message

string

错误信息

Instance llm-xdne77rxe14ziszr does not exist.

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

Data

object

文件上传参数

Signature

string

根据 AccessKey Secret 和 Policy 计算出的签名信息。调用 OSS API 时，OSS 验证该签名信息，从而确认 Post 请求的合法性。

YOUR\_SIGNATURE

Policy

string

OSS 通过该参数验证请求表单域的合法性

eyJleHBpcmF0aW9uIjoiMjAyNi0wMy0yOVQxMzoyNDoyNi4yMDNaIiwiY29uZGl0aW9ucyI6W239

AccessKeyId

string

签名使用的 AccessKeyId。

YOUR\_ACCESS\_KEY\_ID

Host

string

OSS 的接入域名。

[http://cab.oss-cn-hangzhou.aliyuncs.com](http://cab.oss-cn-hangzhou.aliyuncs.com)

FileKey

string

上传文件路径

vocabulary/B678CA67-C8CB-150C-AD7F-6FA7F0A811BA\_热词导入模版 (7).zip

ExpirationTime

integer

上传有效期

1774794266093

SecurityToken

string

安全 token

YOUR\_SECURITY\_TOKEN

AccessKeySecret

string

Oss 授权上传文件的 Secret。

YOUR\_ACCESS\_KEY\_SECRET

Bucket

string

OSS 文件保存桶名称。

cab

Region

string

地域

cn-hangzhou

Params

array

动态错误参数列表

string

动态错误参数

llm-xdne77rxe14ziszr

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-xdne77rxe14ziszr\n does not exist.",
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "Signature": "YOUR_SIGNATURE",
    "Policy": "eyJleHBpcmF0aW9uIjoiMjAyNi0wMy0yOVQxMzoyNDoyNi4yMDNaIiwiY29uZGl0aW9ucyI6W239",
    "AccessKeyId": "YOUR_ACCESS_KEY_ID",
    "Host": "http://cab.oss-cn-hangzhou.aliyuncs.com",
    "FileKey": "vocabulary/B678CA67-C8CB-150C-AD7F-6FA7F0A811BA_热词导入模版 (7).zip",
    "ExpirationTime": 1774794266093,
    "SecurityToken": "YOUR_SECURITY_TOKEN",
    "AccessKeySecret": "YOUR_ACCESS_KEY_SECRET",
    "Bucket": "cab",
    "Region": "cn-hangzhou"
  },
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode)查看更多错误码。

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GenerateFileUploadParams#workbench-doc-change-demo)。
