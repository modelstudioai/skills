# ListGeneratedContents - 获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListGeneratedContents)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:ListGeneratedContents</td><td>list</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AgentKey</td><td>string</td><td>是</td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td>xxxxx_p_efm</td></tr><tr><td>TaskId</td><td>string</td><td>否</td><td><div><p>任务唯一标识</p><div><div><strong>说明</strong> TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</div></div></div></td><td>task-03d46184ee7d8749</td></tr><tr><td>StartTime</td><td>string</td><td>否</td><td><div><p>开始时间</p></div></td><td>2024-01-04 11:46:07</td></tr><tr><td>EndTime</td><td>string</td><td>否</td><td><div><p>结束时间</p></div></td><td>2024-01-04 11:46:07</td></tr><tr><td>Title</td><td>string</td><td>否</td><td><div><p>标题内容</p></div></td><td>杭州亚运会</td></tr><tr><td>Query</td><td>string</td><td>否</td><td><div><p>搜索关键词：支持标题和正文模糊搜索</p></div></td><td>检索Query</td></tr><tr><td>ContentDomain</td><td>string</td><td>否</td><td><div><p>内容领域（创作类型的分类）</p><ul><li>media: 传媒写作</li><li>government: 政府公文写作</li><li>office：办公写作</li><li>market：营销写作</li><li>custom: 自定义写作</li><li>commentGenerate: 观点生成</li></ul></div><div><div>枚举值：</div><ul><li>market：营销写作。</li><li>government：政务。</li><li>custom：自定义写作。</li><li>media：传媒。</li><li>office：办公写作。</li><li>commentGenerate：观点生成。</li></ul></div></td><td>media</td></tr><tr><td>Current</td><td>integer</td><td>否</td><td><div><p>当前页码</p></div></td><td>1</td></tr><tr><td>Size</td><td>integer</td><td>否</td><td><div><p>每页条数：默认 10</p></div></td><td>10</td></tr><tr><td>DataType</td><td>string</td><td>否</td><td><div><p>数据类型筛选</p><ul><li>plainText：纯文本</li><li>richText：富文本</li><li>html：网页</li><li>pdf：PDF</li><li>word：WORD</li><li>excel：excel</li><li>csv：CSV</li><li>image：图片</li><li>video：视频</li><li>audio：音频</li></ul></div></td><td>plainText</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>响应结果</p></div></td><td></td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>NoData</td></tr><tr><td>Current</td><td>integer</td><td><div><p>当前页码</p></div></td><td>1</td></tr><tr><td>Data</td><td>array&lt;object&gt;</td><td><div><p>文档列表</p></div></td><td></td></tr><tr><td>Data</td><td>object</td><td><div><p>文档</p></div></td><td></td></tr><tr><td>Content</td><td>string</td><td><div><p>正文：富文本</p></div></td><td>杭州亚运会</td></tr><tr><td>ContentDomain</td><td>string</td><td><div><p>内容领域（创作类型的分类）</p><ul><li>media: 传媒写作</li><li>government: 政府公文写作</li><li>office：办公写作</li><li>market：营销写作</li><li>custom: 自定义写作</li><li>commentGenerate: 观点生成</li></ul></div></td><td>media</td></tr><tr><td>ContentText</td><td>string</td><td><div><p>正文：纯文本</p></div></td><td>杭州亚运会</td></tr><tr><td>CreateTime</td><td>string</td><td><div><p>创建日期</p></div></td><td>2024-01-04 11:46:07</td></tr><tr><td>CreateUser</td><td>string</td><td><div><p>创建者</p></div></td><td>&quot;123&quot;</td></tr><tr><td>DeviceId</td><td>string</td><td><div><p>设备 ID</p></div></td><td>xxx</td></tr><tr><td>Id</td><td>long</td><td><div><p>文档唯一标识</p></div></td><td>10</td></tr><tr><td>KeywordList</td><td>array</td><td><div><p>关键词</p></div></td><td></td></tr><tr><td>KeywordList</td><td>string</td><td><div><p>关键词</p></div></td><td>观点</td></tr><tr><td>Keywords</td><td>string</td><td><div><p>关键词（string）</p></div></td><td>观点</td></tr><tr><td>Prompt</td><td>string</td><td><div><p>最后一次生成的提示词</p></div></td><td>创作xxx文章</td></tr><tr><td>TaskId</td><td>string</td><td><div><p>会话任务唯一标识</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr><tr><td>Title</td><td>string</td><td><div><p>标题</p></div></td><td>杭州亚运会</td></tr><tr><td>UpdateTime</td><td>string</td><td><div><p>更新日期</p></div></td><td>2024-01-04 11:46:07</td></tr><tr><td>UpdateUser</td><td>string</td><td><div><p>更新者</p></div></td><td>&quot;1111&quot;</td></tr><tr><td>Uuid</td><td>string</td><td><div><p>UUID 溯源唯一标识</p></div></td><td>xxx</td></tr><tr><td>FileKey</td><td>string</td><td><div><p>文件唯一标识</p></div></td><td>oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx</td></tr><tr><td>FileAttr</td><td>object</td><td><div><p>文件属性</p></div></td><td></td></tr><tr><td>FileName</td><td>string</td><td><div><p>文件名称</p></div></td><td>homedepothp.txt</td></tr><tr><td>Width</td><td>integer</td><td><div><p>视频宽度</p></div></td><td>800</td></tr><tr><td>TmpUrl</td><td>string</td><td><div><p>视频文件临时访问 URL。1 小时过期</p></div></td><td><a href="http://www.example.com/xxx.mp4">http://www.example.com/xxx.mp4</a></td></tr><tr><td>Height</td><td>integer</td><td><div><p>视频高度</p></div></td><td>500</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 状态码</p></div></td><td>200</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误说明</p></div></td><td>success</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>1813ceee-7fe5-41b4-87e5-982a4d18cca5</td></tr><tr><td>Size</td><td>integer</td><td><div><p>每页记录数</p></div></td><td>10</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td>true</td></tr><tr><td>Total</td><td>integer</td><td><div><p>总记录数</p></div></td><td>100</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "NoData",
  "Current": 1,
  "Data": [
    {
      "Content": "杭州亚运会",
      "ContentDomain": "media",
      "ContentText": "杭州亚运会",
      "CreateTime": "2024-01-04 11:46:07",
      "CreateUser": 123,
      "DeviceId": "xxx",
      "Id": 10,
      "KeywordList": [
        "观点"
      ],
      "Keywords": "观点",
      "Prompt": "创作xxx文章",
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
      "Title": "杭州亚运会",
      "UpdateTime": "2024-01-04 11:46:07",
      "UpdateUser": 1111,
      "Uuid": "xxx",
      "FileKey": "oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx",
      "FileAttr": {
        "FileName": "homedepothp.txt",
        "Width": 800,
        "TmpUrl": "http://www.example.com/xxx.mp4",
        "Height": 500
      }
    }
  ],
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
