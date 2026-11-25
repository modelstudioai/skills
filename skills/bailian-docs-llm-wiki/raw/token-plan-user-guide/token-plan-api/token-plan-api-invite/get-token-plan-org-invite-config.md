# 获取邀请配置

获取TokenPlan成员邀请配置

<a id="前提条件"></a>

<a id="tpac8f9a253b"></a>

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

<a id="请求说明"></a>

<a id="tpf81267acc1"></a>

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    | 地域 | Endpoint |
    | --- | --- |
    | 华北2（北京） | `GET https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/invite/config/get` |
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: GetTokenPlanOrgInviteConfig`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanOrgInviteConfig) 发起调用，可免去自行计算签名。
    

<a id="请求参数"></a>

<a id="tp6828d52698"></a>

## 请求参数

该接口无请求参数。

<a id="返回参数"></a>

<a id="tp6cf4b5341d"></a>

## 返回参数

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| Success | boolean | 调用接口是否成功：<br>true：成功<br>false：失败 |
| Code | string | 响应状态码。 |
| Message | string | 响应信息。 |
| Data | object | 当前分类统计的数据结果 |
| OrgId | string | 组织 ID |
| DefaultRoleId | string | 默认分配的组织角色 ID<br>SYSTEM\_ROLE\_ORG\_ADMIN<br>SYSTEM\_ROLE\_ORG\_MEMBER |
| SeatAssignStrategy | string | 默认的席位分配策略：<br>HIGH\_TO\_LOW<br>LOW\_TO\_HIGH<br>NONE |

<a id="请求示例"></a>

<a id="tp0b3a7e72ba"></a>

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

<a id="code-block"></a>

```bash
curl -X GET "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/invite/config/get" \
    --header "x-acs-action: GetTokenPlanOrgInviteConfig" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: ${SIGNATURE_NONCE}" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

<a id="返回示例"></a>

<a id="tpe472652d85"></a>

## 返回示例

<a id="code-block-2"></a>

```json
{
  "Success": true,
  "Data": {
    "OrgId": "org_123456789",
    "DefaultRoleId": "ORG_MEMBER",
    "SeatAssignStrategy": "NONE"
  }
}
```

<a id="错误码"></a>

<a id="tpa2b9c371de"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../../../model-api-reference/preparations/error-code.md)。
