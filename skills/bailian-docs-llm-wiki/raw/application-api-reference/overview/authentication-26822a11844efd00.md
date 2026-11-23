# Skill API 认证

Skill API 使用百炼 API Key 鉴权，并通过工作空间 Endpoint 访问。

Skill API 使用阿里云百炼 API Key 鉴权。每个请求通过 HTTP Header 携带 API Key。

## 获取 API Key

1.  登录[阿里云百炼控制台](https://bailian.console.aliyun.com/)。
2.  前往 [API Key 页面](raw/model-api-reference/preparations/get-api-key.md)，创建并复制 API Key。

**警告**API Key 具有访问百炼资源的权限。请妥善保管，不要写入代码仓库或公开渠道。

## 配置 Endpoint

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills
```

-   `workspace_id`：工作空间 ID。登录百炼控制台后，在右上角工作空间菜单中复制。

## 发起请求

将 API Key 配置到环境变量：

```
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

每个请求携带 `Authorization` Header：

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills?pageNo=1&pageSize=10" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 权限说明

-   阿里云主账号可直接调用全部接口。
-   RAM 子账号需要获得对应权限授权。
-   API Key 的权限范围由控制台配置决定。

**说明**身份信息缺失或无效时，接口返回 `401` `WORKSPACE_ID_ILLEGAL`。错误处理见[Skill API 错误码](raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)。
