# 获取账号详情

获取TokenPlan账号详情及组织信息

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `GET [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/account](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/account)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: GetTokenPlanAccountDetail`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanAccountDetail) 发起调用，可免去自行计算签名。
    

在登录状态下，获取 TokenPlan 管理平台的账号信息

## 请求参数

该接口无请求参数。

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

AccountId

string

账号 ID

AccountType

string

账号类型：  
ALIYUN  
SSO  
SA

IsDeleted

boolean

账号全局状态：0=正常，1=已冻结

Name

string

账号显示名称

AliyunUid

string

阿里云 UID（ALIYUN 类型账号）

Email

string

邮箱（SSO 类型账号）

CreatedAt

string

创建时间

OrgMemberships

Array\[Object\]

组织成员关系列表（树形结构，组织 → 工作空间）

Array\[Object\]

OrgId

string

组织 ID

MemberStatus

string

组织成员状态  
ACTIVE  
INITIAL  
FROZEN

RoleId

string

组织角色 ID

RoleCode

string

组织角色编码  
ORG\_OWNER  
ORG\_ADMIN  
ORG\_MEMBER

Workspaces

Array\[Object\]

该组织下账号已加入的工作空间列表

object

工作空间列表。

WorkspaceId

string

工作空间 ID

MemberStatus

string

成员状态  
ACTIVE  
FROZEN

RoleId

string

工作空间角色 ID

RoleCode

string

工作空间角色编码  
WS\_ADMIN  
WS\_MEMBER

HttpStatusCode

integer

HTTP 状态码

RequestId

string

请求唯一标识

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X GET "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/account" \
    --header "x-acs-action: GetTokenPlanAccountDetail" \
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
    "AccountId": "acc_123456789",
    "AccountType": "ALIYUN",
    "IsDeleted": true,
    "Name": "test_name",
    "AliyunUid": "1122334455",
    "Email": "test@email.com",
    "CreatedAt": "Thu May 28 14:33:52 CST 2026",
    "OrgMemberships": [
      {
        "OrgId": "org_123456789",
        "MemberStatus": "ENABLE",
        "RoleId": "SYSTEM_ROLE_ORG_OWNER",
        "RoleCode": "ORG_MEMBER",
        "Workspaces": [
          {
            "WorkspaceId": "ws_123456789",
            "MemberStatus": "ACTIVE",
            "RoleId": "SYSTEM_ROLE_WS_ADMIN",
            "RoleCode": "WS_ADMIN"
          }
        ]
      }
    ]
  }
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
