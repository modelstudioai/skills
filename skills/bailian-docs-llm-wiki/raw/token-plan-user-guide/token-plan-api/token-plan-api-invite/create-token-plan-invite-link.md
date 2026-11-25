# 创建成员邀请链接

创建TokenPlan成员邀请链接

<a id="前提条件"></a>

<a id="tp7be3a608a2"></a>

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

<a id="请求说明"></a>

<a id="tpf6e464c622"></a>

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    | 地域 | Endpoint |
    | --- | --- |
    | 华北2（北京） | `POST https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/invite/link/create` |
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: CreateTokenPlanInviteLink`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/CreateTokenPlanInviteLink) 发起调用，可免去自行计算签名。
    

用户只允许拥有一个有效的邀请链接  
若用户已有有效的邀请链接，该接口将返回这个链接  
若需要创建新的链接，请调用 RevokeTokenPlanInviteLink 接口失效当前的链接  
该接口只返回生成的 token，邀请链接的拼接格式为 https://{host}/accept-invite?token=\[token\]&orgId=\[orgId\]  
国内站 host 为 tokenplan-enterprise.bailian.aliyunportal.com  
国际站 host 为 tokenplan-enterprise.modelstudio.aliyunportal.com

<a id="请求参数"></a>

<a id="tp9dfe10d203"></a>

## 请求参数

所有参数均通过 Query String 传递。

| 参数 | 类型 | 必选 | 描述 |
| --- | --- | --- | --- |
| ExpireType | string | 否 | 过期档位，默认 DAYS\_7<br>DAYS\_7<br>DAYS\_30<br>MONTHS\_6<br>YEAR\_1 |
| SsoSource | string | 是 | 邀请链接绑定的 SSO 登录方式:<br>SAML<br>DINGTALK |

<a id="返回参数"></a>

<a id="tp6573b7b0a6"></a>

## 返回参数

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| Success | boolean | 调用接口是否成功：<br>true：成功<br>false：失败 |
| Code | string | 响应状态码。 |
| Message | string | 响应信息。 |
| Data | object | 业务参数 |
| Token | string | 生成的 Token |

<a id="请求示例"></a>

<a id="tpabfacbf531"></a>

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

<a id="code-block"></a>

```bash
curl -X POST "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/invite/link/create?ExpireType=DAYS_7&SsoSource=SAML" \
    --header "x-acs-action: CreateTokenPlanInviteLink" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: ${SIGNATURE_NONCE}" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

<a id="返回示例"></a>

<a id="tpa837cbf059"></a>

## 返回示例

<a id="code-block-2"></a>

```json
{
  "Success": true,
  "Data": {
    "Token": "sk-ws-D.****.*******"
  }
}
```

<a id="错误码"></a>

<a id="tp70e3349b1e"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../../../model-api-reference/preparations/error-code.md)。
