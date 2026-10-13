# 认证

Security API 的 API Key 获取与使用方式。

Security API 采用 **API Key** 鉴权。全部请求通过 HTTP Header 携带阿里云百炼 API Key：

```
Authorization: Bearer <your-api-key>
```

## 获取 API Key

1.  打开[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)，登录阿里云账号并开通百炼。
2.  在 **API Key** 页面创建并复制 API Key。

**警告**API Key 具有账号级权限，请妥善保管，不要在公开渠道分享或提交到代码仓库。

**重要**配置完成后，从[查询 Agent 资产](raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)开始调用。
