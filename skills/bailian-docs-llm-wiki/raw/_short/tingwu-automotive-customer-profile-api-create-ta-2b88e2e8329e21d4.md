# CreateTask - 创建购车客户画像任务

创建购车客户画像任务的API参考。

<a id="前提条件"></a>

<a id="8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

<a id="接入地址"></a>

<a id="52a5ef4ab7tfg"></a>

## 接入地址

<a id="code-block"></a>

```http
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<a id="请求方式"></a>

<a id="606a6390d6xdn"></a>

## 请求方式

post方法请求

<a id="请求头"></a>

<a id="24323e44bdlg5"></a>

## 请求头

<a id="code-block-2"></a>

```http
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

<a id="创建任务"></a>

<a id="22bffc7225ihe"></a>

## 创建任务

创建购车客户画像分析任务。

<a id="请求参数"></a>

<a id="49d9739eabds5"></a>

### 请求参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义业务类型，固定为tingwu-automotive-customer-profile</p></td><td><p>tingwu-automotive-customer-profile</p></td></tr><tr><td><p>input</p></td><td><p>object</p></td><td><p>是</p></td><td><p>传入相关业务参数</p></td><td></td></tr><tr><td><p>input.fileUrl</p></td><td><p>string</p></td><td rowspan="3"><p>3选1</p></td><td><p>待分析文件oss URL地址</p></td><td><p>https://<em><strong>.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Expires=</strong></em>&amp;Signature=YOUR_SIGNATURE</p></td></tr><tr><td><p>input.text</p></td><td><p>string</p></td><td><p>待分析文本</p></td><td><p>每行必须按照如下格式：</p><p>${发言人名称}: ${发言人内容}</p><p>例子比如：</p><a id="code-block-3"></a><pre class="language-text"><code>张3: 我想买一个SUV汽车
李4: 想要什么价位的？
</code></pre></td></tr><tr><td><p>input.dataId</p></td><td><p>string</p></td><td><p>关联已经上传并解析完成的任务</p></td><td></td></tr><tr><td><p>input.appId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>应用id</p></td><td></td></tr><tr><td><p>input.task</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义任务类型，固定为createTask，表示创建任务</p></td><td><p>createTask</p></td></tr><tr><td><p>parameters</p></td><td><p>object</p></td><td><p>否</p></td><td><p>客户画像控制参数</p></td><td></td></tr><tr><td><p>parameters.identityRecognition</p></td><td><p>object</p></td><td><p>否</p></td><td><p>角色设定</p></td><td></td></tr><tr><td><p>parameters.identityRecognition.identityContents</p></td><td><p>list[]</p></td><td><p>是</p></td><td><p>角色设定列表，包含身份名称和描述，列表最大长度为5</p></td><td></td></tr><tr><td><p>parameters.identityRecognition.identityContents[i].Name</p></td><td><p>string</p></td><td><p>是</p></td><td><p>角色身份名称</p></td><td><p>客户</p></td></tr><tr><td><p>parameters.identityRecognition.identityContents[i].Description</p></td><td><p>string</p></td><td><p>是</p></td><td><p>角色身份描述</p></td><td><p>对车辆提出疑问，表达使用感受</p></td></tr><tr><td><p>parameters.contentExtraction</p></td><td><p>object</p></td><td><p>否</p></td><td><p>客户详细关注点提取参数对象</p></td><td></td></tr><tr><td><p>parameters.contentExtraction.extractionContents</p></td><td><p>list[]</p></td><td><p>是</p></td><td><p>客户详细关注点提取的提取维度列表，包含提取项的名称和定义</p><p>个数不超过150</p></td><td></td></tr><tr><td><p>parameters.contentExtraction.extractionContents[i].title</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户详细关注点提取的提取维度名称</p></td><td><p>订车相关</p></td></tr><tr><td><p>parameters.contentExtraction.extractionContents[i].content</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户详细关注点提取的维度定义</p></td><td><p>定制颜色要多久？</p></td></tr><tr><td><p>parameters.contentExtraction.extractionContents[i].identity</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户的角色名称</p></td><td><p>客户</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="9c516a766ag9w"></a>

### 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>object</p></td><td></td><td></td></tr><tr><td><p>output.dataId</p></td><td><p>string</p></td><td><p>任务id</p></td><td><p>lsA***</p></td></tr><tr><td><p>output.status</p></td><td><p>string</p></td><td><p>任务状态：</p><ul><li><p>0：成功</p></li><li><p>1：进行中</p></li><li><p>2：失败</p></li></ul></td><td><p>0</p></td></tr><tr><td><p>usage</p></td><td><p>object</p></td><td><p>用量</p></td><td><p>{}</p></td></tr><tr><td><p>code</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>InvalidParameter</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>Agent Input text format error.</p></td></tr><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求id</p></td><td><p>f97ee37d-0f9c-9b93-b6bf-bd263a232bf9</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="3ae58682d3kav"></a>

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

<a id="code-block-4"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-automotive-customer-profile",
    "input": {
        "task": "createTask",
        "text": "张3:我想买一个SUV\n李4：想要什么价位的？",
        "appId": "tw_***"
    },
    "parameters": {
        "identityRecognition": {
            "identityContents": [
                {
                    "name": "***",
                    "description": "介绍车辆的不同配置、性能与技术、舒适性与便利性等"
                },
                {
                    "name": "***",
                    "description": "对车辆提出疑问，表达使用感受等"
                }
            ]
        },
        "contentExtraction": {
            "extractionContents": [
                {
                    "title": "***",
                    "content": "车辆基础信息",
                    "identity": "客户询问车型参数、技术配置，销售详细介绍参数信息"
                }
            ]
        }
    }
}'
```

<a id="返回示例"></a>

<a id="cdb64d4059e73"></a>

### 返回示例

<a id="code-block-5"></a>

```json
{
    "output": {
        "dataId": "Foi***"
    },
    "usage": {},
    "request_id": "95edfcc7-0481-90aa-884b-3ebf3603b6f8"
}
```
