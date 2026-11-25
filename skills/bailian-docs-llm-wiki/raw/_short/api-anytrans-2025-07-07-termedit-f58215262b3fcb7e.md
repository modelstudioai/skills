# TermEdit - 术语库编辑

通义多模态翻译术语库编辑

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/TermEdit)

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>anytrans:TermEdit</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /anytrans/translate/intervene/edit HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>当前请求所使用的百炼业务空间 id</p></div></td><td>llm-kqtrcpdee4xm29xx</td></tr><tr><td>action</td><td>string</td><td>是</td><td><div><p>操作类型</p></div><div><div>枚举值：</div><ul><li>ADD：新增。</li><li>DELETE：删除。</li><li>MODIFY：修改。</li></ul></div></td><td>ADD</td></tr><tr><td>sourceLanguage</td><td>string</td><td>是</td><td><div><p>源语言</p></div></td><td>en</td></tr><tr><td>targetLanguage</td><td>string</td><td>是</td><td><div><p>目标语言</p></div></td><td>zh</td></tr><tr><td>scene</td><td>string</td><td>是</td><td><div><p>模型类型</p></div><div><div>枚举值：</div><ul><li>mt-plus：专业版。</li><li>mt-flash：轻量版。</li></ul></div></td><td>mt-flash</td></tr><tr><td>ext</td><td>object</td><td>是</td><td><div><p>扩展参数</p></div></td><td></td></tr><tr><td>terms</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>干预术语列表</p></div></td><td></td></tr><tr><td></td><td>object</td><td>是</td><td><div><p>干预术语</p></div></td><td></td></tr><tr><td>termId</td><td>string</td><td>否</td><td><div><p>干预术语 id</p></div></td><td>92669964</td></tr><tr><td>src</td><td>string</td><td>是</td><td><div><p>源文本</p></div></td><td>大模型</td></tr><tr><td>tgt</td><td>string</td><td>是</td><td><div><p>干预后译文</p></div></td><td>LLM</td></tr><tr><td>paramMap</td><td>any</td><td>否</td><td><div><p>扩展参数配置（bizUserld：业务层面的用户 ID，用来区分不 同业务用户，做到“按用户隔离”的术语干预，互不影响。 bizType：业务场景类型/标识，用来区分不同场景，做到 “按场景隔离”的术语干预，互不影响。）</p></div><div><div>枚举值：</div><ul><li>bizType：业务场景类型。</li><li>bizUserId：业务用户id。</li></ul></div></td><td>{&quot;bizUserld&quot;:&quot;123456&quot;,&quot;bizType&quot;:session&quot;}</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| code | string | 响应状态码 | success |
| message | string | 响应信息 | success |
| requestId | string | 请求 id | 1DCD50EC-D218-1844-9CD8-E97CAB9D31BE |
| success | boolean | 接口调用是否成功 | true |
| httpStatusCode | string | http 状态码 | 200 |
| data | object | 返回数据 |  |
| terms | array<object> | 干预术语列表 |  |
| terms | object | 干预术语 |  |
| termId | string | 术语 id | 92669964 |
| src | string | 源文本 | 大模型 |
| tgt | string | 目标文本 | LLM |
| failCount | long | 失败数量 | 0 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "code": "success",
  "message": "success",
  "requestId": "1DCD50EC-D218-1844-9CD8-E97CAB9D31BE",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "terms": [
      {
        "termId": 92669964,
        "src": "大模型",
        "tgt": "LLM"
      }
    ],
    "failCount": 0
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 |
| --- | --- | --- |
| 400 | IdempotentParameterMismatch | The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical. |

访问[错误中心](https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |
| 2025-12-25 | OpenAPI 错误码发生变更 | [查看变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TermEdit?updateTime=2025-12-25#workbench-doc-change-demo) |
