# OAuth 2.0 配置

Salesforce 与 MaxCompute 的 OAuth 2.0 凭证字段与获取路径。

2 个 App 使用 OAuth 2.0。控制台对这种方法的说明是：通过 OAuth 2.0 授权流程实现安全、用户友好的登录。

用户不把密码交给平台，而是跳转到对方系统登录并同意授权，平台拿到的是可撤销的令牌。

## 字段速查

App

必填字段

可选字段

Salesforce on Alibaba Cloud

组织域名、Client ID、Client Secret

—

MaxCompute

—

Scope

除此之外，每个配置都有共有的 **配置名称** 字段，见[创建身份验证配置](raw/application-user-guide/overview/auth-guide/create-config.md)。

## Salesforce on Alibaba Cloud

页面提示：请输入您的 Salesforce 组织域名和 OAuth 应用凭证。

字段

是否必填

说明

组织域名

是

你的 Salesforce on Alibaba Cloud 组织地址，形如 `xxx.my.salesforce.com`

Client ID

是

Salesforce External Client App 的 Consumer Key

Client Secret

是

Salesforce External Client App 的 Consumer Secret

凭证来自 Salesforce 侧的 External Client App。在 Salesforce 中创建 External Client App 并启用 OAuth 设置后，即可取到这两项，完整步骤见 Salesforce 官方文档 [Create an External Client App](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth_eca.htm)。

### 配置 OAuth

创建 External Client App 时，将 **Callback URL** 设置为：

```
https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback
```

**OAuth Scopes** 至少选择以下三项：

-   `Manage user data via APIs (api)`
-   `Manage user data via Web browsers (web)`
-   `Perform requests at any time (refresh_token, offline_access)`

**说明**组织域名要填你自己组织的地址，不是 `login.salesforce.com`。沙箱环境和生产环境的域名不同，注意不要填错。

## MaxCompute

页面提示：请输入授权范围（可选）。

字段

是否必填

说明

Scope

否

权限范围，不填则使用默认值

MaxCompute 是唯一不需要填任何凭证的 OAuth 2.0 配置，只有一个可选的授权范围。直接单击 **完成** 即可创建。

## 凭证轮转

对方系统里更换了 Client Secret 之后，原配置随之失效，基于它建立的连接会一并失败。

处理方式：新建一个身份验证配置填入新凭证，用新配置重建连接，确认可用后删除旧连接。

**警告**不要在对方系统删除仍在使用的 OAuth 应用。应用一删，所有基于它的连接立刻中断，且无法通过重新授权恢复。

## 授权失败排查

现象

常见原因

单击确定后没有跳转

浏览器拦截了弹窗，允许弹窗后重试

跳转后提示应用无效

Client ID 填错，或对方系统里的应用未启用

授权成功但工具调用失败

权限范围不足，或对方系统侧未开通对应 API

提示回调地址不匹配

对方系统的应用里没有登记平台的回调地址

**重要**只用一个 API Key 就能连的 App 见[API Key 配置](raw/application-user-guide/overview/auth-guide/api-key.md)，不需要去对方系统注册应用。
