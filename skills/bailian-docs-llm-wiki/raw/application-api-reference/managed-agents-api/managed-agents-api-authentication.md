# 认证

Managed Agents API 的 API Key 获取与使用方式。

Managed Agents API 采用 **API Key** 鉴权。全部请求通过 HTTP Header 携带 API Key，一个 Key 可访问其归属工作空间下的全部资源：

```
Authorization: Bearer <your-api-key>
```

## 获取 API Key

1.  打开[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)，登录阿里云账号并开通百炼。
2.  在 **API Key** 页面创建并复制 API Key。

**警告**API Key 具有账号级权限，请妥善保管，不要在公开渠道分享或提交到代码仓库。

## 使用方式

将 API Key 配置为环境变量（例如 `DASHSCOPE_API_KEY`），每个请求携带 `Authorization` Header：

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 权限说明

-   **阿里云主账号**：可直接调用所有接口。
-   **RAM 子账号**：需获得相应权限授权后调用。
-   API Key 的权限范围由控制台配置。

**重要**配置完成后，从 [Agent 接口](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)开始调用。
