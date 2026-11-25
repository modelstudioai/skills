# 千问-文生图API参考

千问-文生图模型（Qwen-Image）是一款通用图像生成模型，支持多种艺术风格，尤其擅长 复杂文本渲染 。模型支持多行布局、段落级文本生成以及细粒度细节刻画，可实现复杂的图文混合布局设计。

|  |
| --- |
| **快速入口：**[使用指南](../../../../model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md) \| 在线体验（[北京](https://bailian.console.aliyun.com/cn-beijing/model/experience/vision/imageGenerate?modelId=qwen-image-2.0-pro) \| [新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/experience/vision/imageGenerate?modelId=qwen-image-2.0-pro)） \| [技术博客](https://qwen.ai/blog?id=9467b4bff9c638e847f08443802c6b96ab116a87&from=research.research-list) |

<a id="效果展示"></a>

<a id="5849834e92mb7"></a>

## 效果展示

| 输入提示词 | 输出图像 |
| --- | --- |
| 冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。 | ![image (10)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9373463771/p1058343.png) |

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>模型简介</strong></th><th><strong>输出图像规格</strong></th></tr></thead><tbody><tr><td><p>qwen-image-2.0-pro <code>推荐</code></p><blockquote><p>当前与qwen-image-2.0-pro-2026-04-22能力相同</p></blockquote></td><td rowspan="4"><p>千问图像生成与编辑模型Pro系列。文字渲染、真实质感、语义遵循能力更强。</p><blockquote><p>图像编辑请参考<a href="qwen-image-edit-api.md">千问-图像编辑</a>。</p></blockquote></td><td rowspan="6"><p>图像分辨率：支持自由设置宽高，输出图像总像素需在512<em>512至2048</em>2048之间。默认分辨率为2048*2048。</p><p>图像格式：png</p><p>图像张数：1-6张</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-06-22 <code>推荐</code></p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-04-22</p></td></tr><tr><td><p>qwen-image-2.0-pro-2026-03-03</p></td></tr><tr><td><p>qwen-image-2.0 <code>推荐</code></p><blockquote><p>当前与qwen-image-2.0-2026-03-03能力相同</p></blockquote></td><td rowspan="2"><p>千问图像生成与编辑模型加速版，兼顾效果与响应速度。</p><blockquote><p>图像编辑请参考<a href="qwen-image-edit-api.md">千问-图像编辑</a>。</p></blockquote></td></tr><tr><td><p>qwen-image-2.0-2026-03-03 <code>推荐</code></p></td></tr></tbody></table>

各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

在调用前，先[获取与配置 API Key](../../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](../../../preparations/install-sdk.md)。

> **重要**
>
> 华北2（北京）和新加坡地域拥有独立的 **API Key**与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="同步接口"></a>

<a id="39337f0fd0wzt"></a>

## 同步接口

<a id="http调用"></a>

<a id="90575c8228nmq"></a>

### HTTP调用

千问图像模型支持同步接口，一次请求即可获得结果，调用流程简单，推荐用于多数场景。

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="576ce84612n7u"></a><h4>请求参数</h4><a id="bb0a157056fbk"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="45d1fa2260zn6"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：<code>qwen-image-2.0-pro</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。<strong>当前仅支持单轮对话</strong>，数组内<strong>有且只有一个元素</strong>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词用于描述您期望生成的图像内容、风格和构图。</p><p>支持中英文，qwen-image-2.0系列模型长度上限为 1300 Token，其他模型为 800 Token，超出部分将自动截断。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超出部分将自动截断。</p><p>示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图像的分辨率，格式为<code>宽*高</code>。</p><p><strong>qwen-image-2.0系列模型</strong>：输出图像总像素需在<code>512*512</code>至<code>2048*2048</code>之间，默认分辨率为<code>2048*2048</code>。推荐分辨率：</p><ul><li><code>2688*1536</code> ：16:9</li><li><code>1536*2688</code> ：9:16</li><li><code>2048*2048</code>（<strong>默认值）</strong>：1:1</li><li><code>2368*1728</code> ：4:3</li><li><code>1728*2368</code> ：3:4</li></ul><p><strong>n</strong> <code>integer</code> （可选）</p><p>输出图像的数量，默认值为1。</p><p>对于qwen-image-2.0系列模型，可选择输出1-6张图片。</p><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><p>是否开启 Prompt（提示词）智能改写功能。开启后模型将对正向提示词进行优化与润色。此功能不会修改反向提示词。</p><ul><li><code>true</code>：<strong>默认值</strong>，开启智能改写。如果希望图像内容更多样化，由模型补充细节，建议开启此选项。</li><li><code>false</code>：关闭智能改写。如果图像细节更可控，建议关闭此选项，并参考<a href="../../../../model-user-guide/use-cases/text-to-image-prompt.md">文生图Prompt指南</a>进行优化，</li></ul><a id="accordion-点击查看改写示例"></a><section><p>点击查看改写示例</p><div><p><strong>原始提示词（orig_prompt）</strong>：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>实际提示词（actual_prompt）</strong>：一只坐着的橘黄色猫咪，毛发蓬松柔软，阳光透过窗户洒在它身上，呈现出温暖的光泽。猫咪体型匀称，四肢自然弯曲，稳稳地坐在木质地板上，尾巴轻轻卷曲在身侧，显得格外放松而优雅。它的大眼睛圆润明亮，瞳孔微微收缩，流露出愉悦而灵动的神情，嘴角微扬，仿佛正享受着美好的时光。耳朵微微向前倾斜，透露出活泼与好奇。背景是一间温馨的现代家居客厅，浅色木地板、一扇半开的窗户透进柔和的自然光，窗外可见绿意盎然的庭院，窗台上摆放着几盆绿植。画面采用真实摄影风格，细节逼真，光影层次丰富，突出猫咪的毛发质感、眼神神态与整体姿态的生动自然，整体氛围轻松愉快，充满生活气息。</p></div></section><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否在图像右下角添加 &quot;Qwen-Image&quot; 水印。默认值为 <code>false</code>。水印样式：<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8972029571/p1012089.jpg" alt="1"></p><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-image-2.0-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;negative_prompt&quot;: &quot;低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: false,
        &quot;size&quot;: &quot;2048*2048&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b7e833ee1f962"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。此数组仅包含一个元素。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section><p><strong>task_metric</strong> <code>object</code></p><p>任务结果统计。使用qwen-image-2.0系列时无此返回值。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量，当前固定为1。</p><p><strong>width</strong> <code>integer</code></p><p>模型生成图像的宽度（像素）。</p><p><strong>height</strong> <code>integer</code></p><p>模型生成图像的高度（像素）。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>图像URL仅保留24小时，超时后会被自动清除，请及时保存生成的图像。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx&quot;
                        }
                    ],
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;height&quot;: 2048,
        &quot;image_count&quot;: 1,
        &quot;width&quot;: 2048
    },
    &quot;request_id&quot;: &quot;d0250a3d-b07f-49e1-bdc8-6793f4929xxx&quot;
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;n must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

* * *

<a id="dashscope-sdk调用"></a>

<a id="bc5bea44cab1b"></a>

### DashScope SDK调用

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据语言特性进行封装。同步调用参数说明可参考[HTTP调用](qwen-image-api.md#90575c8228nmq)。

<a id="sec-tabs-3"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

> **说明**
>
> 请先确认已安装最新版DashScope Python SDK，否则可能运行报错：[安装SDK](../../../preparations/install-sdk.md)。

<a id="3dcaa20713o8e"></a>

##### 请求示例

<a id="code-block-4"></a>

```python
import json
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

messages = [
    {
        "role": "user",
        "content": [
            {"text": "冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。"}
        ]
    }
]

# 1.x 的 prompt_extend/watermark/negative_prompt/size 等参数，2.0 中统一通过 parameters 传入
response = client.multimodal.chat.create(
    model="qwen-image-2.0-pro",
    messages=messages,
    parameters={
        "watermark": False,
        "prompt_extend": True,
        "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        "size": "2048*2048",
    },
)

# 2.0 SDK：生成结果从 message.content_parts 读取，图像 part 形如 {"image": URL, "type": "image"}
message = response.choices[0].message
for part in (message.content_parts or []):
    if "image" in part:
        print(json.dumps(part, ensure_ascii=False))
```

<a id="f60171c71fg3t"></a>

##### 响应示例

> 图像链接的有效期为24小时，请及时下载图像。

<a id="code-block-5"></a>

```json
{
    "status_code": 200,
    "request_id": "d2d1a8c0-325f-9b9d-8b90-xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "width": 2048,
        "image_count": 1,
        "height": 2048
    }
}
```

<a id="java"></a>

<a id="java-h4"></a>

#### Java

> **说明**
>
> 请先确认已安装最新版DashScope Java SDK，否则可能运行报错：[安装SDK](../../../preparations/install-sdk.md)。

<a id="d137cf544fnw6"></a>

##### 请求示例

<a id="code-block-6"></a>

```java
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class QwenImage {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：static String apiKey ="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

        MultiModalConversation conv = new MultiModalConversation();

        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。")
                )).build();

        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", false);
        parameters.put("prompt_extend", true);
        parameters.put("negative_prompt", "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。");
        parameters.put("size", "2048*2048");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(apiKey)
                .model("qwen-image-2.0-pro")
                .messages(Collections.singletonList(userMessage))
                .parameters(parameters)
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="9631851c87t5h"></a>

##### 响应示例

> 图像链接的有效期为24小时，请及时下载图像。

<a id="code-block-7"></a>

```json
{
    "requestId": "5b6f2d04-b019-40db-a5cc-xxxxxx",
    "usage": {
        "image_count": 1,
        "width": 2048,
        "height": 2048
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ]
    }
}
```

<a id="结合-openai-agents-sdk-使用"></a>

<a id="oaisdk00h2t"></a>

## 结合 OpenAI Agents SDK 使用

千问-文生图（Qwen-Image）等图像生成模型通过 DashScope 原生接口调用，不支持 OpenAI 兼容（compatible-mode）模式，因此无法直接作为 OpenAI Agents SDK 中 Agent 的推理模型。

在 OpenAI Agents SDK 等智能体框架中，可将图像生成能力封装为工具（function tool），由支持 OpenAI 兼容模式的文本对话模型（如 qwen-plus）作为 Agent 的推理核心进行调度。示例如下：

运行前请先安装依赖：`pip install openai-agents dashscope`。

<a id="code-block-8"></a>

```python
import os
import asyncio
import dashscope
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel

# 从环境变量读取百炼 API Key（若未配置，可直接替换为 api_key="sk-xxx"）
API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# 图像生成走 DashScope 原生接口；文本对话模型（Agent 推理核心）通过 OpenAI 兼容模式接入
client = dashscope.Client(
    api_key=API_KEY,
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
openai_client = AsyncOpenAI(api_key=API_KEY, base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

# 将图像生成封装为工具（function tool），供 Agent 调用
@function_tool
def generate_image(prompt: str) -> str:
    """根据文本描述生成一张图片并返回图片 URL。prompt：图片内容的文字描述。"""
    rsp = client.multimodal.chat.create(
        model="qwen-image-2.0-pro",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    # 2.0 SDK：生成结果从 message.content_parts 读取，图像 part 形如 {"image": URL, "type": "image"}
    message = rsp.choices[0].message
    for part in (message.content_parts or []):
        if "image" in part:
            return part["image"]
    return "生成失败：未返回图像"

agent = Agent(
    name="图像生成助手",
    instructions="你是图像生成助手。当用户想要图片时，调用 generate_image 工具，并把返回的图片 URL 告诉用户。",
    model=OpenAIChatCompletionsModel(model="qwen-plus", openai_client=openai_client),
    tools=[generate_image],
)

async def main():
    result = await Runner.run(agent, "帮我画一只在草地上奔跑的柯基犬")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

<a id="计费与限流"></a>

<a id="aa1d5dd501v1b"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../../../model-user-guide/test-1/model-pricing.md#2e0ddf5c9edy0)。
-   模型限流请参见[千问（Qwen-Image）](../../../../model-user-guide/get-started-with-models/rate-limit.md#f812e7c63axvx)。
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="2000000003510"></a>

## 常见问题

<a id="q-prompt-extend参数应该开启还是关闭"></a>

<a id="2000000000135"></a>

#### Q：prompt\_extend参数应该开启还是关闭？

A：如果希望图像内容更多样化，由模型补充细节，建议开启此选项（默认）。如果图像细节更可控，建议关闭此选项，并参考[文生图Prompt指南](../../../../model-user-guide/use-cases/text-to-image-prompt.md)进行优化，

<a id="q-qwen-image-2-0系列模型有什么区别"></a>

<a id="8c22963d65qr5"></a>

#### Q：qwen-image-2.0系列模型有什么区别？

A：

-   **图像生成与编辑融合模型：**同时支持文生图和图像编辑。
    
    -   `qwen-image-2.0-pro`、`qwen-image-2.0-pro-2026-04-22`：当前两者能力相同，Pro系列具备更专业的文字渲染能力、更细腻的真实质感，细腻刻画写实场景，以及更强的语义遵循能力。仅支持同步接口。
    -   `qwen-image-2.0`、`qwen-image-2.0-2026-03-03`：当前两者能力相同，加速版有效实现了模型效果和性能的最佳平衡。仅支持同步接口。

<a id="q-如何获取图像存储的访问域名白名单"></a>

<a id="5fb153423ct8z"></a>

### Q：如何获取图像存储的访问域名白名单？

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL（链接有效期为 24 小时，请及时下载保存）。图片URL的域名格式为`dashscope-{标识}.oss-accelerate.aliyuncs.com`或`dashscope-{标识}.oss-cn-{地域}.aliyuncs.com`。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会动态变更，以下bucket名称仅供参考，可能随时更新：dashscope-a717、dashscope-66f3、dashscope-7c2c、dashscope-2522、dashscope-c72b、dashscope-0484、dashscope-7e0f、dashscope-5859、dashscope-5496、dashscope-35f9、dashscope-31d9、dashscope-7f1f、dashscope-cc75、dashscope-64e9。为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。API当前仅支持返回URL格式，不支持base64格式输出。
