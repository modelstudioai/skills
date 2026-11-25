# GenerateUploadConfig

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

通过这接口可以拿到文件上传的地址和凭证，参考如下文档可以完成文件上传： [OSS-表单上传](https://help.aliyun.com/zh/oss/user-guide/form-upload?scm=20140722.H_31849._.OR_help-T_cn~zh-V_1)

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

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
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| aimiaobi:GenerateUploadConfig | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>AgentKey</td><td><p>string</p></td><td><p>是</p></td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td><p>xxxxx_p_efm</p></td></tr><tr><td>FileName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文件名称</p></div></td><td><p>test.docx</p></td></tr><tr><td>ParentDir</td><td><p>string</p></td><td><p>是</p></td><td><div><p>父目录：</p><ul><li><p>materialDocument: 妙笔-素材库</p></li><li><p>datasetUpload: 妙搜-数据集</p></li><li><p>intervenes：干预</p></li><li><p>temp: 临时上传目录(周期释放)</p></li></ul></div></td><td><p>dataset</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><p>PlainResult</p></td><td></td></tr><tr><td><p>Code</p></td><td><p>string</p></td><td><p>状态码</p></td><td><p>successful</p></td></tr><tr><td><p>Data</p></td><td><p>object</p></td><td><p>业务数据</p></td><td></td></tr><tr><td><p>FileKey</p></td><td><p>string</p></td><td><p>文件唯一标识：可以当做 url 给到全妙</p></td><td><p>oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx</p></td></tr><tr><td><p>FormDatas</p></td><td><p>object</p></td><td><p>上传 oss 的凭证信息：</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;OSSAccessKeyId&quot;: &quot;xxx&quot;,
  &quot;Signature&quot;: &quot;YOUR_SIGNATURE&quot;,
  &quot;MaxSize&quot;: 31457280,
  &quot;key&quot;: &quot;aimiaobi/dataset/2_2/xx.txt&quot;,
  &quot;policy&quot;: &quot;xxx==&quot;
}
</code></pre></td><td></td></tr><tr><td></td><td><p>string</p></td><td></td><td></td></tr><tr><td><p>PostUrl</p></td><td><p>string</p></td><td><p>上传 oss 的地址（妙笔自有的 OSS 域名，固定是：<a href="https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/"></a><a href="https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/">https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/</a>）</p></td><td><p><a href="https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/">https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/</a></p></td></tr><tr><td><p>HttpStatusCode</p></td><td><p>integer</p></td><td><p>http 状态码</p></td><td><p>200</p></td></tr><tr><td><p>Message</p></td><td><p>string</p></td><td><p>错误说明</p></td><td><p>successful</p></td></tr><tr><td><p>RequestId</p></td><td><p>string</p></td><td><p>请求唯一标识</p></td><td><p>1813ceee-7fe5-41b4-87e5-982a4d18cca5</p></td></tr><tr><td><p>Success</p></td><td><p>boolean</p></td><td><p>是否成功：true 成功，false 失败</p></td><td><p>true</p></td></tr></tbody></table>

<a id="执行文件上传"></a>

<a id="api-detail-responseParamsDescription"></a>

## 执行文件上传

拿到 PostUrl（妙笔官方 OSS） 、FormDatas （OSS 的临时鉴权）两个参数之后，需要手动上传 到 OSS 中。

> **说明**
>
> 此步骤是核心上传步骤，一定要执行。 执行上传完毕之后：fileKey 即可用于其他接口。

示例请求 CURL 为：

> **说明**
>
> 注意：此示例仅为 简单的 CURL 示例，具体 SDK 对接流程一般使用 **代码编写方式** 发起表单的文件上传。

<a id="code-block-2"></a>

```bash
curl -X POST --location "${PostUrl}" \
    -H "Content-Type: multipart/form-data; boundary=WebKitFormBoundarykFF1FqdGZn2nxzfb" \
    -F "key=${key};type=*/*" \
    -F "OSSAccessKeyId=YOUR_ACCESS_KEY_ID" \
    -F "Signature=YOUR_SIGNATURE" \
    -F "policy=${policy};type=*/*" \
    -F "file=@/Users/<username>/xxx.text;filename=xxx.text;type=text/plain"
```

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```json
{
  "Code": "successful",
  "Data": {
    "FileKey": "oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx",
    "FormDatas": {
      "key": ""
    },
    "PostUrl": "https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/"
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GenerateUploadConfig#workbench-doc-change-demo)。
