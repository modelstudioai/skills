# 修改组织信息

修改指定组织的名称等基本信息。

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `POST [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: UpdateOrganization`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/UpdateOrganization) 发起调用，可免去自行计算签名。
    

## 请求参数

所有参数均通过 Query String 传递。

**参数**

**类型**

**必选**

**描述**

Name

string

否

组织名称

Description

string

否

组织描述

## 返回参数

**参数**

**类型**

**描述**

Success

boolean

调用接口是否成功：  
true：成功  
false：失败

Code

string

响应状态码。

Message

string

响应信息。

Data

object

业务数据

OrgId

string

组织 ID

NamespaceId

string

产品命名空间 ID

Name

string

组织名称

Description

string

组织描述

Status

string

状态  
ACTIVE  
FROZEN

OwnerId

string

组织 Owner 的 UAC 账号 ID

OwnerBizAccountId

string

组织 Owner 的业务账号标识（ALIYUN 类型为 aliyunUid，SSO 类型为 userIdentifier）

GmtCreate

string

创建时间

GmtModified

string

修改时间

HttpStatusCode

integer

HTTP 状态码

RequestId

string

请求唯一标识

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。示例 URL 中的中文取值为便于阅读未做编码；实际计算签名时，规范化请求（CanonicalRequest）的 Query String 需按 RFC 3986 对键和取值做百分号编码，否则会返回 `SignatureDoesNotMatch`。使用阿里云 SDK 时会自动处理。

```
curl -X POST "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization?Name=新的组织名称&Description=新的组织描述" \
    --header "x-acs-action: UpdateOrganization" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: 3e3b2a9f0c7d4f8e9a1b2c3d4e5f6a7b" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

## 返回示例

```
{
  "Success": true,
  "Data": {
    "OrgId": "org_123456789",
    "NamespaceId": "namespace-1",
    "Name": "组织名称",
    "Description": "组织描述",
    "Status": "ACTIVE",
    "OwnerId": "acc_123456789",
    "OwnerBizAccountId": "1269388320468566",
    "GmtCreate": "2025-12-11T02:19:27Z",
    "GmtModified": "2025-07-08 13:59:11"
  }
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
