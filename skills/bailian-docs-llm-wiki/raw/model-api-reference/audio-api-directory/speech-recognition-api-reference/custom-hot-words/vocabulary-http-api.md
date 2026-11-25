# 定制热词HTTP API参考

通过HTTP API管理定制热词列表，包括创建、查询、更新和删除热词列表。

**用户指南：**[提升识别准确率](../../../../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md)。热词列表数量上限等使用限制详见[热词限制与计费](../../../../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw10_limit_h2)。

> **重要**
>
> 新加坡地域的子业务空间暂不支持热词功能。

<a id="接口地址"></a>

<a id="fe508c8badxjg"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/customization`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="请求头"></a>

<a id="f5b7af17168sz"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| Authorization | string | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。 |
| Content-Type | string | 是 | 请求体的媒体类型，固定为`application/json`。 |

<a id="创建热词列表"></a>

<a id="e441257ef2stq"></a>

## 创建热词列表

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>定制热词模型，固定为<code>speech-biasing</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型，固定为<code>create_vocabulary</code>。</p><p><strong>target_model</strong> <code>string</code><strong>（必选）</strong></p><p>使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。</p><p><strong>prefix</strong> <code>string</code><strong>（必选）</strong></p><p>热词列表自定义前缀，仅允许数字和小写字母，长度不超过10个字符。</p><p><strong>vocabulary</strong> <code>array[object]</code><strong>（必选）</strong></p><p>热词列表数组。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>热词文本。</p><p>热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。</p><p>热词用于提升识别的准确率，请使用实际词语而非任意字符组合。</p><p>长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。</p><p><strong>weight</strong> <code>integer</code><strong>（必选）</strong></p><p>热词权重。常用值：4。</p><p>取值范围：[1, 5]。</p><p>如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。</p><p><strong>lang</strong> <code>string</code>（可选）</p><p>待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>取值范围（因模型而异）：</p><ul><li><p>Paraformer：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul></li><li><p>Fun-ASR：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li></ul></li></ul></div></section></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><p>新加坡地域和北京地域的API Key不同，详情请参见<a href="../../../preparations/get-api-key.md">获取与配置 API Key</a>。</p><a id="code-block"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;speech-biasing&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;create_vocabulary&quot;,
        &quot;target_model&quot;: &quot;fun-asr&quot;,
        &quot;prefix&quot;: &quot;testpfx&quot;,
        &quot;vocabulary&quot;: [
          {&quot;text&quot;: &quot;赛德克巴莱&quot;, &quot;weight&quot;: 4}
        ]
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>vocabulary_id</strong><code>string</code></p><p>创建的热词列表ID。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>创建的热词列表数量，固定为1。</p></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;vocabulary_id&quot;: &quot;vocab-testpfx-5112c3de3705486baxxxxxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;aee47022-2352-40fe-acfa-xxxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="批量查询热词列表"></a>

<a id="0d6d710380ffx"></a>

## 批量查询热词列表

<table><tbody><tr><td><a id="aff9713c97xur"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>定制热词模型，固定为<code>speech-biasing</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型，固定为<code>list_vocabulary</code>。</p><p><strong>prefix</strong> <code>string</code>（可选）</p><p>热词列表自定义前缀，如果设定则只返回指定前缀的热词列表。</p><p><strong>page_index</strong> <code>integer</code></p><p>页码索引，从0开始计数。</p><p>默认值：0。</p><p><strong>page_size</strong> <code>integer</code></p><p>每页包含数据条数。</p><p>默认值：10。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><p>新加坡地域和北京地域的API Key不同，详情请参见<a href="../../../preparations/get-api-key.md">获取与配置 API Key</a>。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;speech-biasing&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;list_vocabulary&quot;,
        &quot;prefix&quot;: &quot;testpfx&quot;,
        &quot;page_index&quot;: 0,
        &quot;page_size&quot;: 10
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="f9bba1e5bcz2z"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>vocabulary_list</strong><code>array[object]</code></p><p>查询到的热词列表。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>vocabulary_id</strong><code>string</code></p><p>热词列表ID。</p><p><strong>gmt_create</strong><code>string</code></p><p>创建时间。</p><p><strong>gmt_modified</strong><code>string</code></p><p>修改时间。</p><p><strong>status</strong><code>string</code></p><p>状态：</p><ul><li>OK：可调用</li><li>UNDEPLOYED：不可调用。</li></ul></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>固定为1。</p></div></section></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;vocabulary_list&quot;: [
            {
                &quot;gmt_create&quot;: &quot;2026-03-02 18:07:38&quot;,
                &quot;gmt_modified&quot;: &quot;2026-03-02 18:07:38&quot;,
                &quot;status&quot;: &quot;OK&quot;,
                &quot;vocabulary_id&quot;: &quot;vocab-ciotest-8e74bef2accf4xxxxxxxx&quot;
            },
            {
                &quot;gmt_create&quot;: &quot;2026-02-27 19:04:48&quot;,
                &quot;gmt_modified&quot;: &quot;2026-02-28 13:40:40&quot;,
                &quot;status&quot;: &quot;OK&quot;,
                &quot;vocabulary_id&quot;: &quot;vocab-sifasr-f483ad46e1844fxxxxxxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;81d51a05-8cdd-45c0-973f-xxxxxxxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="查询热词列表"></a>

<a id="2833029dbddju"></a>

## 查询热词列表

<table><tbody><tr><td><a id="3cc2e8ade02sf"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>定制热词模型，固定为<code>speech-biasing</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型，固定为<code>query_vocabulary</code>。</p><p><strong>vocabulary_id</strong> <code>string</code><strong>（必选）</strong></p><p>需要查询的热词列表ID。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><p>新加坡地域和北京地域的API Key不同，详情请参见<a href="../../../preparations/get-api-key.md">获取与配置 API Key</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;speech-biasing&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;query_vocabulary&quot;,
        &quot;vocabulary_id&quot;: &quot;vocab-testpfx-xxxx&quot;
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="06b012ec7cxrk"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>gmt_create</strong><code>string</code></p><p>创建时间。</p><p><strong>gmt_modified</strong><code>string</code></p><p>修改时间。</p><p><strong>status</strong><code>string</code></p><p>状态：</p><ul><li>OK：可调用</li><li>UNDEPLOYED：不可调用。</li></ul><p><strong>target_model</strong> <code>string</code></p><p>使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。</p><p><strong>vocabulary</strong><code>array[object]</code></p><p>查询到的热词列表。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code></p><p>热词文本。</p><p><strong>weight</strong> <code>integer</code></p><p>热词权重。</p><p><strong>lang</strong> <code>string</code></p><p>待识别音频语种。</p></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>固定为1。</p></div></section></td><td><a id="code-block-6"></a><pre class="language-json"><code>{
  &quot;output&quot;: {
    &quot;gmt_create&quot;: &quot;2025-12-19 11:47:11&quot;,
    &quot;gmt_modified&quot;: &quot;2025-12-19 11:47:11&quot;,
    &quot;status&quot;: &quot;OK&quot;,
    &quot;target_model&quot;: &quot;fun-asr&quot;,
    &quot;vocabulary&quot;: [
      {
        &quot;lang&quot;: &quot;zh&quot;,
        &quot;text&quot;: &quot;赛德克巴莱&quot;,
        &quot;weight&quot;: 4
      }
    ]
  },
  &quot;usage&quot;: {
    &quot;count&quot;: 1
  },
  &quot;request_id&quot;: &quot;3d461d3f-b2c4-4de5-xxxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="更新热词列表"></a>

<a id="a3353cde38ni9"></a>

## 更新热词列表

<table><tbody><tr><td><a id="37efc11199nce"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>定制热词模型，固定为<code>speech-biasing</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型，固定为<code>update_vocabulary</code>。</p><p><strong>vocabulary_id</strong> <code>string</code><strong>（必选）</strong></p><p>需要更新的热词列表ID。</p><p><strong>vocabulary</strong> <code>array[object]</code><strong>（必选）</strong></p><p>新的热词列表，将完全替换原有内容。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>热词文本。</p><p>热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。</p><p>热词用于提升识别的准确率，请使用实际词语而非任意字符组合。</p><p>长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。</p><p><strong>weight</strong> <code>integer</code><strong>（必选）</strong></p><p>热词权重。常用值：4。</p><p>取值范围：[1, 5]。</p><p>如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。</p><p><strong>lang</strong> <code>string</code>（可选）</p><p>待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>取值范围（因模型而异）：</p><ul><li><p>Paraformer：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul></li><li><p>Fun-ASR：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li></ul></li></ul></div></section></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><p>新加坡地域和北京地域的API Key不同，详情请参见<a href="../../../preparations/get-api-key.md">获取与配置 API Key</a>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;speech-biasing&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;update_vocabulary&quot;,
        &quot;vocabulary_id&quot;: &quot;vocab-testpfx-xxx&quot;,
        &quot;vocabulary&quot;: [
          {&quot;text&quot;: &quot;赛德克巴莱&quot;, &quot;weight&quot;: 4, &quot;lang&quot;: &quot;zh&quot;}
        ]
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="c596236c58aau"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据，固定为空。</p><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>更新的热词列表数量，固定为1。</p></div></section></td><td><a id="code-block-8"></a><pre class="language-json"><code>{
  &quot;output&quot;: {},
  &quot;usage&quot;: {
    &quot;count&quot;: 1
  },
  &quot;request_id&quot;: &quot;aee47022-2352-40fe-acfa-xxxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="删除热词列表"></a>

<a id="66dd22f7e2fbv"></a>

## 删除热词列表

<table><tbody><tr><td><a id="ff6650790bvzh"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>定制热词模型，固定为<code>speech-biasing</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型，固定为<code>delete_vocabulary</code>。</p><p><strong>vocabulary_id</strong> <code>string</code><strong>（必选）</strong></p><p>需要删除的热词列表ID。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><p>新加坡地域和北京地域的API Key不同，详情请参见<a href="../../../preparations/get-api-key.md">获取与配置 API Key</a>。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;speech-biasing&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;delete_vocabulary&quot;,
        &quot;vocabulary_id&quot;: &quot;vocab-testpfx-xxx&quot;
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="58f1118820aci"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据，固定为空。</p><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>删除的热词列表数量，固定为1。</p></div></section></td><td><a id="code-block-10"></a><pre class="language-json"><code>{
  &quot;output&quot;: {},
  &quot;usage&quot;: {
    &quot;count&quot;: 1
  },
  &quot;request_id&quot;: &quot;aee47022-2352-40fe-acfa-xxxx&quot;
}
</code></pre></td></tr></tbody></table>
