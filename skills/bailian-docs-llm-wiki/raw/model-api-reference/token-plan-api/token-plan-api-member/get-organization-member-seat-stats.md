# 获取成员与席位统计

查询组织成员统计信息，包含成员总数、管理员数、普通成员数、已分配席位成员数、未分配席位成员数。

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `GET [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/member-seat-stats](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/member-seat-stats)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: GetOrganizationMemberSeatStats`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetOrganizationMemberSeatStats) 发起调用，可免去自行计算签名。
    

## 请求参数

该接口无请求参数。

## 返回参数

**参数**

**类型**

**描述**

OrgId

string

组织 ID

TotalMemberCount

integer

成员总数

OwnerRoleUserCount

integer

主账号数（ORG\_OWNER 角色）

AdminRoleUserCount

integer

管理员数（ORG\_ADMIN 角色）

MemberRoleUserCount

integer

普通成员数（ORG\_MEMBER 角色）

SeatedMemberCount

integer

已分配席位成员数

UnseatedMemberCount

integer

未分配席位成员数

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X GET "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/member-seat-stats" \
    --header "x-acs-action: GetOrganizationMemberSeatStats" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: 3e3b2a9f0c7d4f8e9a1b2c3d4e5f6a7b" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

## 返回示例

```
{
  "OrgId": "5ffd468b1e45db3c1cc26ad6",
  "TotalMemberCount": 12,
  "OwnerRoleUserCount": 1,
  "AdminRoleUserCount": 3,
  "MemberRoleUserCount": 8,
  "SeatedMemberCount": 2,
  "UnseatedMemberCount": 10
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
