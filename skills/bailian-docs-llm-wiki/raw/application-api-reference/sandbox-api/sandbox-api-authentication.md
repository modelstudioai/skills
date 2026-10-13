# 认证

Sandbox API 的 API Key 获取与 E2B SDK 配置。

Sandbox API 采用 **API Key** 鉴权。管控面请求通过 HTTP Header 携带阿里云百炼 API Key：

```
Authorization: Bearer <your-api-key>
```

使用 E2B SDK 时，SDK 必填的 `X-API-Key` / `api_key` 仅用于满足 E2B 协议格式，阿里云百炼侧不使用它做业务鉴权。推荐填写 `e2b_${ALIYUN_UID}`。

**说明**兼容 E2B 协议的接口返回体贴近 E2B 原生响应结构，不封装为阿里云百炼统一 `Result<T>` 结构。

## 获取 API Key

1.  打开[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)，登录阿里云账号并开通百炼。
2.  在 **API Key** 页面创建并复制 API Key。

**警告**API Key 具有账号级权限，请妥善保管，不要在公开渠道分享或提交到代码仓库。

**重要**配置完成后，从[创建实例](raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)开始调用。
