# API 概览

ParseX API 概览。

通过ParseX API，你可以以编程方式进行文档解析&信息抽取。所有接口通过 DashScope 网关提供服务。

<a id="服务地址"></a>

## 服务地址

<a id="code-block"></a>

```bash
https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x
```

所有接口使用统一的服务地址，路径前缀为 `/api/v2/apps/parse-x`。

<a id="协议约定"></a>

## 协议约定

-   所有接口均通过 **HTTPS** 访问，不支持 HTTP。
-   请求体和响应体均为 **JSON** 格式，字符集 **UTF-8。**
-   所有接口均使用 `POST` 方法。

<a id="认证与请求头"></a>

## 认证与请求头

| Header | 必填 | 说明 |
| --- | --- | --- |
| `Authorization` | 是 | `Bearer $DASHSCOPE_API_KEY`，获取方式见[**鉴权**](api-overview/authentication.md) |
| `Content-Type` | 是 | `application/json` |

<a id="通用响应格式"></a>

## 通用响应格式

所有接口返回统一的 JSON 结构。

<a id="成功响应"></a>

### 成功响应：

<a id="code-block-2"></a>

```json
{
  "request_id": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "data": {
    "biz_id": "parseX-video-20260911-c954ec4fc32e4bc3a8cfda61841e4f19"
  }
}
```

<a id="失败响应"></a>

### 失败响应：

<a id="code-block-3"></a>

```json
{
  "code": "InvalidParameter",
  "message": "The biz_id must be provided.",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

<a id="异步调用流程"></a>

## 异步调用流程

正式入口发布后，提交接口返回 `biz_id`，调用方使用该 ID 调用对应的结果接口，直到 `data.status` 为 `success` 或 `failed`。

<a id="code-block-4"></a>

```text
graph LR
  A[提交任务] --> B[获得 biz_id]
  B --> C[调用结果接口]
  C --> D{data.status}
  D -->|processing| C
  D -->|success| E[读取结果]
  D -->|failed| F[按错误信息处理]
```

-   [提交解析任务](api-overview/document-parsing/parse-submit.md)：提交文档或音视频解析任务，返回 biz\_id 用于异步查询。
-   [提交抽取任务](api-overview/field-extraction/extract-submit.md)：按 JSON Schema 提交结构化信息抽取任务。
-   [错误码](api-overview/errors.md)：查看错误响应格式与公开错误码。
