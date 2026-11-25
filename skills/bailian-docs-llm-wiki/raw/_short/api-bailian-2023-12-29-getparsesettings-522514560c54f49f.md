# GetParseSettings - 获取类目解析设置

查询指定类目的数据解析设置。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（`AliyunBailianDataFullAccess`或`AliyunBailianDataReadOnlyAccess`均可，已包括 sfm:GetParseSettings 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/GetParseSettings)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:GetParseSettings</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{WorkspaceId}/datacenter/parser/settings HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 否 | 文件所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3shx2gu255oqxxxx |
| CategoryId | string | 否 | 类目 ID，即 **AddCategory** 接口返回的`CategoryId`，或者在[应用数据](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/data-center)\-非结构化数据页签，单击类目名称旁的 ID 图标获取。 | cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td>string</td><td><div><p>本次请求 requestId</p></div></td><td>35A267BF-xxxx-54DB-8394-AA3B0742D833</td></tr><tr><td>Data</td><td>array&lt;object&gt;</td><td><div><p>请求成功返回的业务数据。</p></div></td><td></td></tr><tr><td>Data</td><td>object</td><td><div><p>返回具体内容</p></div></td><td></td></tr><tr><td>FileType</td><td>string</td><td><div><p>文件类型，扩展名，可能值为： pdf、docx、doc 等，列举当前类目中支持的所有文件类型。</p></div></td><td>pdf</td></tr><tr><td>ParserDisplayName</td><td>string</td><td><div><p>解析方式的显示名称。</p></div></td><td>电子文档解析</td></tr><tr><td>ParserConfig</td><td>object</td><td><div><p>解析器配置，仅在类型被设置为 Qwen VL 解析时才会返回。</p></div></td><td></td></tr><tr><td>ModelName</td><td>string</td><td><div><p>模型名称。</p></div><div><div>枚举值：</div><ul><li>qwen3-vl-plus：qwen3-vl-plus。</li></ul></div></td><td>qwen3-vl-plus</td></tr><tr><td>ModelPrompt</td><td>string</td><td><div><p>调用 Qwen VL 解析时的 Prompt。</p></div></td><td>#角色 你是一个专业的图片内容标注人员，擅长识别并描述出图片中的内容。 # 任务目标 请结合输入图片，详细描述图片中的内容。</td></tr><tr><td>Parser</td><td>string</td><td><div><p>解析该类目下当前类型文件使用的解析器。可能值为：</p><ul><li>DOCMIND：智能文档解析</li><li>DOCMIND_DIGITAL：电子文档解析</li><li>DOCMIND_LLM_VERSION：大模型文档解析</li><li>DASH_QWEN_VL_PARSER：Qwen VL 解析</li></ul></div></td><td>DOCMIND</td></tr><tr><td>Status</td><td>string</td><td><div><p>接口返回的状态码。</p></div></td><td>200</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>接口调用是否成功，可能值为：</p><ul><li>true：成功 。</li><li>false：失败。</li></ul></div></td><td>True</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误信息。</p></div></td><td>workspace id is null or invalid.</td></tr><tr><td>Code</td><td>string</td><td><div><p>错误状态码。</p></div></td><td>success</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
  "Data": [
    {
      "FileType": "pdf",
      "ParserDisplayName": "电子文档解析",
      "ParserConfig": {
        "ModelName": "qwen3-vl-plus",
        "ModelPrompt": "#角色\n你是一个专业的图片内容标注人员，擅长识别并描述出图片中的内容。\n# 任务目标\n请结合输入图片，详细描述图片中的内容。"
      },
      "Parser": "DOCMIND"
    }
  ],
  "Status": 200,
  "Success": true,
  "Message": "workspace id is null or invalid.",
  "Code": "success"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。
