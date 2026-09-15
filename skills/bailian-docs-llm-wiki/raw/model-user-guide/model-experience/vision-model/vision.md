# 图像与视频理解

视觉理解模型可以根据您传入的图片或视频进行回答，支持单图或多图的输入，适用于图像描述、视觉问答、物体定位等多种任务。

**在线体验：**访问[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，在页面右上角选择目标地域，进入[视觉模型](https://bailian.console.aliyun.com/model/experience/vision)页面进行体验。

## 快速开始

您需要先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。若通过OpenAI SDK进行调用，需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

以下示例演示了如何调用模型描述图像内容。关于本地文件和图像限制的说明，请参见[如何传入本地文件](https://help.aliyun.com/zh/model-studio/vision#d987f8de5395x)、[图像限制](raw/model-user-guide/model-experience/vision-model/vision.md)章节。

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        },
    ],
)
print(completion.choices[0].message.content)
```

### 返回结果

```
这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
   // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
  const response = await openai.chat.completions.create({
    model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages: [
      {
        role: "user",
        content: [{
            type: "image_url",
            image_url: {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
            }
          },
          {
            type: "text",
            text: "图中描绘的是什么景象?"
          }
        ]
      }
    ]
  });
  console.log(response.choices[0].message.content);
}
main()
```

### 返回结果

```
这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。
```

#### Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.StreamResponse;
import com.openai.models.chat.completions.*;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
                .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
                .build();

        // 构造多模态消息内容：图片 + 文本
        ChatCompletionContentPart imagePart = ChatCompletionContentPart.ofImageUrl(
                ChatCompletionContentPartImage.builder()
                        .imageUrl(ChatCompletionContentPartImage.ImageUrl.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg")
                                .build())
                        .build());
        ChatCompletionContentPart textPart = ChatCompletionContentPart.ofText(
                ChatCompletionContentPartText.builder()
                        .text("图中描绘的是什么景象?")
                        .build());

        // 创建聊天请求
        ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .model("qwen3.8-max")
                .addUserMessageOfArrayOfContentParts(List.of(imagePart, textPart))
                .build();

        StringBuilder fullResponse = new StringBuilder();

        // 所有代码示例均采用流式输出，以清晰和直观地展示模型输出过程。如果您希望查看非流式输出的案例，请参见https://help.aliyun.com/zh/model-studio/text-generation
        try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
            streamResponse.stream().forEach(chunk -> {
                System.out.println(chunk);
                String content = chunk.choices().get(0).delta().content().orElse("");
                if (!content.isEmpty()) {
                    fullResponse.append(content);
                }
            });
            System.out.println(fullResponse);
        } catch (Exception e) {
            System.err.println("错误信息：" + e.getMessage());
            System.err.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
    }
}
```

### 返回结果

```
这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.8-max",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

### 返回结果

```
{
  "choices": [
    {
      "message": {
        "content": "这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 1270,
    "completion_tokens": 54,
    "total_tokens": 1324
  },
  "created": 1725948561,
  "system_fingerprint": null,
  "model": "qwen3.8-max",
  "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
{
    "role": "user",
    "content": [
    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
    {"text": "图中描绘的是什么景象?"}]
}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3.7-plus',  # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages = messages
)
print(response.output.choices[0].message.content[0]["text"])
```

### 返回结果

```
是一张在海滩上拍摄的照片。照片中有一位女士和一只狗。女士坐在沙滩上，微笑着与狗互动。狗戴着项圈，似乎在与女士握手。背景是大海和天空，阳光洒在她们身上，营造出温馨的氛围。
```

#### Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                 // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
这是一张在海滩上拍摄的照片。照片中有一个穿着格子衬衫的人和一只戴着项圈的狗。人和狗面对面坐着，似乎在互动。背景是大海和天空，阳光洒在他们身上，营造出温暖的氛围。
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象?"}
                ]
            }
        ]
    }
}'
```

### 返回结果

```
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "这是一张在海滩上拍摄的照片。照片中有一个穿着格子衬衫的人和一只戴着项圈的狗。他们坐在沙滩上，背景是大海和天空。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "output_tokens": 55,
    "input_tokens": 1271,
    "image_tokens": 1247
  },
  "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
}
```

#### dashscope CLI

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope multimodal-conversation create -m qwen-vl-plus -t "你好"
```

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

## 模型效果

### 图像问答

描述图像中的内容或者对其进行分类打标，如识别人物、地点、动植物等。

![p1021359](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025117.webp)

如果太阳很刺眼，我应该用这张图中的什么物品？

当太阳很刺眼时，你应该使用图中的粉色太阳镜。太阳镜可以有效阻挡强光、减少紫外线对眼睛的伤害，帮助你在阳光强烈时保护视力并提升视觉舒适度。

### 创意写作

根据图片或视频内容生成生动的文字描述，适用于故事创作、文案撰写、短视频脚本等创意场景。

![vl-问答](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025118.webp)

请根据图片内容，帮我写一段有意思的朋友圈文案。

好的，这张图片充满了浓郁的中秋节日氛围，古典与现代元素结合得非常巧妙。根据图片中的主要元素，我为你准备了几个不同风格的朋友圈文案，你可以根据自己的喜好选择。

**诗意唯美风**

今夜月明人尽望，不知秋思落谁家。嫦娥奔月，玉兔捣药，古人的浪漫在今夜被点亮。愿这轮明月，能照亮你回家的路，也能寄去我最深的思念。中秋节快乐！

**温馨祝福风**

月圆人团圆，中秋夜最温柔。看烟花绽放，赏圆月当空，吃一口月饼，道一声安康。愿你我心中所念，皆能如愿以偿。祝大家中秋快乐，阖家幸福！

### 文字识别与信息抽取

识别图像中的文字、公式或抽取票据、证件、表单中的信息，支持格式化输出文本。

![\-q2cdz6jy89b6m3kp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025119.webp)

提取图中的：\['发票代码','发票号码','到站','燃油费','票价','乘车日期','开车时间','车次','座号'\]，请你以JSON格式输出。

{

"发票代码": "221021325353",

"发票号码": "10283819",

"到站": "开发区",

"燃油费": "2.0",

"票价": "8.00<全>",

"乘车日期": "2013-06-29",

"开车时间": "流水",

"车次": "040",

"座号": "371"

}

### 多学科题目解答

解答图像中的数学、物理、化学等问题，适用于中小学、大学以及成人教育阶段。

![\-5jwcstcvmdpqghaj](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025120.webp)

请你分步骤解答图中的数学题。

![\-答案](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025121.webp)

### 视觉编程

可通过图像或视频生成代码，可用于将设计图、网站截图等生成HTML、CSS、JS 代码。

![code](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025123.webp)

根据我的草图设计使用HTML、CSS创建网页，主色调为黑色。

![code-预览](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025124.png)

**网页预览效果**

### 物体定位

支持二维和三维定位，可用于判断物体方位、视角变化、遮挡关系。三维定位为Qwen3-VL模型新增能力。

> Qwen2.5-VL模型 480_480_～\* 2560\*2560 分辨率范围内，物体定位效果较为鲁棒，在此范围之外检测精度可能会下降（偶发检测框漂移现象）。

> 如需将定位结果绘制到原图可参见 [常见问题](raw/model-user-guide/model-experience/vision-model/vision.md) 。

**二维定位**![\-530xdcos1lqkcfuy](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025125.webp)

-   返回 Box（边界框）坐标 ：检测图中所有食物并以JSON格式输出其bbox的坐标。
-   返回 Point（中心点）坐标：以点的形式定位图中所有食物并以XML格式输出其point坐标。

**可视化展示二维定位效果**![\-mu9podu1eyvph1zd](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025126.webp)

三维定位

![3d](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025127.webp)

检测图像中的汽车并预测3D位置。输出JSON：`[{"bbox_3d": [x_center, y_center, z_center, x_size, y_size, z_size, roll, pitch, yaw], "label": "category"}]`。

可视化展示三维定位效果

### 文档解析

将图像类的文档（如扫描件/图片PDF）解析为 QwenVL HTML 或 QwenVL Markdown 格式，该格式不仅能精准识别文本，还能获取图像、表格等元素的位置信息。Qwen3-VL模型新增解析为 Markdown 格式的能力。

> 推荐提示词如下： `qwenvl html` （解析为HTML格式）或 `qwenvl markdown` （解析为Markdown格式）

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025129.png)

qwenvl markdown。

![\-结果](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025130.webp)

**可视化展示效果**

### 视频理解

分析视频内容，如对具体事件进行定位并获取时间戳、生成关键时间段的摘要等。

请你描述下视频中的人物的一系列动作，以JSON格式输出开始时间（start\_time）、结束时间（end\_time）、事件（event），请使用HH:mm:ss表示时间戳。

{

"events": \[

{

"start\_time": "00:00:00",

"end\_time": "00:00:05",

"event": "人物手持一个纸箱走向桌子，并将纸箱放在桌上。"

},

{

"start\_time": "00:00:05",

"end\_time": "00:00:15",

"event": "人物拿起扫描枪，对准纸箱上的标签进行扫描。"

},

{

"start\_time": "00:00:15",

"end\_time": "00:00:21",

"event": "人物将扫描枪放回原位，然后拿起笔在笔记本上记录信息。"}\]

}

## 核心能力

### 开启/关闭思考模式

-   `qwen3.8`、`qwen3.7`、`qwen3.6`、`qwen3.5`、`qwen3-vl-plus`、`qwen3-vl-flash`系列模型属于混合思考模型，模型可以在思考后回复，也可直接回复；通过`enable_thinking`参数控制是否开启思考模式：
    
    -   `true`：开启思考模式。`qwen3.8`、`qwen3.7`、`qwen3.6`、`qwen3.5`系列模型默认为`true`。
    -   `false`：关闭思考模式。`qwen3-vl-plus`、`qwen3-vl-flash`系列模型默认为`false`。
-   `qwen3-vl-235b-a22b-thinking`等带`thinking`后缀的属于仅思考模型，模型总会在回复前进行思考，且无法关闭。
    

**重要**

-   **模型配置：**在非 Agent 工具调用的通用对话场景下，为保持最佳效果，建议不设置`System Message`，可将模型角色设定、输出格式要求等指令通过`User Message` 传入。
-   **优先使用流式输出：** 开启思考模式时，支持**流式和非流式**两种输出方式。为避免因响应内容过长导致超时，建议优先使用流式输出方式。
-   **限制思考长度：**深度思考模型有时会输出冗长的推理过程，可使用 `thinking_budget` 参数限制思考过程的长度。若模型思考过程生成的 Token 数超过`thinking_budget`，推理内容会进行截断并立刻开始生成最终回复内容。`thinking_budget` 默认值为模型的最大思维链长度，请参见模型列表。

#### OpenAI 兼容

`enable_thinking`非 OpenAI 标准参数，若使用 OpenAI Python SDK请通过 `extra_body`传入。

python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # 通过enable_thinking参数切换思考模式
    extra_body={
        'enable_thinking': enable_thinking,
        "thinking_budget": 81920},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

javascript

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.7-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking,
          thinking_budget: 81920

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.8-max",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true,
    "thinking_budget": 81920
}'
```

#### DashScope

python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

enable_thinking=True
messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.8-max",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # 通过enable_thinking参数切换思考模式
    enable_thinking=enable_thinking,
    # thinking_budget 参数设置最大推理过程 Token 数
    thinking_budget=81920,

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk is not None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 打印完整思考过程与回复
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .thinkingBudget(81920)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "thinking_budget": 81920
    }
}'
```

### 多图像输入

视觉理解模型支持在单次请求中传入多张图片，可用于**商品对比、多页文档处理**等任务。实现时只需在`user message` 的`content`数组中包含多个图片对象即可。

**重要**图片数量受模型图文总 Token 上限的限制，所有图片和文本的总 Token 数必须小于模型的最大输入。

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
       {"role": "user","content": [
           {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
           {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},},
           {"type": "text", "text": "这些图描绘了什么内容？"},
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

### 返回结果

```
图1中是一位女士和一只拉布拉多犬在海滩上互动的场景。女士穿着格子衬衫，坐在沙滩上，与狗进行握手的动作，背景是海浪和天空，整个画面充满了温馨和愉快的氛围。

图2中是一只老虎在森林中行走的场景。老虎的毛色是橙色和黑色条纹相间，它正向前迈步，周围是茂密的树木和植被，地面上覆盖着落叶，整个画面给人一种野生自然的感觉。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
          {role: "user",content: [
            {type: "image_url",image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
            {type: "image_url",image_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}},
            {type: "text", text: "这些图描绘了什么内容？" },
        ]}]
    });
    console.log(response.choices[0].message.content);
}

main()
```

### 返回结果

```
第一张图片中，一个人和一只狗在海滩上互动。人穿着格子衬衫，狗戴着项圈，他们似乎在握手或击掌。

第二张图片中，一只老虎在森林中行走。老虎的毛色是橙色和黑色条纹，背景是绿色的树木和植被。
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.8-max",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
          }
        },
        {
          "type": "text",
          "text": "这些图描绘了什么内容？"
        }
      ]
    }
  ]
}'
```

### 返回结果

```
{
  "choices": [
    {
      "message": {
        "content": "图1中是一位女士和一只拉布拉多犬在海滩上互动的场景。女士穿着格子衬衫，坐在沙滩上，与狗进行握手的动作，背景是海景和日落的天空，整个画面显得非常温馨和谐。\n\n图2中是一只老虎在森林中行走的场景。老虎的毛色是橙色和黑色条纹相间，它正向前迈步，周围是茂密的树木和植被，地面上覆盖着落叶，整个画面充满了自然的野性和生机。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 2497,
    "completion_tokens": 109,
    "total_tokens": 2606
  },
  "created": 1725948561,
  "system_fingerprint": null,
  "model": "qwen3.8-max",
  "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
            {"text": "这些图描绘了什么内容?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus', # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

### 返回结果

```
这些图片展示了一些动物和自然场景。第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走
```

#### Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import java.util.HashMap;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),
                        Collections.singletonMap("text", "这些图描绘了什么内容?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
               // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
这些图片展示了一些动物和自然场景。

1. 第一张图片：一个女人和一只狗在海滩上互动。女人穿着格子衬衫，坐在沙滩上，狗戴着项圈，伸出爪子与女人握手。
2. 第二张图片：一只老虎在森林中行走。老虎的毛色是橙色和黑色条纹，背景是树木和树叶。
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
                    {"text": "这些图展现了什么内容？"}
                ]
            }
        ]
    }
}'
```

### 返回结果

```
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "这些图片展示了一些动物和自然场景。第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走。"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "output_tokens": 81,
    "input_tokens": 1277,
    "image_tokens": 2497
  },
  "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
}
```

### 视频理解

视觉理解模型支持对视频内容进行理解，文件形式包括图像列表（视频帧）或视频文件。以下是理解在线视频或图像列表（通过URL指定）的示例代码。关于视频限制或可传入的图像列表数量限制，请参见[视频限制](raw/model-user-guide/model-experience/vision-model/vision.md)章节。

> 建议使用性能较优的最新版或近期快照版模型理解视频文件。

#### 视频文件

视觉理解模型通过从视频中提取帧序列进行内容分析。您可以通过以下两个参数控制抽帧策略：

-   **fps**：控制抽帧频率，每隔 1/fps 秒抽取一帧。取值范围为 \[0.1, 10\]，默认值为 2.0。
    
    -   高速运动场景：建议设置较高的 fps 值，以捕捉更多细节
    -   静态或长视频：建议设置较低的 fps 值，以提高处理效率
-   **max\_frames**：限制视频抽取帧的上限。当按 fps 计算的总帧数超过此限制时，系统将自动在 max\_frames 内均匀抽帧。**此参数仅在使用 DashScope SDK时可用。**
    

#### OpenAI兼容

> 使用OpenAI SDK或HTTP方式向视觉理解模型直接输入视频文件时，需要将用户消息中的 `"type"` 参数设为 `"video_url"` 。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "user",
            "content": [
                # 直接传入视频文件时，请将type的值设置为video_url
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps": 2
                },
                {
                    "type": "text",
                    "text": "这段视频的内容是什么?"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.8-max",
        messages: [
            {
                role: "user",
                content: [
                    // 直接传入视频文件时，请将type的值设置为video_url
                    {
                        type: "video_url",
                        video_url: {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        "fps": 2
                    },
                    {
                        type: "text",
                        text: "这段视频的内容是什么?"
                    }
                ]
            }
        ]
    });

    console.log(response.choices[0].message.content);
}

main();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3.8-max",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
            "fps":2
          },
          {
            "type": "text",
            "text": "这段视频的内容是什么?"
          }
        ]
      }
    ]
  }'
```

#### DashScope

Python

```
import dashscope
import os

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {"role": "user",
        "content": [
            # fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus',
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
        Map<String, Object> params = new HashMap<>();
        params.put("video", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4");
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "这段视频的内容是什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {"role": "user","content": [{"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}]}]}
}'
```

#### 图像列表

当视频以图像列表（即预先抽取的视频帧）传入时，可通过`fps`参数告知模型视频帧之间的时间间隔，这能帮助模型更准确地理解事件的顺序、持续时间和动态变化。模型支持通过 `fps` 参数指定原始视频的抽帧率，表示视频帧是每隔 1/fps 秒从原始视频中抽取的。该参数支持**Qwen3.6**、**Qwen3-VL、Qwen2.5-VL**模型。

#### OpenAI兼容

> 使用OpenAI SDK或HTTP方式向视觉理解模型输入图片列表形式的视频时，需要将用户消息中的 `"type"` 参数设为 `"video"` 。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[{"role": "user","content": [
        # 传入图像列表时，用户消息中的"type"参数为"video"
         {"type": "video","video": [
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
         "fps":2},
         {"type": "text","text": "描述这个视频的具体过程"},
    ]}]
)

print(completion.choices[0].message.content)
```

Node.js

```
// 确保之前在 package.json 中指定了 "type": "module"
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [{
            role: "user",
            content: [
                {
                    // 传入图像列表时，用户消息中的"type"参数为"video"
                    type: "video",
                    video: [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                        "fps":2
                },
                {
                    type: "text",
                    text: "描述这个视频的具体过程"
                }
            ]
        }]
    });
    console.log(response.choices[0].message.content);
}

main();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "messages": [{"role": "user","content": [{"type": "video","video": [
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                  "fps":2},
                {"type": "text","text": "描述这个视频的具体过程"}]}]
}'
```

#### DashScope

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [{"role": "user",
             "content": [
                  # 传入图像列表时，fps 参数适用于Qwen3.6、Qwen3-VL 和 Qwen2.5-VL系列模型
                 {"video":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                   "fps":2},
                 {"text": "描述这个视频的具体过程"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3.7-plus', # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages
)
print(response.output.choices[0].message.content[0]["text"])
```

Java

```
// DashScope SDK版本需要不低于2.21.10
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final String MODEL_NAME = "qwen3.8-max"; // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // 传入图像列表时，fps 参数适用于Qwen3.6、Qwen3-VL 和 Qwen2.5-VL系列模型
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"));
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL_NAME)
                .messages(Arrays.asList(userMessage)).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.8-max",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
            ],
            "fps":2

          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

### 传入本地文件（Base64 编码或文件路径）

视觉理解模型提供两种本地文件上传方式：Base64 编码上传和文件路径直接上传。可根据文件大小、SDK类型选择上传方式，具体建议请参见[如何选择文件上传方式](raw/model-user-guide/model-experience/vision-model/vision.md)；两种方式均需满足[图像限制](raw/model-user-guide/model-experience/vision-model/vision.md)中对文件的要求。

#### Base64 编码上传

将文件转换为 Base64 编码字符串，再传入模型。适用于 OpenAI 和 DashScope SDK及HTTP方式

传入 Base64 编码字符串的步骤（以图像为例）

1.  文件编码：将本地图像转换为 Base64 编码；
    
    图像转换为 Base64 编码的示例代码
    
    ```
    #  编码函数： 将本地文件转换为 Base64 编码的字符串
    import base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    # 将xxxx/eagle.png替换为你本地图像的绝对路径
    base64_image = encode_image("xxx/eagle.png")
    ```
    
2.  构建 [Data URL](https://www.rfc-editor.org/rfc/rfc2397)：格式如下：`data:[MIME_type];base64,{base64_image}`；
    
    1.  `MIME_type`需替换为实际的媒体类型，确保与[支持的图像格式](raw/model-user-guide/model-experience/vision-model/vision.md)表格中`MIME Type` 的值匹配（如`image/jpeg`、`image/png`）；
    2.  `base64_image`为上一步生成的 Base64 字符串；
3.  调用模型：通过`image`或`image_url`参数传递`Data URL`并调用模型。
    

#### 文件路径上传

直接向模型传入本地文件路径。仅 DashScope Python 和 Java SDK支持，不支持 DashScope HTTP和OpenAI 兼容方式。

请您参考下表，结合您的编程语言与操作系统指定文件的路径。

指定文件路径（以图像为例）

**系统**

**SDK**

**传入的文件路径**

**示例**

Linux或macOS系统

Python SDK

file://{文件的绝对路径}

file:///home/images/test.png

Java SDK

Windows系统

Python SDK

file://{文件的绝对路径}

file://D:/images/test.png

Java SDK

file:///{文件的绝对路径}

file:///D:/images/test.png

#### 图像

#### 文件路径传入

Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 将xxx/eagle.png替换为你本地图像的绝对路径
local_path = "xxx/eagle.png"
image_path = f"file://{local_path}"
messages = [
                {'role':'user',
                'content': [{'image': image_path},
                            {'text': '图中描绘的是什么景象?'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus',  # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)
print(response.output.choices[0].message.content[0]["text"])
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
        String filePath = "file://"+localPath;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>(){{put("image", filePath);}},
                        new HashMap<String, Object>(){{put("text", "图中描绘的是什么景象？");}})).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

    public static void main(String[] args) {
        try {
            // 将xxx/eagle.png替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### Base64 编码传入

#### OpenAI兼容

#### Python

```
from openai import OpenAI
import os
import base64

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                    # PNG图像：  f"data:image/png;base64,{base64_image}"
                    # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                    # WEBP图像： f"data:image/webp;base64,{base64_image}"
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };
// 将xxx/eagle.png替换为你本地图像的绝对路径
const base64Image = encodeImage("xxx/eagle.png")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
            {"role": "user",
             "content": [{"type": "image_url",
                            // 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。
                           // PNG图像：  data:image/png;base64,${base64Image}
                          // JPEG图像： data:image/jpeg;base64,${base64Image}
                         // WEBP图像： data:image/webp;base64,${base64Image}
                        "image_url": {"url": `data:image/png;base64,${base64Image}`},},
                        {"type": "text", "text": "图中描绘的是什么景象?"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.8-max",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."}},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

#### DashScope

#### Python

```
import base64
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxxx/eagle.png")

messages = [
    {
        "role": "user",
        "content": [
            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
            # PNG图像：  f"data:image/png;base64,{base64_image}"
            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
            # WEBP图像： f"data:image/webp;base64,{base64_image}"
            {"image": f"data:image/png;base64,{base64_image}"},
            {"text": "图中描绘的是什么景象?"},
        ],
    },
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages,
)
print(response.output.choices[0].message.content[0]["text"])
```

#### Java

```
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
   static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static String encodeImageToBase64(String imagePath) throws IOException {
        Path path = Paths.get(imagePath);
        byte[] imageBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void callWithLocalFile(String localPath) throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Image = encodeImageToBase64(localPath); // Base64编码

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        new HashMap<String, Object>() {{ put("image", "data:image/png;base64," + base64Image); }},
                        new HashMap<String, Object>() {{ put("text", "图中描绘的是什么景象？"); }}
                )).build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/eagle.png 替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
               {"text": "图中描绘的是什么景象?"}
                ]
            }
        ]
    }
}'
```

#### 视频文件

以保存在本地的[test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250118/hcgaks/test.mp4)为例。

#### 文件路径传入

Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 将xxxx/test.mp4替换为你本地视频的绝对路径
local_path = "xxx/test.mp4"
video_path = f"file://{local_path}"
messages = [
                {'role':'user',
                # fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                'content': [{'video': video_path,"fps":2},
                            {'text': '这段视频描绘的是什么景象？'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus',
    messages=messages)
print(response.output.choices[0].message.content[0]["text"])
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
        String filePath = "file://"+localPath;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>()
                                       {{
                                           put("video", filePath);// fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                                           put("fps", 2);
                                       }},
                        new HashMap<String, Object>(){{put("text", "这段视频描绘的是什么景象？");}})).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

    public static void main(String[] args) {
        try {
            // 将xxxx/test.mp4替换为你本地视频的绝对路径
            callWithLocalFile("xxx/test.mp4");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### Base64 编码传入

#### OpenAI兼容

#### Python

```
from openai import OpenAI
import os
import base64

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

# 将xxxx/test.mp4替换为你本地视频的绝对路径
base64_video = encode_video("xxx/test.mp4")
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    # 直接传入视频文件时，请将type的值设置为video_url
                    "type": "video_url",
                    "video_url": {"url": f"data:video/mp4;base64,{base64_video}"},
                    "fps":2
                },
                {"type": "text", "text": "这段视频描绘的是什么景象？"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeVideo = (videoPath) => {
    const videoFile = readFileSync(videoPath);
    return videoFile.toString('base64');
  };
// 将xxxx/test.mp4替换为你本地视频的绝对路径
const base64Video = encodeVideo("xxx/test.mp4")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",
        messages: [
            {"role": "user",
             "content": [{
                 // 直接传入视频文件时，请将type的值设置为video_url
                "type": "video_url",
                "video_url": {"url": `data:video/mp4;base64,${base64Video}`},
                "fps":2},
                 {"type": "text", "text": "这段视频描绘的是什么景象？"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.8-max",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},"fps":2},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

#### DashScope

#### Python

```
import base64
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

# 将xxxx/test.mp4替换为你本地视频的绝对路径
base64_video = encode_video("xxxx/test.mp4")

messages = [{'role':'user',
            # fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
             'content': [{'video': f"data:video/mp4;base64,{base64_video}","fps":2},
                            {'text': '这段视频描绘的是什么景象？'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus',
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

#### Java

```
import java.io.IOException;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    private static String encodeVideoToBase64(String videoPath) throws IOException {
        Path path = Paths.get(videoPath);
        byte[] videoBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(videoBytes);
    }

    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Video = encodeVideoToBase64(localPath); // Base64编码

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>()
                                       {{
                                           put("video", "data:video/mp4;base64," + base64Video);// fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                                           put("fps", 2);
                                       }},
                        new HashMap<String, Object>(){{put("text", "这段视频描绘的是什么景象？");}})).build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/test.mp4 替换为你本地视频的绝对路径
            callWithLocalFile("xxx/test.mp4");
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"f"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"video": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
               {"text": "这段视频描绘的是什么景象? "}
                ]
            }
        ]
    }
}'
```

#### 图像列表

以保存在本地的[football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vzfwkh/football1.jpg)、[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vgkgqy/football2.jpg)、[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/mgvhvh/football3.jpg)、[football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/bydzjh/football4.jpg)为例。

#### 文件路径传入

Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

local_path1 = "football1.jpg"
local_path2 = "football2.jpg"
local_path3 = "football3.jpg"
local_path4 = "football4.jpg"

image_path1 = f"file://{local_path1}"
image_path2 = f"file://{local_path2}"
image_path3 = f"file://{local_path3}"
image_path4 = f"file://{local_path4}"

messages = [{'role':'user',
              #  传入图像列表时，fps 参数适用于Qwen3.6、Qwen3-VL 和 Qwen2.5-VL系列模型
             'content': [{'video': [image_path1,image_path2,image_path3,image_path4],"fps":2},
                            {'text': '这段视频描绘的是什么景象?'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.7-plus',  # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

Java

```
// DashScope SDK版本需要不低于2.21.10
import java.util.Arrays;
import java.util.Map;
import java.util.Collections;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final String MODEL_NAME = "qwen3.8-max";  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    public static void videoImageListSample(String localPath1, String localPath2, String localPath3, String localPath4)
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        String filePath1 = "file://" + localPath1;
        String filePath2 = "file://" + localPath2;
        String filePath3 = "file://" + localPath3;
        String filePath4 = "file://" + localPath4;
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList(filePath1,filePath2,filePath3,filePath4));
        //  传入图像列表时，fps 参数适用于Qwen3.6、Qwen3-VL 和 Qwen2.5-VL系列模型
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL_NAME)
                .messages(Arrays.asList(userMessage)).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample(
                    "xxx/football1.jpg",
                    "xxx/football2.jpg",
                    "xxx/football3.jpg",
                    "xxx/football4.jpg");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### Base64 编码传入

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI
import base64

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image1 = encode_image("football1.jpg")
base64_image2 = encode_image("football2.jpg")
base64_image3 = encode_image("football3.jpg")
base64_image4 = encode_image("football4.jpg")
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.8-max",  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
    {"role": "user","content": [
        {"type": "video","video": [
            f"data:image/jpeg;base64,{base64_image1}",
            f"data:image/jpeg;base64,{base64_image2}",
            f"data:image/jpeg;base64,{base64_image3}",
            f"data:image/jpeg;base64,{base64_image4}",]},
        {"type": "text","text": "描述这个视频的具体过程"},
    ]}]
)
print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };

const base64Image1 = encodeImage("football1.jpg")
const base64Image2 = encodeImage("football2.jpg")
const base64Image3 = encodeImage("football3.jpg")
const base64Image4 = encodeImage("football4.jpg")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max", // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
            {"role": "user",
             "content": [{"type": "video",
                        "video": [
                            `data:image/jpeg;base64,${base64Image1}`,
                            `data:image/jpeg;base64,${base64Image2}`,
                            `data:image/jpeg;base64,${base64Image3}`,
                            `data:image/jpeg;base64,${base64Image4}`]},
                        {"type": "text", "text": "这段视频描绘的是什么景象？"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "messages": [{"role": "user",
                "content": [{"type": "video",
                "video": [
                          "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
                          "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
                          "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
                          "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."
                          ]},
                {"type": "text",
                "text": "描述这个视频的具体过程"}]}]
}'
```

#### DashScope

#### Python

```
import base64
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image1 = encode_image("football1.jpg")
base64_image2 = encode_image("football2.jpg")
base64_image3 = encode_image("football3.jpg")
base64_image4 = encode_image("football4.jpg")

messages = [{'role':'user',
             'content': [
                    {'video':
                         [f"data:image/jpeg;base64,{base64_image1}",
                          f"data:image/jpeg;base64,{base64_image2}",
                          f"data:image/jpeg;base64,{base64_image3}",
                          f"data:image/jpeg;base64,{base64_image4}"
                         ]
                    },
                    {'text': '请描绘这个视频的具体过程?'}]}]
response = MultiModalConversation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3.7-plus',  # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

#### Java

```
import java.io.IOException;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static String encodeImageToBase64(String imagePath) throws IOException {
        Path path = Paths.get(imagePath);
        byte[] imageBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void videoImageListSample(String localPath1,String localPath2,String localPath3,String localPath4)
            throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Image1 = encodeImageToBase64(localPath1); // Base64编码
        String base64Image2 = encodeImageToBase64(localPath2);
        String base64Image3 = encodeImageToBase64(localPath3);
        String base64Image4 = encodeImageToBase64(localPath4);

        MultiModalConversation conv = new MultiModalConversation();
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList(
                        "data:image/jpeg;base64," + base64Image1,
                        "data:image/jpeg;base64," + base64Image2,
                        "data:image/jpeg;base64," + base64Image3,
                        "data:image/jpeg;base64," + base64Image4));
        //  传入图像列表时，fps 参数适用于Qwen3.6、Qwen3-VL 和 Qwen2.5-VL系列模型
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/football1.png 等替换为你本地图像的绝对路径
            videoImageListSample(
                    "xxx/football1.jpg",
                    "xxx/football2.jpg",
                    "xxx/football3.jpg",
                    "xxx/football4.jpg"
            );
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/vision-model/vision.md)；
-   为了便于展示，代码中的`"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.8-max",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
                      "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
                      "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
                      "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
                      "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."
            ],
            "fps":2
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

### 处理高分辨率图像

视觉理解模型API对单张图像编码后的视觉 Token 数量设有限制，默认配置下，高分辨率图像会被压缩，可能丢失细节，影响理解准确性。启用 `vl_high_resolution_images` 或调整 `max_pixels` 可增加视觉 Token 数量，从而保留更多图像细节，提升理解效果。

查看每个模型视觉 Token 对应的像素、Token 上限和像素上限

> 当输入图像像素大于模型的像素上限时，会将图像进行缩小至像素上限内。

**模型**

**每Token 对应像素**

**vl\_high\_resolution\_images**

**max\_pixels**

**Token 上限**

**像素上限**

`Qwen3.8`、`Qwen3.7`、`Qwen3.6`、`Qwen3.5`、`Qwen3-VL`系列模型

`32*32`

`true`

`max_pixels` 无效

`16384 Token`

`16777216`（即`16384*32*32`）

`false`（默认）

可自定义，默认为 `2621440`，最大值是`16777216`

由 `max_pixels` 决定，即`max_pixels/32/32`

`max_pixels`

`qwen-vl-max`、`qwen-vl-plus`模型

`32*32`

`true`

`max_pixels` 无效

`16384 Token`

`16777216`（即`16384*32*32`）

`false`（默认）

可自定义，默认为`1310720`，最大值是`16777216`

由 `max_pixels` 决定，即`max_pixels/32/32`

`max_pixels`

`QVQ`系列模型

`28*28`

`true`

`max_pixels` 无效

`16384 Token`

`12845056`（即`16384*28*28`）

`false`（默认）

可自定义，默认为`1003520`，最大值是`12845056`

由 `max_pixels` 决定，即`max_pixels/28/28`

`max_pixels`

-   当`vl_high_resolution_images=true`时，API 使用固定分辨率策略，忽略`max_pixels`设置。适合用于识别图像中的精细文本、微小物体或丰富细节。
    
-   当`vl_high_resolution_images=false`时，最终的像素上限取决于 `max_pixels` 参数值。
    
    -   对成本敏感（希望减少视觉 Token 消耗）：使用`max_pixels`的默认值或设置为更小的值。`max_pixels`主要影响视觉 Token 数量与调用成本，实测对端到端响应时间没有显著影响；如需降低时延，请参见下方[响应速度与模型选型](raw/model-user-guide/model-experience/vision-model/vision.md)。
    -   需要关注一定的细节，可接受较低的处理速度：适当提高`max_pixels`的值

#### 响应速度与模型选型

在延迟敏感的场景中，响应时间主要由所选模型决定，而不是由`max_pixels`决定。`qwen-vl-max`与`qwen-vl-plus`在相同输入条件下的响应时间对比如下：

**模型**

**平均响应时间**

**特点**

`qwen-vl-max`

约 12s

识别精度更高，适合细节密集、容错要求低的图像

`qwen-vl-plus`

约 8s

速度与精度平衡，比`qwen-vl-max`快约 39%

上表为单张 2480x3508 像素图像在默认参数（`vl_high_resolution_images=false`）下的实测参考值：`qwen-vl-max`两次调用分别为 12.75s、11.84s，平均 12.29s；`qwen-vl-plus`两次调用分别为 8.29s、6.75s，平均 7.52s。实际耗时随图像尺寸、输出长度和网络状况变化，仅供量级参考，不构成性能承诺。

-   启用流式输出（`stream=True`）可显著降低首字延迟：同一请求下首个 Token 约 0.95s 返回，完整响应的总耗时不变。适合需要尽快向用户反馈的交互式场景。
-   工作流等对时延敏感的图片识别场景：建议使用`qwen-vl-plus`并开启`stream=True`，可在约 1 秒内拿到首字响应；仅当`qwen-vl-plus`的识别准确度不满足要求时，再切换到`qwen-vl-max`。调小`max_pixels`不是提速手段——实测中`max_pixels=16384`为 18.59s、`max_pixels=65536`为 13.22s，与默认值下的 12.29s 基本持平甚至更慢。

#### OpenAI 兼容

`vl_high_resolution_images`非 OpenAI 标准参数，在不同语言的SDK中传递方式存在差异：

-   **Python SDK:**必须通过 `extra_body` 字典传递
-   **Node.js SDK:**可作为顶层参数直接传递

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role": "user","content": [
            {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
            # max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            # "max_pixels": 16384 * 32 * 32
            },
           {"type": "text", "text": "这张图表现的是哪个节日的氛围？"},
            ],
        }
    ],
    extra_body={"vl_high_resolution_images":True}

)
print(f"模型输出结果: {completion.choices[0].message.content}")
print(f"输入总Tokens: {completion.usage.prompt_tokens}")
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
 const response = await openai.chat.completions.create({
        model: "qwen3.8-max",
        messages: [
        {role: "user",content: [
            {type: "image_url",
            image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
            // max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，不生效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            // "max_pixels": 2560 * 32 * 32
            },
            {type: "text", text: "这张图表现的是哪个节日的氛围？" },
        ]}],
        vl_high_resolution_images:true
    })

console.log("模型输出结果：",response.choices[0].message.content);
console.log("输入总Tokens",response.usage.prompt_tokens);
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.8-max",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"
          }
        },
        {
          "type": "text",
          "text": "这张图表现的是哪个节日的氛围？"
        }
      ]
    }
  ],
  "vl_high_resolution_images":true
}'
```

#### DashScope

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg",
            # max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            # "max_pixels": 16384 * 32 * 32
            },
            {"text": "这张图表现的是哪个节日的氛围？"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.7-plus',
        messages=messages,
        vl_high_resolution_images=True
    )

print("模型输出",response.output.choices[0].message.content[0]["text"])
print("输入总Tokens：",response.usage.input_tokens)
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map<String, Object> map = new HashMap<>();
        map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg");
        // max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
        // map.put("max_pixels", 2621440);
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map,
                        Collections.singletonMap("text", "这张图表现的是哪个节日的氛围？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .message(userMessage)
                .vlHighResolutionImages(true)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        System.out.println(result.getUsage().getInputTokens());
    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"
                },
               {"text": "这张图表现的是哪个节日的氛围？"}
                ]
            }
        ]
    },
    "parameters": {
        "vl_high_resolution_images": true
    }
}'
```

### 更多用法

-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#36eaa79f55dz7)
-   [流式输出](https://help.aliyun.com/zh/model-studio/stream#e98db795e87q9)

## 使用限制

### 输入文件限制

#### 图像限制

-   **图像分辨率：**
    -   最小尺寸：图像的宽度和高度均须大于`10`像素。
        
    -   宽高比：原图及缩放后的图像，长边与短边的比值不得超过 `200:1`。
        
        > 图像缩放逻辑请参见 [计算图像的Token](raw/model-user-guide/model-experience/vision-model/vision.md) 中 `smart_resize` 函数。
        
    -   像素上限：
        
        -   推荐将图像分辨率控制在`8K(7680x4320)`以内。超过此分辨率的图像可能因文件过大、网络传输耗时过长而导致API调用超时。
        -   自动缩放机制：模型可通过`max_pixels`和`min_pixels`调整图像大小；因此，提供超高分辨率的图像并不会提升识别精度，反而会增加调用失败的风险，建议在客户端提前将图像缩放至合理大小。
-   **支持的图像格式**
    -   分辨率在4K `(3840x2160)`以下，支持的图像格式如下：
        
        **图像格式**
        
        **常见扩展名**
        
        **MIME Type**
        
        BMP
        
        .bmp
        
        image/bmp
        
        JPEG
        
        .jpe, .jpeg, .jpg
        
        image/jpeg
        
        PNG
        
        .png
        
        image/png
        
        TIFF
        
        .tif, .tiff
        
        image/tiff
        
        WEBP
        
        .webp
        
        image/webp
        
        HEIC
        
        .heic
        
        image/heic
        
    -   分辨率处于`4K(3840x2160)`到`8K(7680x4320)`范围，仅支持 JPEG、JPG 、PNG 格式
        
-   **图像大小：**
    
    -   以公网URL传入时：Qwen3.8系列、Qwen3.7系列、Qwen3.6系列、Qwen3.5系列、Qwen3-VL系列单个图像不超过 `20MB`，其他模型单个图像不超过`10MB`
    -   以本地路径传入时：单个图像不超过`10MB`
    -   以 Base64 编码传入时（OpenAI 兼容接口或DashScope）：Qwen3.8系列、Qwen3.7系列、Qwen3.6系列、Qwen3.5、Qwen3-VL系列编码前的原始图像文件不超过 `20MB`，其他模型不超过`10MB`；且编码后的 Data URI 字符串不超过 `20MB`。
    -   以 Base64 编码传入时（Anthropic 兼容接口）：受**请求体整体不超过**`6MB` 的限制，**多张图像**时需共享此额度。
    
    上述限制取决于所选模型，不支持通过购买高级套餐或升级模型版本提升。
    
    > 如需压缩文件体积请参见 [如何将图像或视频压缩到满足要求的大小](raw/model-user-guide/model-experience/vision-model/vision.md) 。
    
-   **图片数量限制：**多图输入时根据传入方式不同，支持的图片数量上限有所区别：
    
    -   以公网URL或本地路径传入时：
        
        -   Qwen3.8-Max、Qwen3.8-Flash、Qwen3.7-Plus：最多 2048 张
        -   Qwen3.7-Flash、Qwen3.6-Plus、Qwen3.6-Flash、Qwen3.5-Plus、Qwen3.5-Flash、Qwen3-VL、Qwen-VL、QVQ系列：最多 256 张
    -   以 Base64 编码传入时：最多 250 张
        
    
    Qwen-Omni系列模型请参考[全模态](raw/model-user-guide/model-experience/omni-modal/omni.md)。
    

> 同时受模型图文总 Token 上限（即最大输入）的限制，所有图片的总 Token 数必须小于模型的最大输入。

#### 视频限制

-   **以图像列表传入，图像列表的数量有如下限制：**
    -   `qwen3.8`系列、`qwen3.7`系列、`qwen3.6`系列、`qwen3.5` 系列：最少传入 4 张图片，最多 8000 张图片
    -   `qwen3-vl-plus` 系列、`qwen3-vl-flash` 系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：最少传入 4 张图片，最多 2000 张图片
    -   其他`Qwen3-VL`开源、`Qwen2.5-VL`（包括商业版和开源版）和`QVQ`系列模型：最少传入 4 张图片，最多 512 张图片
    -   其他模型：最少传入 4 张图片，最多 80 张图片
-   **以视频文件传入时：**
    -   **视频大小：**
        
        -   以公网URL传入时：
            
            -   `qwen3.8`系列、`qwen3.7`系列、`qwen3.6`系列、`qwen3.5` 系列、`Qwen3-VL`系列、`qwen-vl-max` ：不超过 2GB；
            -   `qwen-vl-plus` 系列、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：不超过 1GB；
            -   其他模型不超过 150MB
        -   以 Base64 编码传入时：编码后的字符串小于 10MB；
            
        -   以本地文件路径传入时：视频本身不超过 100MB。
            
        
        > 如需压缩文件体积请参见 [如何将图像或视频压缩到满足要求的大小](raw/model-user-guide/model-experience/vision-model/vision.md) 。
        
    -   **视频时长：**
        -   `qwen3.8`系列、`qwen3.7`系列、`qwen3.6`系列、`qwen3.5` 系列：2秒至2小时；
        -   `qwen3-vl-plus`系列、`qwen3-vl-flash`系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：2 秒至 1 小时；
        -   其他`Qwen3-VL`开源系列、`qwen-vl-max` ：2 秒至 20 分钟；
        -   `qwen-vl-plus`系列、 其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：2 秒至 10 分钟；
        -   其他模型：2 秒至 40 秒。
    -   **视频格式：** MP4、AVI、MKV、MOV、FLV、WMV 等。
        
    -   **视频尺寸：**无特定限制，模型可通过`max_pixels`和`min_pixels`自动调整视频尺寸，更大尺寸的视频文件不会有更好的理解效果。
        
    -   **视频数量限制：**最多可传入 64 个视频。
        
    -   **音频理解：**不支持对视频文件的音频进行理解。
        

### 文件传入方式

-   **公网URL**：提供一个公网可访问的文件地址，支持HTTP或HTTPS协议。为获得最佳稳定性和性能，可将文件[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/console-quick-start)或[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)，获取公网 URL。**百炼**服务无法访问 OSS 内网地址（endpoint 中带 `-internal`，如 `https://<bucket>.oss-cn-hangzhou-internal.aliyuncs.com/image.jpg`），传入内网地址会导致文件下载失败，返回 `InvalidParameter`，message 为 `Failed to download multimodal content`。请改用 OSS 公网域名（如 `https://<bucket>.oss-cn-hangzhou.aliyuncs.com/image.jpg`）或 OSS 临时签名 URL 传入文件。
    
    **重要**为确保模型能成功下载文件，提供的公网URL的响应头中**必须**包含 Content-Length（文件大小）和 Content-Type（媒体类型，如 image/jpeg）。任一字段缺失或者错误将会导致文件下载失败。
    
-   **Base64编码传入：**将文件转换为 Base64 编码字符串再传入。
    
-   **本地文件路径传入（仅限 DashScope SDK）：**传入本地文件的路径。
    

> 关于文件传入方式的建议，请参见 [如何选择文件上传方式？](raw/model-user-guide/model-experience/vision-model/vision.md)

## 应用于生产环境

-   **图像/视频预处理：**视觉理解模型对输入的文件有大小限制，如需压缩文件请参见[图像或视频压缩方法](raw/model-user-guide/model-experience/vision-model/vision.md)。
    
-   **处理文本文件：**视觉理解模型仅支持输入文本、图像和视频，不支持直接处理 TXT、Word（.doc/.docx）、PDF 等文本文件。如需处理文本文件，可使用以下替代方案：
    
    -   将文本文件转换为图片格式，建议使用图像处理库（如Python的pdf2image）将文件按页转换为多张高质量的图片，再使用[多图像输入](raw/model-user-guide/model-experience/vision-model/vision.md)方式传入模型。
    -   使用[Qwen-Long](raw/model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md)模型，该模型支持上传文档并通过文件ID传入信息并对话。
-   **异步与批量处理：**对于大规模、非实时的图像或视频处理任务，推荐使用[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)的方式（仅支持部分模型）。此方式以异步方式处理任务，并提供50%的成本折扣。
    
-   **容错与稳定性**
    -   超时处理：非流式调用的最大超时时间不少于300秒，实际时长因部署区域与选用模型存在差异。为了提升用户体验，超时后响应体中会将已生成的内容返回。如果响应头包含`x-dashscope-partialresponse：true`，表示本次响应触发了超时。您可以使用[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)功能（支持部分模型），将已生成的内容添加到 messages 数组并再次发出请求，使大模型继续生成内容。详情请参见：[基于不完整输出进行续写](https://help.aliyun.com/zh/model-studio/partial-mode#8cc28acfd7a91)。
    -   客户端超时配置：上文的超时是**服务端**限制，SDK 客户端本身也有默认超时时间。处理大尺寸图片（如 4000x4000 像素）时，请求耗时可能超过客户端默认超时时间，从而抛出 `APITimeoutError`。客户端超时与服务端超时是两个独立的限制，需要分别处理。使用 OpenAI Python SDK 时，可通过 `with_options` 延长客户端超时时间：

```
client = client.with_options(timeout=1800.0)
response = client.chat.completions.create(
    model="qwen-vl-plus",
    messages=[...]
)
```

-   使用流式输出：将 `stream` 参数设置为 `True` 后，内容会逐步返回，避免长时间等待单个完整响应而触发客户端超时：

```
stream = client.chat.completions.create(
    model="qwen-vl-plus",
    messages=[...],
    stream=True
)
for chunk in stream:
    print(chunk.choices[0].delta.content)
```

-   重试机制：设计合理的API调用重试逻辑（如指数退避），以应对网络波动或服务瞬时不可用的情况。

## 计费与限流

-   **计费 ：**总费用根据输入和输出的总 Token 数计算；输入和输出价格可参见百炼控制台。
    
    -   **Token 构成：**输入 Token 由文本 Token 和图像或视频转换后的 Token 组成；输出 Token 为模型生成的文本。在思考模式下，模型的思考过程也会计入输出 Token。若思考模式下未输出思考过程，按照非思考模式价格计费。
        
    -   **计算图像与视频的Token：**可通过以下代码计算图像或视频的 Token 消耗。估算结果仅供参考，实际用量以API响应为准。
        
        计算图像与视频的Token
        
        #### 图像
        
        计算公式：`图像 Token = h_bar * w_bar / token_pixels + 2`
        
        -   `h_bar、w_bar`：缩放后的图像长宽，模型在处理图像前会进行预处理，会将图像缩小至特定像素上限内，像素上限与`max_pixels`和`vl_high_resolution_images`参数的取值有关，相关章节：[处理高分辨率图像](raw/model-user-guide/model-experience/vision-model/vision.md)。
            
        -   `token_pixels`：每视觉`Token`对应的像素值，不同模型情况不同：
            
            -   `qwen3.8系列`、`qwen3.7系列`、`qwen3.6系列`、`qwen3.5系列`、`Qwen3-VL`、`qwen-vl-max`、`qwen-vl-plus`**：**每个`Token`对应 `32x32`像素
            -   `QVQ`及其他`Qwen2.5-VL`模型**：**每个Token对应`28x28`像素
        
        以下代码演示了模型内部对图像的大致缩放逻辑，可用于估算一张图像的Token，实际计费请以API响应为准。
        
        ```
        import math
        from PIL import Image  # pip install Pillow
        
        def smart_resize(image_path, max_pixels, vl_high_resolution_images):
            """根据模型参数，计算图像缩放后的尺寸，用于估算图像 Token。"""
            image = Image.open(image_path)
            height, width = image.height, image.width
        
            # Qwen3.6、Qwen3.5、Qwen3-VL 等模型的缩放因子为 32；其他模型为 28
            factor = 32
            h_bar = round(height / factor) * factor
            w_bar = round(width / factor) * factor
        
            # Token 下限：4 个 Token
            min_pixels = 4 * factor * factor
        
            # vl_high_resolution_images=True 时，Token 上限固定为 16384，忽略 max_pixels
            if vl_high_resolution_images:
                max_pixels = 16384 * factor * factor
        
            # 将总像素数约束在 [min_pixels, max_pixels] 范围内
            if h_bar * w_bar > max_pixels:
                beta = math.sqrt((height * width) / max_pixels)
                h_bar = math.floor(height / beta / factor) * factor
                w_bar = math.floor(width / beta / factor) * factor
            elif h_bar * w_bar < min_pixels:
                beta = math.sqrt(min_pixels / (height * width))
                h_bar = math.ceil(height * beta / factor) * factor
                w_bar = math.ceil(width * beta / factor) * factor
        
            return h_bar, w_bar
        
        if __name__ == "__main__":
            # 注意：max_pixels 和 vl_high_resolution_images 的值需要与调用模型时传入的参数保持一致
            h_bar, w_bar = smart_resize("xxx/test.jpg", max_pixels=2560 * 32 * 32, vl_high_resolution_images=False)
            print(f"缩放后的图像尺寸：高度 {h_bar}，宽度 {w_bar}")
        
            # 每张图像额外包含 <vision_bos> 和 <vision_eos> 各 1 个 Token
            token = int(h_bar * w_bar / (32 * 32)) + 2
            print(f"图像的 Token 数：{token}")
        ```
        
        #### 视频
        
        -   **视频文件：**
            
            模型处理视频文件时，会先进行抽帧，然后计算所有视频帧的总 Token 数。由于该计算过程较为复杂，可使用以下代码，通过传入视频路径来估算视频消耗的总 Token 数：
            
        
        ```
        # 使用前安装：pip install opencv-python
        import math
        import os
        import logging
        import cv2
        
        logger = logging.getLogger(__name__)
        
        FRAME_FACTOR = 2
        
        # Qwen3.6、Qwen3.5、Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710等模型，图像缩放因子为32
        IMAGE_FACTOR = 32
        
        #  其他模型，图像缩放因子为28
        # IMAGE_FACTOR = 28
        
        # 视频帧的最大长宽比
        MAX_RATIO = 200
        # 视频帧的像素下限
        VIDEO_MIN_PIXELS = 4 * 32 * 32
        # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
        VIDEO_MAX_PIXELS = 640 * 32 * 32
        
        # 用户未传入FPS参数，则fps使用默认值
        FPS = 2.0
        # 最少抽取帧数
        FPS_MIN_FRAMES = 4
        # 最大抽取帧数（根据模型选择设置值）
        FPS_MAX_FRAMES = 2000
        
        # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请将VIDEO_TOTAL_PIXELS设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
        VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_TOTAL_PIXELS', 131072 * 32 * 32)))
        
        def round_by_factor(number: int, factor: int) -> int:
            """返回与”number“最接近的整数，该整数可被”factor“整除。"""
            return round(number / factor) * factor
        
        def ceil_by_factor(number: int, factor: int) -> int:
            """返回大于或等于“number”且可被“factor”整除的最小整数。"""
            return math.ceil(number / factor) * factor
        
        def floor_by_factor(number: int, factor: int) -> int:
            """返回小于或等于“number”且可被“factor”整除的最大整数。"""
            return math.floor(number / factor) * factor
        
        def extract_vision_info(conversations):
            vision_infos = []
            if isinstance(conversations[0], dict):
                conversations = [conversations]
            for conversation in conversations:
                for message in conversation:
                    if isinstance(message["content"], list):
                        for ele in message["content"]:
                            if (
                                "image" in ele
                                or "image_url" in ele
                                or "video" in ele
                                or ele.get("type","") in ("image", "image_url", "video")
                            ):
                                vision_infos.append(ele)
            return vision_infos
        
        def smart_nframes(ele,total_frames,video_fps):
            """用于计算抽取的视频帧数。
        
            Args:
                ele (dict): 包含视频配置的字典格式
                    - fps: fps用于控制提取模型输入帧的数量。
                total_frames (int): 视频的原始总帧数。
                video_fps (int | float): 视频的原始帧率
        
            Raises:
                nframes应该在[FRAME_FACTOR，total_frames]间隔内，否则会报错
        
            Returns:
                用于模型输入的视频帧数。
            """
            assert not ("fps" in ele and "nframes" in ele), "Only accept either `fps` or `nframes`"
            fps = ele.get("fps", FPS)
            min_frames = ceil_by_factor(ele.get("min_frames", FPS_MIN_FRAMES), FRAME_FACTOR)
            max_frames = floor_by_factor(ele.get("max_frames", min(FPS_MAX_FRAMES, total_frames)), FRAME_FACTOR)
            duration = total_frames / video_fps if video_fps != 0 else 0
            if duration-int(duration)>(1/fps):
                total_frames = math.ceil(duration * video_fps)
            else:
                total_frames = math.ceil(int(duration)*video_fps)
            nframes = total_frames / video_fps * fps
            if nframes > total_frames:
                logger.warning(f"smart_nframes: nframes[{nframes}] > total_frames[{total_frames}]")
            nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
            if not (FRAME_FACTOR <= nframes and nframes <= total_frames):
                raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
        
            return nframes
        
        def get_video(video_path):
            # 获取视频信息
            cap = cv2.VideoCapture(video_path)
        
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # 获取视频高度
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            return frame_height, frame_width, total_frames, video_fps
        
        def smart_resize(ele, path, factor=IMAGE_FACTOR):
            # 获取原视频的宽和高
            height, width, total_frames, video_fps = get_video(path)
            # 视频帧的Token下限
            min_pixels = VIDEO_MIN_PIXELS
            total_pixels = VIDEO_TOTAL_PIXELS
            # 抽取的视频帧数
            nframes = smart_nframes(ele, total_frames, video_fps)
            max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR),int(min_pixels * 1.05))
        
            # 视频的长宽比不应超过200:1或1:200
            if max(height, width) / min(height, width) > MAX_RATIO:
                raise ValueError(
                    f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}"
                )
        
            h_bar = max(factor, round_by_factor(height, factor))
            w_bar = max(factor, round_by_factor(width, factor))
            if h_bar * w_bar > max_pixels:
                beta = math.sqrt((height * width) / max_pixels)
                h_bar = floor_by_factor(height / beta, factor)
                w_bar = floor_by_factor(width / beta, factor)
            elif h_bar * w_bar < min_pixels:
                beta = math.sqrt(min_pixels / (height * width))
                h_bar = ceil_by_factor(height * beta, factor)
                w_bar = ceil_by_factor(width * beta, factor)
            return h_bar, w_bar
        
        def token_calculate(video_path, fps):
            # 传入视频路径和fps抽帧参数
            messages = [{"content": [{"video": video_path, "fps": fps}]}]
            vision_infos = extract_vision_info(messages)[0]
        
            resized_height, resized_width = smart_resize(vision_infos, video_path)
        
            height, width, total_frames, video_fps = get_video(video_path)
            num_frames = smart_nframes(vision_infos, total_frames, video_fps)
            print(f"原视频尺寸：{height}*{width}， 输入模型的尺寸：{resized_height}*{resized_width}，视频总帧数:{total_frames}，fps等于{fps}时，抽取的总帧数：{num_frames}", end="，")
            video_token = int(math.ceil(num_frames / 2) * resized_height / 32 * resized_width / 32)
            video_token += 2   # 系统会自动添加<|vision_bos|>和<|vision_eos|>视觉标记（各计1个Token）
            return video_token
        
        video_token = token_calculate("xxx/test.mp4", 1)
        print("视频tokens:", video_token)
        ```
        
        -   **图像列表：**
            
            当以图像列表形式传入视频时，表示已预先完成视频抽帧，可使用以下代码，通过传入图像的路径和数量来计算传入图像列表时消耗的Token数：
            
        
        ```
        # 使用前安装：pip install Pillow
        import math
        import os
        import logging
        from typing import Tuple
        from PIL import Image
        
        logger = logging.getLogger(__name__)
        
        # ==================== 常量定义 ====================
        FRAME_FACTOR = 2
        # Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710模型，缩放因子为32
        IMAGE_FACTOR = 32
        
        #  其他模型，缩放因子为28
        # IMAGE_FACTOR = 28
        
        # Token计算相关常量
        TOKEN_DIVISOR = 32  # token计算时的除数
        VISION_SPECIAL_TOKENS = 2  # <|vision_bos|>和<|vision_eos|>标记
        
        # 视频帧的最大长宽比
        MAX_RATIO = 200
        # 视频帧的像素下限
        VIDEO_MIN_PIXELS = 4 * 32 * 32
        # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
        VIDEO_MAX_PIXELS = 640 * 32 * 32
        
        # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请将VIDEO_TOTAL_PIXELS设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
        VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_TOTAL_PIXELS', 131072 * 32 * 32)))
        
        def round_by_factor(number: int, factor: int) -> int:
            """返回与”number“最接近的整数，该整数可被”factor“整除。"""
            return round(number / factor) * factor
        
        def ceil_by_factor(number: int, factor: int) -> int:
            """返回大于或等于“number”且可被“factor”整除的最小整数。"""
            return math.ceil(number / factor) * factor
        
        def floor_by_factor(number: int, factor: int) -> int:
            """返回小于或等于“number”且可被“factor”整除的最大整数。"""
            return math.floor(number / factor) * factor
        
        def get_image_size(image_path: str) -> Tuple[int, int]:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图像文件不存在: {image_path}")
        
            try:
                image = Image.open(image_path)
                height = image.height
                width = image.width
                image.close()  # 及时关闭文件
                return height, width
            except Exception as e:
                raise ValueError(f"无法读取图像文件 {image_path}: {str(e)}")
        
        def smart_resize(height: int, width: int, nframes: int, factor: int = IMAGE_FACTOR) -> Tuple[int, int]:
            """
            计算图像缩放后的尺寸
        
            Args:
                height: 原始图像高度
                width: 原始图像宽度
                nframes: 视频帧数
                factor: 缩放因子，默认为IMAGE_FACTOR
        
            Returns:
                (resized_height, resized_width) 缩放后的高度和宽度
        
            Raises:
                ValueError: 长宽比超过限制
            """
            # 视频帧的Token下限
            min_pixels = VIDEO_MIN_PIXELS
            total_pixels = VIDEO_TOTAL_PIXELS
            # 抽取的视频帧数
            max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))
        
            # 视频的长宽比不应超过200:1或1:200
            aspect_ratio = max(height, width) / min(height, width)
            if aspect_ratio > MAX_RATIO:
                raise ValueError(
                    f"图像长宽比必须小于 {MAX_RATIO}:1，当前为 {aspect_ratio:.2f}:1"
                )
        
            h_bar = max(factor, round_by_factor(height, factor))
            w_bar = max(factor, round_by_factor(width, factor))
            if h_bar * w_bar > max_pixels:
                beta = math.sqrt((height * width) / max_pixels)
                h_bar = floor_by_factor(height / beta, factor)
                w_bar = floor_by_factor(width / beta, factor)
            elif h_bar * w_bar < min_pixels:
                beta = math.sqrt(min_pixels / (height * width))
                h_bar = ceil_by_factor(height * beta, factor)
                w_bar = ceil_by_factor(width * beta, factor)
            return h_bar, w_bar
        
        def calculate_video_tokens(image_path: str, nframes: int = 1, factor: int = IMAGE_FACTOR, verbose: bool = True) -> int:
            """
        
            Args:
                image_path: 视频帧文件路径
                nframes: 视频帧数，
                factor: 缩放因子，默认为IMAGE_FACTOR
                verbose: 是否打印详细信息
        
            Returns:
                所消耗的token数量
        
            Raises:
                FileNotFoundError: 文件不存在
                ValueError: 文件格式无效或长宽比超限
            """
            # 获取原始图像尺寸（只读取一次）
            height, width = get_image_size(image_path)
        
            # 计算缩放后的尺寸
            resized_height, resized_width = smart_resize(height, width, nframes, factor)
        
            # 计算token数量
            # 公式：⌈帧数/2⌉ × (高度/TOKEN_DIVISOR) × (宽度/TOKEN_DIVISOR) + VISION_SPECIAL_TOKENS
            video_token = int(
                math.ceil(nframes / 2) *
                (resized_height / TOKEN_DIVISOR) *
                (resized_width / TOKEN_DIVISOR)
            )
            # 添加视觉标记token（<|vision_bos|>和<|vision_eos|>）
            video_token += VISION_SPECIAL_TOKENS
        
            if verbose:
                print(f"原视频帧尺寸：{height}×{width}，输入模型的尺寸：{resized_height}×{resized_width}，", end="")
        
            return video_token
        
        if __name__ == "__main__":
            try:
                video_token = calculate_video_tokens("xxx/test.jpg", nframes=30)
                print(f"视频tokens: {video_token}\n")
            except Exception as e:
                print(f"错误: {str(e)}\n")
        ```
        
-   **查看账单：**您可以在阿里云控制台的[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面查看账单或进行充值。
    
-   **限流：**视觉理解模型的限流条件参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   **免费额度（仅北京地域）（仅新加坡地域）**：从开通百炼或模型申请通过之日起计算有效期，有效期 90 天内，视觉理解模型提供 100 万 Token 的免费额度。
    

## API参考

关于视觉理解模型的输入输出参数，请参见[文本生成](raw/model-api-reference/qwen-api-reference.md)。

## 常见问题

如何选择文件上传方式？

推荐综合考虑SDK类型、文件大小以及网络稳定性来选择最合适的上传方式。

**文件类型**

**文件规格**

**DashScope SDK（Python、Java）**

**OpenAI 兼容 / DashScope HTTP**

图像

大于 7MB 小于 10MB

传入本地路径

仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss)

小于 7MB

传入本地路径

Base64 编码

视频

大于 100 MB

仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss)

仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss)

大于 7MB 小于 100 MB

传入本地路径

仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss)

小于 7MB

传入本地路径

Base64 编码

> Base64 编码会增大数据体积，原始文件大小应小于 7 MB。

> 使用 Base64 或本地路径可避免服务端下载超时，提升稳定性。

如何将图像或视频压缩到满足要求的大小？

视觉理解模型对输入的文件有大小限制，可通过以下方法压缩。

图像压缩方法

-   在线工具：使用 [CompressJPEG](https://compressjpeg.com/zh/) 等在线工具进行压缩。
-   本地软件：使用 Photoshop 等软件，在导出时调整质量。
-   代码实现：

```
# pip install pillow

from PIL import Image
def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", optimize=True, quality=quality)

# 传入本地图像
compress_image("/xxx/before-large.jpeg","/xxx/after-min.jpeg")

# 批量压缩目录下的图像
import glob
import os

def batch_compress(input_dir, output_dir, quality=85):
    files = (
        glob.glob(os.path.join(input_dir, "*.jpg"))
        + glob.glob(os.path.join(input_dir, "*.jpeg"))
        + glob.glob(os.path.join(input_dir, "*.png"))
    )
    for i, f in enumerate(files, 1):
        try:
            compress_image(f, os.path.join(output_dir, os.path.basename(f)), quality)
            print(f"[{i}/{len(files)}] {os.path.basename(f)} done")
        except Exception as e:
            print(f"[{i}/{len(files)}] {os.path.basename(f)} error: {e}")

batch_compress("/xxx/input_dir", "/xxx/output_dir")
```

视频压缩方法

-   在线工具：使用 [FreeConvert](https://www.freeconvert.com/) 等在线工具进行压缩。
-   本地软件：使用 [HandBrake](https://handbrake.fr/) 等软件。
-   代码实现：使用FFmpeg工具，更多用法请参见[FFmpeg官网](https://ffmpeg.org/download.html)。

```
# 基础转换命令
# -i，作用：输入文件路径，常用值示例：input.mp4
# -vcodec，作用 视频编码器 ，一般取值有libx264（通用推荐）、libx265（压缩率更高）、
# -crf，作用：控制视频质量，取值范围：[18-28]，数值越小，质量越高，文件体积越大。
# --preset，作用：控制编码速度与压缩效率的平衡。一般取值有 slow、fast、faster
# -y，作用：覆盖已存在文件(无需赋值)
# output.mp4，作用：输出文件路径

ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow output.mp4
```

模型输出物体定位的结果后，如何将检测框绘制到原图上？

视觉理解模型输出物体定位效果后，可参照以下代码将检测框及其标签信息绘制到原图上。

-   Qwen2.5-VL：返回的坐标相对于缩放后的图像左上角的绝对值，单位为像素。可参见[qwen2\_5\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/xldjey/qwen2_5-vl-2d.py)代码绘制检测框。
-   Qwen3-VL、Qwen3.5、Qwen3.6、Qwen3.7、Qwen3.8系列（如 qwen3.5-plus、qwen3.6-plus、qwen3.7-plus 等）：返回的坐标为相对坐标，坐标值会归一化到`[0, 999]`。可参见[qwen3\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/eamyrc/qwen3-vl-2d.py)（二维定位）或[qwen3\_vl\_3d.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/uukdlq/qwen3_vl_3d.zip)（三维定位）中的代码绘制检测框。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
