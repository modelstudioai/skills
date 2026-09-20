# OSS 托管使用

ParseX 中OSS 托管使用方式，STS Token 接入。

## 概述

### 什么是 OSS 托管

OSS 托管方案允许客户把文档的处理结果落到**客户自己名下的 OSS Bucket** 中，而非服务侧存储。适合对数据有隐私、合规、权限管控要求的场景：

-   **结果不出客户侧**：解析/抽取结果直接写入客户的 OSS 空间，便于客户做后续业务处理与权限控制。
-   **细粒度权限管控**：客户可对源文件目录、结果目录分别授权，实现最小权限。
-   **避免二次转存成本**：客户无需再从服务侧下载结果后自行转存。

### 接入方式说明（重要）

维度

当前方案（parse-x 接口）

鉴权方式

**不支持角色信任**，需要客户直接把 OSS 的 STS 临时凭证（或 RAM 用户 AK）随请求传入

传入字段

`output.oss_config` 中的 `bucket` / `endpoint` / `access_key_id` / `access_key_secret` / `security_token`

结果写入

服务端直接使用客户传入的 STS 凭证写 OSS

**因此，使用当前 parse-x 接口接入 OSS 托管时，客户必须自行获取一组可访问目标 OSS Bucket 的 STS 临时凭证（或 RAM 用户 AK），并在每次提交/查询时随请求传入。**

* * *

## 前置准备

### 创建 RAM 用户（或 RAM 角色）

登录 [RAM 控制台](https://ram.console.aliyun.com/)，选择「身份管理 → 用户」（或「角色」），创建用于访问 OSS 的身份：

-   若使用**长期 AccessKey**：创建 RAM 用户，并为其生成 AccessKey ID / AccessKey Secret（`security_token` 留空即可）。
-   若使用**STS 临时凭证（推荐）**：创建 RAM 角色，后续通过 `AssumeRole` 接口换取临时凭证（含 `security_token`）。

### 创建最小权限授权策略

在「权限管理 → 权限策略 → 创建权限策略」中，使用脚本编辑方式，配置如下最小权限（示例策略名 `testParseXAccessOss`）：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:GetObject"
      ],
      "Resource": "acs:oss:*:*:[your-bucket-name]/[your-source-directory]/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:PutObject",
        "oss:GetObject"
      ],
      "Resource": "acs:oss:*:*:[your-bucket-name]/[your-result-directory]/*"
    }
  ]
}
```

字段说明：

权限

用途

说明

`oss:GetObject`（源目录）

读取源文件

当源文件采用客户 OSS 签名 URL（`file_url` 指向客户 OSS 对象）时，需要该权限

`oss:PutObject`（结果目录）

写入解析结果

服务将结果写入客户 OSS 的指定目录时必需

`oss:GetObject`（结果目录）

读取结果

查询接口返回结果 URL / 生成签名 URL 时必需

> 请将 `[your-bucket-name]`、`[your-source-directory]`、`[your-result-directory]` 替换为客户实际 Bucket 与目录。若希望简化，也可将 `Resource` 放宽为 `acs:oss:*:*:[your-bucket-name]/*`，但出于安全建议保持目录级最小授权。

### 将策略授权给 RAM 用户 / 角色

创建策略后，进入对应 RAM 用户（或角色）的「权限管理 → 新增授权」，选择刚创建的策略（资源范围选择「账号级别」）完成授权。

### 获取 STS 临时凭证（推荐）

通过 STS `AssumeRole` 接口，使用上述 RAM 角色的 ARN 换取临时凭证：

```
请求：sts.aliyuncs.com  -  Action: AssumeRole
      RoleArn        : acs:ram::{account-id}:role/{role-name}
      RoleSessionName: parse-x-oss-access
返回：AccessKeyId / AccessKeySecret / SecurityToken / Expiration
```

将返回的三个字段分别填入请求中的 `access_key_id`、`access_key_secret`、`security_token`。

> -   若使用 RAM 用户长期 AK，则只填 `access_key_id`、`access_key_secret`，`security_token` 可省略。
> -   STS 临时凭证存在有效期（`Expiration`），请确保在调用期间凭证未过期；过期后需重新换取。

* * *

## 调用说明

### API 端点与鉴权

环境

地址

预发

`https://{workspace}.cn-beijing.pre-maas.aliyuncs.com/api/v2/apps/pre-parse-x/{端点}`

正式

`https://{workspace}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/{端点}`

### 提交&查询解析任务 `/parse/submit` 、`/parse/result`

​调用前请确保已获取 API Key，详见[提交解析任务](raw/application-api-reference/overview/document-parsing/parse-submit.md)、[查询解析任务](raw/application-api-reference/overview/document-parsing/parse-result.md)。

字段说明（`output.oss_config`）：

字段

类型

必填

说明

`bucket`

string

是

客户 OSS Bucket 名称

`endpoint`

string

是

OSS Endpoint，如 `oss-cn-hangzhou.aliyuncs.com`

`access_key_id`

string

是

STS 临时凭证或 RAM 用户 AK ID

`access_key_secret`

string

是

对应 Secret

`security_token`

string

否

STS 临时凭证的 SecurityToken；使用长期 AK 时省略

### 抽取任务 `/extract/submit` 与 `/extract/result`

​调用前请确保已获取 API Key，详见[提交解析任务](raw/application-api-reference/overview/field-extraction/extract-submit.md)、[查询解析任务](raw/application-api-reference/overview/field-extraction/extract-result.md)。

字段说明（`output.oss_config`）：

字段

类型

必填

说明

`bucket`

string

是

客户 OSS Bucket 名称

`endpoint`

string

是

OSS Endpoint，如 `oss-cn-hangzhou.aliyuncs.com`

`access_key_id`

string

是

STS 临时凭证或 RAM 用户 AK ID

`access_key_secret`

string

是

对应 Secret

`security_token`

string

否

STS 临时凭证的 SecurityToken；使用长期 AK 时省略

* * *

## OSS 侧配置要求与常见异常排查

> 以下均为「客户 OSS 自身配置」导致「服务使用客户 STS 凭证调用失败」的常见场景。排查时请以最终报错为准，逐一核对。

### 权限不足（AccessDenied / HTTP 403）

**现象**：返回 `FileDownloadFailed`（下载失败）或 `CustomerOssWriteFailed`（写入客户 OSS 失败），或 OSS 侧报 `AccessDenied`。

**原因**：STS 凭证所属的 RAM 用户/角色未授权 `oss:GetObject`（源目录）或 `oss:PutObject`（结果目录），或 `Resource` 路径配置与实际目录不一致。

**处理**：按第 2.2 节核对授权策略，确认 `Action` 与 `Resource`（含末尾 `/*`）覆盖实际读写路径。

### 阻止公共访问（Block Public Access）

相关文档：[阻止公共访问](https://help.aliyun.com/zh/oss/user-guide/block-public-access)

**现象**：服务使用 STS 凭证访问客户 Bucket 时被拒绝（403 Forbidden），即使凭证本身有效。

**原因**：客户在 Bucket 或账号级别开启了「阻止公共访问」，会拦截来自公网/非受信条件的访问请求，可能连带影响授权访问。

**处理**：

-   若必须开启「阻止公共访问」，请确认已放行解析服务的访问来源，或改用同地域**内网 Endpoint**（如 `oss-cn-hangzhou-internal.aliyuncs.com`，需与访问来源同 Region）。
-   如非必需，可临时关闭该功能以验证是否为拦截根因。

### 防盗链（Referer 校验）

相关文档：[防盗链](https://help.aliyun.com/zh/oss/user-guide/hotlink-protection)

**现象**：服务以 SDK 方式（无 `Referer` 头）读写客户 Bucket 时被拒（403）。

**原因**：客户开启了 OSS 防盗链，并设置了 Referer 白名单 / 勾选了「不允许空 Referer」。服务端 SDK 请求通常不携带 `Referer` 头，会被判定为非法来源而拒绝。

**处理**：

-   在防盗链配置中**允许空 Referer**（勾选允许），或将服务端请求来源加入白名单。
-   若必须启用防盗链，请确认服务端 SDK 请求不会被 Referer 校验拦截。

### 跨域资源共享（CORS）

相关文档：[跨域资源共享](https://help.aliyun.com/zh/oss/user-guide/configure-cross-origin-resource-sharing)

**现象**：结果 URL 无法在浏览器端直接访问（浏览器报 CORS 跨域错误）；服务端读写本身**不受 CORS 影响**。

**原因**：CORS 只约束浏览器端跨域请求。若客户的前端直接（不经服务端代理）访问结果 URL，而 Bucket 未配置 CORS 规则，浏览器会拦截。

**处理**：若需要浏览器端直接访问结果，请在 OSS「数据安全 → 跨域设置」中配置 CORS 规则（允许的来源 Origin、方法 GET/PUT、需暴露的响应头）。

### Bucket Policy / 授权策略

**现象**：STS 凭证有效，但访问仍被拒（403）。

**原因**：客户 Bucket 上配置了 Bucket Policy（授权策略），显式 `Deny` 了服务端或 STS 主体的访问，或限制了访问来源。

**处理**：核对 Bucket 的「权限管理 → 授权策略」，确认没有 `Deny` 语句阻断服务访问。

### STS 凭证过期 / Endpoint 不匹配

**现象**：返回鉴权失败或 403。

**原因**：

-   STS 临时凭证已过 `Expiration` 有效期，或 `security_token` 与 `access_key_id` 不匹配。
-   `endpoint` 与 Bucket 实际 Region 不一致（如 Bucket 在 `cn-shanghai`，endpoint 却填 `oss-cn-hangzhou.aliyuncs.com`）。

**处理**：重新获取未过期的 STS 凭证；确认 `endpoint` 与 Bucket 所在 Region 一致。

### 排查清单

序号

检查项

处理

1

RAM/Bucket 权限是否覆盖 `GetObject` / `PutObject`

核对策略 Action 与 Resource 路径

2

是否开启「阻止公共访问」

放行来源或改用内网 Endpoint / 临时关闭验证

3

是否开启「防盗链」且不允许空 Referer

允许空 Referer 或将来源加入白名单

4

是否需要浏览器端直接访问结果

配置 CORS 规则

5

Bucket Policy 是否含 Deny 语句

移除或调整 Deny

6

STS 凭证是否过期 / token 与 ak 是否匹配

重新换取凭证

7

endpoint 是否与 Bucket Region 一致

修正 endpoint

* * *

## 错误码对照

枚举常量

HTTP

业务码

说明

英文 message

`OSS_NOSUCKKEY_ERROR`

400

32001

OSS 中未能匹配到的目标文件

Target file that could not be matched in OSS.

`OSS_INVALIDACCESSKEYID_ERROR`

400

32002

提供的 OSS Access Key Id 不存在

The OSS Access Key Id you provided does not exist in our records.

`OSS_SIGNATUREDOESNOTMATCH_ERROR`

400

32003

请求签名校验不匹配

The request signature we calculated does not match the signature you provided. Check your key and signing method.

`OSS_INVALIDSECURITYTOKEN_ERROR`

400

32004

提供的 Security Token 无效

The security token you provided is invalid.

`OSS_ACCESSDENIED_ERROR`

400

32005

因 Bucket ACL 无权访问该对象

You have no right to access this object because of bucket acl.

`OSS_CHECK_ERROR`

400

32006

OSS 校验失败

oss check fail.

`OSS_NoSuchBucket_ERROR`

400

32007

指定的 Bucket 不存在

The specified bucket does not exist.

`OSS_AccessForbidden_ERROR`

400

32008

访问被禁止

AccessForbidden

* * *

## 注意事项与最佳实践

1.  **凭证安全**：STS 临时凭证有有效期，请勿硬编码长期 AK；推荐使用 STS `AssumeRole` 动态换取，控制有效期为任务所需最短时间。
2.  **最小权限**：仅授予源目录 `GetObject`、结果目录 `PutObject` + `GetObject`，避免全 Bucket 授权。
3.  **Endpoint 选择**： 实际以服务提供endpoint为准：

-   公网 Endpoint（`oss-cn-hangzhou.aliyuncs.com`）通用，但流量走公网。
-   内网 Endpoint（`oss-cn-hangzhou-internal.aliyuncs.com`）需与访问来源同 Region，可保证「不出公网」。

4.  **结果目录**：结果写入的具体前缀由服务侧约定，请保证策略中的结果目录 `Resource` 能覆盖该前缀。
5.  **源文件隐私**：如源文件也需要「不出公网」，可以客户自身 OSS 签名 URL 作为 `file_url` 传入（带有效期），避免源文件对外永久公开。
