# 通用图像编辑-万相2.1

万相-通用图像编辑模型支持输入文本指令，实现扩图、去水印、风格迁移、指令编辑、局部重绘、图像修复等多种图像编辑任务。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="模型概览"></a>

<a id="a157c08947jdi"></a>

## 模型概览

**效果示例**

|  |  |  |  |
| --- | --- | --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p942860.png)<br><br>原图 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p942862.png)<br><br>把她的头发修改为红色 | ![35779519-bfc3-4b0a-a594-d764fe9a46d83005601501](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p1005537.png)<br><br>给她戴上一副墨镜 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p1005538.png)<br><br>转换成法国绘本风格 |

> 更多示例请参见[关键能力](wanx-image-edit.md#3529413499zph)。

<a id="快速开始"></a>

<a id="61747164c4o6o"></a>

## 快速开始

<a id="前提条件"></a>

<a id="52fe871aee8n2"></a>

#### 前提条件

在调用前，请[获取与配置 API Key](../../../../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过DashScope SDK进行调用，还需要[安装SDK](../../../../model-api-reference/preparations/install-sdk.md)。

<a id="示例代码"></a>

<a id="75c877efa951c"></a>

#### 示例代码

本节演示如何调用通用图像编辑 API 完成一次“局部重绘”任务。

> SDK 在底层封装了异步处理逻辑，上层接口表现为同步调用（即单次请求并等待最终结果返回）；而 curl 示例则对应两个独立的异步 API 接口：一个用于提交任务，另一个用于查询结果。

<a id="sec-tabs"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

本示例支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="3cd4969b00193"></a>

### 请求示例

<a id="code-block"></a>

```python
import base64
import os
import mimetypes
import dashscope
from dashscope import DashScopeError

"""
环境要求：
    dashscope python SDK >= 2.0.1
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# mask_image_url = "file://" + "/path/to/your/mask_image.png"     # Linux/macOS
# base_image_url = "file://" + "C:/path/to/your/base_image.jpeg"  # Windows
# 示例（相对路径）：
# mask_image_url = "file://" + "./mask_image.png"                 # 以实际路径为准
# base_image_url = "file://" + "./base_image.jpeg"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# mask_image_url = encode_file("./mask_image.png")               # 以实际路径为准
# base_image_url = encode_file("./base_image.jpeg")              # 以实际路径为准

def sample_sync_call_imageedit():
    print('please wait...')
    try:
        # generate 为“提交+等待”一步式调用，返回已完成的任务对象 job
        job = client.images.generate(
            model="wanx2.1-imageedit",
            function="description_edit_with_mask",
            prompt="陶瓷兔子拿着陶瓷小花",
            # base_image_url/mask_image_url 为编辑专属入参，经 extra_input 透传到请求 input 段
            extra_input={
                "mask_image_url": mask_image_url,
                "base_image_url": base_image_url,
            },
            n=1,
        )
        print('response: %s' % job)
        for url in job.image_urls:
            print("---------------------------")
            print(url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_imageedit()
```

<a id="0c0533477emwb"></a>

### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-2"></a>

```json
{
    "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
    "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="java"></a>

<a id="java-h4"></a>

#### Java

本示例支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="36e8ee89107qx"></a>

### 请求示例

<a id="code-block-3"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >=2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */

public class ImageEditSync {
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
    static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String maskImageUrl = "file://" + "/your/path/to/mask_image.png";    // Linux/macOS
    // static String baseImageUrl = "file:///" + "C:/your/path/to/base_image.png";  // Windows

    //【方式三】Base64编码
    // static String maskImageUrl = encodeFile("/your/path/to/mask_image.png");
    // static String baseImageUrl = encodeFile("/your/path/to/base_image.png");

    public static void syncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

<a id="75c2320e48eer"></a>

### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-4"></a>

```json
{
    "request_id": "bf6c6361-f0fc-949c-9d60-xxxxxx",
    "output": {
        "task_id": "958db858-153b-4c81-b243-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

本示例覆盖了从创建任务、轮询状态到获取并保存结果的全过程。

> **说明**
>
> -   异步调用必须设置 Header 参数`X-DashScope-Async` 为`enable`。
> -   异步任务的 `task_id` 查询有效期为 24 小时，过期后任务状态将变为 `UNKNOWN`。
> -   新手建议使用 [Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)调用API。

<a id="a4ac549258mtq"></a>

#### 步骤1：发起创建任务请求

该请求会返回一个任务ID（`task_id`）。

**请求示例**

<a id="code-block-5"></a>

```text
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "description_edit_with_mask",
    "prompt": "陶瓷兔子拿着陶瓷小花。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg",
    "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

**响应示例**

<a id="code-block-6"></a>

```json
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

<a id="26c6e917d9j74"></a>

#### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，通过接口轮询任务状态，直到 `task_status` 变为 SUCCEEDED 或 FAILED。

**请求示例**

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

<a id="code-block-7"></a>

```bash
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

> 图像URL有效期为24小时，请及时下载图像。

<a id="code-block-8"></a>

```text
{
    "request_id": "eeef0935-02e9-9742-bb55-xxxxxx",
    "output": {
        "task_id": "a425c46f-dc0a-400f-879e-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-02-21 17:56:31.786",
        "scheduled_time": "2025-02-21 17:56:31.821",
        "end_time": "2025-02-21 17:56:42.530",
        "results": [
            {
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/aaa.png"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="关键能力"></a>

<a id="3529413499zph"></a>

## 关键能力

通用图像编辑API 通过 `function` 参数来指定不同的图像编辑功能。所有功能均遵循[快速开始](wanx-image-edit.md#61747164c4o6o)的调用方式。

下文以curl调用为例，仅列出各功能专属的 `input` 和 `parameters` JSON 片段，用于说明请求体中需配置的内容。

> 提示：curl完整请求应包含 model、input、parameters 等顶层字段，具体结构请参考[通用图像编辑API参考](../../../../model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md#42703589880ts)。

<a id="全局风格化"></a>

<a id="d058c678a9iqt"></a>

### 全局风格化

将整张图像迁移至指定的艺术风格。使用场景包括：绘本创作、社交媒体配图（生成符合特定视觉风格的背景或概念图）等。

-   **如何使用**：将参数`function`设置为`stylization_all`。
    
-   **支持的风格**：
    
    -   法国绘本风格
    -   金箔艺术风格
-   **搭配使用的参数**：`parameters.strength` (0.0-1.0, 默认 0.5) 控制修改幅度，值越小越接近原图。
    
-   **提示词技巧**：使用**“转换成xx风格”**的句式，如“转换成法国绘本风格”。
    

<a id="accordion-请求示例"></a>

请求示例

<a id="code-block-9"></a>

```json
{
  "input": {
    "function": "stylization_all",
    "prompt": "转换成法国绘本风格",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_all_3.png"
  },
  "parameters": {
    "strength": 0.5
  }
}
```

<table><thead><tr><th rowspan="2"><p><strong>输入图像</strong></p></th><th colspan="2"><p><strong>输出图像</strong></p></th></tr><tr><th><p><strong>提示词：转换成法国绘本风格</strong></p></th><th><p><strong>提示词：转换成金箔艺术风格</strong></p></th></tr></thead><tbody><tr><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930009.png" alt="image"><strong></strong></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930012.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930013.png" alt="image"></p></td></tr><tr><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930016.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930018.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930020.png" alt="image"></p></td></tr></tbody></table>

<a id="1d330776a4w4s"></a>

##### 通过strength控制图像修改幅度

通过`parameters.strength`参数来控制图像修改幅度。该参数为可选值，取值范围为\[0.0, 1.0\]，默认值为0.5。值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。

> **输入提示词：**转换成法国绘本风格。

<table><thead><tr><th rowspan="2"><p><strong>输入图像</strong></p></th><th colspan="3"><p><strong>输出图像</strong></p></th></tr><tr><th><p><strong>strength=0.0（最小值）</strong></p></th><th><p><strong>strength=0.5（默认值）</strong></p></th><th><p><strong>strength=1.0（最大值）</strong></p></th></tr></thead><tbody><tr><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p944730.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p944733.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p944732.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p944734.png" alt="image"></p></td></tr></tbody></table>

<a id="局部风格化"></a>

<a id="b65daaa5cb1c5"></a>

### 局部风格化

仅对图像的局部区域进行风格迁移。使用场景包括：个性化定制（如人物服装风格化）、广告设计（突出商品）。

-   **如何使用**：将参数`function`设置为`stylization_local`。
    
-   **支持的风格**：中英文对照如下：
    
    -   冰雕：ice
    -   云朵：cloud
    -   花灯：chinese festive lantern
    -   木板：wooden
    -   青花瓷：blue and white porcelain
    -   毛茸茸：fluffy
    -   毛线：weaving
    -   气球：balloon
-   **提示词技巧**：使用“**把xx变成xx风格”**的句式，如“把房子变成木板风格”。
    

<a id="accordion-请求示例-2"></a>

请求示例

<a id="code-block-10"></a>

```json
{
  "input": {
    "function": "stylization_local",
    "prompt": "把房子变成木板风格",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_local_1.png"
  }
}
```

<table><thead><tr><th><p><strong>输入图像</strong></p></th><th colspan="4"><p><strong>输出图像</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930030.png" alt="image"></p><p><strong></strong></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930031.png" alt="image"></p><p>冰雕</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930038.png" alt="image"></p><p>云朵</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930040.png" alt="image"></p><p>花灯</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930041.png" alt="image"></p><p>木板</p></td></tr><tr><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930044.png" alt="image"></p><p>青花瓷</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930045.png" alt="image"></p><p>毛茸茸</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930046.png" alt="image">毛线</p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930048.png" alt="image"></p><p>气球</p></td></tr></tbody></table>

<a id="指令编辑"></a>

<a id="0c932e6efebf7"></a>

### 指令编辑

无需指定区域，仅通过文本指令即可增加或修改图像内容。使用场景包括：为人物添加配饰、更换发色等无需精确定位的简单编辑。

-   **如何使用**：将参数`function`设置为`description_edit`。
-   **搭配使用的参数**：`parameters.strength` (0.0-1.0, 默认 0.5) 控制修改幅度，值越小越接近原图。
-   **提示词技巧**：显式写明**“添加”**、**“修改”**这类操作描述。删除操作推荐使用[局部重绘](wanx-image-edit.md#b0d2188736q4f)。

<a id="accordion-请求示例-3"></a>

请求示例

<a id="code-block-11"></a>

```json
{
  "input": {
    "function": "description_edit",
    "prompt": "给小猫添加一副墨镜",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_1.jpeg"
  },
  "parameters": {
    "strength": 0.5
  }
}
```

| 能力 | 输入图像 | 输出图像 |
| --- | --- | --- |
| **添加元素** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p942858.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p942859.png)<br><br>给小猫添加一副墨镜。 |
| **修改元素** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p942860.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6028878571/p942862.png)<br><br>把她的头发修改为红色。 |

<a id="c9eadaec31lz1"></a>

##### 通过strength控制图像修改幅度

通过`parameters.strength`参数来控制图像修改幅度。该参数为可选值，取值范围为\[0.0, 1.0\]，默认值为0.5。值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。

> **输入提示词：**将她穿的衣服修改为彩色印花的沙滩衬衣。

<table><thead><tr><th rowspan="2"><p><strong>输入图像</strong></p></th><th colspan="3"><p><strong>输出图像</strong></p></th></tr><tr><th><p><strong>strength=0.0（最小值）</strong></p></th><th><p><strong>strength=0.5（默认值）</strong></p></th><th><p><strong>strength=1.0（最大值）</strong></p></th></tr></thead><tbody><tr><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p942929.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p942931.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p942932.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p942934.png" alt="image"></p></td></tr></tbody></table>

<a id="局部重绘"></a>

<a id="b0d2188736q4f"></a>

### 局部重绘

通过提供涂抹区域（mask）图像，对指定区域进行增加、修改或删除操作。使用场景包括：换装、替换物体、移除干扰物等需要精确控制范围的编辑。

-   **如何使用**：将参数`function`设置为`description_edit_with_mask`。
    
-   **涂抹区域要求**：需要提供 `mask_image_url`，涂抹图像中白色区域为待编辑区域，黑色为保留区域。
    
-   **提示词技巧**：显式写明**“添加”**、**“修改”以及描述删除后的内容**这类操作描述。
    
    -   **增加/修改**：可描述动作（“给小狗添加一顶帽子”）或描述最终结果（“一只戴着帽子的小狗”）。
    -   **删除**：若删除对象较小，`prompt` 可留空 (`""`)；若删除对象较大，`prompt` 需描述删除后应出现的背景内容（如“一个透明玻璃花瓶放在桌子上”），而非“删除小熊”。

<a id="accordion-请求示例-4"></a>

请求示例

<a id="code-block-12"></a>

```json
{
  "input": {
    "function": "description_edit_with_mask",
    "prompt": "一只陶瓷兔子抱着一朵陶瓷花",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_1.jpeg",
    "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_1_mask.png"
  }
}
```

<table><thead><tr><th><strong>能力</strong></th><th><strong>输入图像</strong></th><th><strong>输入涂抹区域图像</strong><strong>（白色为待编辑区域）</strong></th><th><strong>输出图像</strong></th></tr></thead><tbody><tr><td><strong>增加元素</strong></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929600.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929603.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929604.png" alt="image"><p>给小狗添加一顶帽子。</p><blockquote><p>提示词也可以写为“一只戴着帽子的小狗”（描述期望的图像内容）。</p></blockquote></td></tr><tr><td><strong>修改元素</strong></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930480.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930481.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930482.png" alt="image"><p>一只陶瓷兔子抱着一朵陶瓷花。</p><blockquote><p>提示词也可以写为“将陶瓷兔子抱着的胡萝卜换做陶瓷花”（描述动作）。</p></blockquote></td></tr><tr><td><strong>删除元素</strong></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930483.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930484.png" alt="image"></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930485.png" alt="image"><p>一个透明玻璃花瓶放在桌子上。</p><blockquote><p>提示词需要描述删除后的内容，不要写为“删除一只棕色的小熊”。</p></blockquote></td></tr></tbody></table>

<a id="去文字水印"></a>

<a id="97cea0ec36xff"></a>

### 去文字水印

> **说明**
>
> **法律风险提示**
>
> 使用本功能处理受版权保护的图像（如去除他人品牌水印）可能构成侵权行为。请确保您拥有所处理图像的合法使用权，并自行承担所有相关法律责任。

去除图像中的中英文字符或常见水印。使用场景包括：素材二次处理、广告图净化等。

-   **如何使用**：将参数`function`设置为`remove_watermark`。
-   **提示词技巧**：可使用通用指令如**“去除图像中的文字”**，或指定类型如“去除英文文字”。

<a id="accordion-请求示例-5"></a>

请求示例

<a id="code-block-13"></a>

```json
{
  "input": {
    "function": "remove_watermark",
    "prompt": "去除图像中的文字",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/remove_watermark_1.png"
  }
}
```

| 输入图像 | 输出图像（去除图像中的文字） |
| --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2315368571/p1005529.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2315368571/p1005526.png) |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2315368571/p1005528.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2315368571/p1005527.png) |

<a id="扩图"></a>

<a id="42a62bb11bx9n"></a>

### 扩图

沿图像的上、下、左、右四个方向按比例扩展画布，并智能填充内容。使用场景包括：调整构图、将竖图扩展为横图以适配不同媒介尺寸。

-   **如何使用**：将参数`function`设置为`expand`。
-   **搭配使用的参数**：`parameters`中的`top_scale`, `bottom_scale`, `left_scale`, `right_scale` 分别控制四个方向的扩展比例（如全部设置为 1.5，表示扩展为原尺寸的 1.5倍）。
-   **提示词技巧**：描述扩展后期望看到的完整场景内容。

<a id="accordion-请求示例-6"></a>

请求示例

<a id="code-block-14"></a>

```json
{
  "input": {
    "function": "expand",
    "prompt": "一家人在公园草坪上",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/expand_1.jpeg"
  },
  "parameters": {
    "top_scale": 1.5,
    "bottom_scale": 1.5,
    "left_scale": 1.5,
    "right_scale": 1.5
  }
}
```

| 输入图像 | 输出图像 |
| --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930529.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930531.png) |

<a id="图像超分"></a>

<a id="04e73f5e9d728"></a>

### 图像超分

提升图像清晰度并支持放大，将低分辨率或模糊图像变得清晰。使用场景包括：老照片修复、提升素材分辨率以满足高清打印或展示需求。

-   **如何使用**：将参数`function`设置为`super_resolution`。
-   **搭配使用的参数**：`parameters.upscale_factor` (1-4, 默认 1) 控制放大倍数。当值为 1 时，仅提升清晰度而不放大。
-   **提示词技巧**：可使用**“图像超分”**或描述图像内容。

<a id="accordion-请求示例-7"></a>

请求示例

<a id="code-block-15"></a>

```json
{
  "input": {
    "function": "super_resolution",
    "prompt": "图像超分",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/super_resolution_1.jpeg"
  },
  "parameters": {
    "upscale_factor": 2
  }
}
```

| 输入图像（模糊图像） | 输出图像（清晰图像） |
| --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930079.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2971781571/p930082.png) |

<a id="图像上色"></a>

<a id="dad8aa53ee8ng"></a>

### 图像上色

将黑白或灰度图像转换为彩色图像（黑白/灰度 → 彩色）。使用场景包括：历史照片上色、为线稿或灰度图填充颜色。

-   **如何使用**：将参数`function`设置为`colorization`。
-   **提示词技巧**：可留空由模型自动上色，或通过提示词指定关键元素的颜色（如“蓝色背景，黄色叶子”）。

<a id="accordion-请求示例-8"></a>

请求示例

<a id="code-block-16"></a>

```json
{
  "input": {
    "function": "colorization",
    "prompt": "蓝色背景，黄色的叶子",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/colorization_1.jpeg"
  }
}
```

| 输入图像 | 输出图像 |
| --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929637.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929638.png) |

<a id="线稿生图-支持涂鸦作画"></a>

<a id="aec91c51deqld"></a>

### 线稿生图（支持涂鸦作画）

基于输入图像的轮廓（线稿）并结合提示词生成新图像。使用场景包括：建筑概念设计、插画设计、涂鸦作画等。

-   **如何使用**：将参数`function`设置为`doodle`。
    
-   **搭配使用参数**：`parameters.is_sketch`，用来控制模型的生成效果。
    
    -   `false` （默认）：输入为 RGB 图像，模型会先提取线稿再生成图像（RGB图像 → 线稿 → 新图）。
    -   `true`：输入为 RGB 图像（如涂鸦或线稿），模型将直接基于此图像生成图像（RGB图像 → 新图）。
-   **提示词技巧**：描述期望生成的图像内容，描述越具体，生成效果越好。
    

<a id="accordion-请求示例1-线稿生图"></a>

请求示例1：线稿生图

<a id="code-block-17"></a>

```json
{
  "input": {
    "function": "doodle",
    "prompt": "北欧极简风格的客厅。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_1.png"
  },
  "parameters": {
    "is_sketch": false
  }
}
```

<a id="accordion-请求示例2-涂鸦作画"></a>

请求示例2：涂鸦作画

<a id="code-block-18"></a>

```json
{
  "input": {
    "function": "doodle",
    "prompt": "一颗树，二次元动漫风格",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_2.png"
  },
  "parameters": {
    "is_sketch": true
  }
}
```

| 能力 | 输入图像 | 输出图像 |
| --- | --- | --- |
| **线稿生图**<br><br>（is\_sketch=false） | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930074.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p930077.png)<br><br>北欧极简风格的客厅。 |
| **涂鸦作画**<br><br>（is\_sketch=true） | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p943021.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p943022.png)<br><br>一颗树，二次元动漫风格。 |

<a id="参考卡通形象生图"></a>

<a id="fade6eec1ctqa"></a>

### 参考卡通形象生图

> **说明**
>
> **法律风险提示**
>
> 使用本功能处理受版权保护的卡通形象可能构成侵权行为。请确保您拥有所参考形象的合法使用权，或使用您原创的形象，并自行承担所有相关法律责任。

-   **如何使用**：将参数`function`设置为`control_cartoon_feature`。
-   **提示词技巧**：**采用“卡通形象...”**的句式，详细描述形象的动作和所处环境。

<a id="accordion-请求示例2-涂鸦作画-2"></a>

请求示例2：涂鸦作画

<a id="code-block-19"></a>

```json
{
  "input": {
    "function": "control_cartoon_feature",
    "prompt": "卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/control_cartoon_feature_1.png"
  }
}
```

| 输入图像 | 输出图像 |
| --- | --- |
| ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929648.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3971781571/p929649.png) |

<a id="应用于生产环境"></a>

<a id="7c8e9262dcbem"></a>

## 应用于生产环境

<a id="最佳实践"></a>

<a id="dc072ae1abafj"></a>

#### 最佳实践

-   **异步轮询**：采轮询查询异步任务结果时，建议采用合理的轮询策略（如前30秒每3秒一次，之后拉长间隔），避免因过于频繁的请求而触发限流。
-   **参数调优**：对于 `strength` 等影响效果的关键参数，建议在正式上线前进行小范围测试，找到最适合业务场景的数值。
-   **图像存储**：API 返回的图像 URL 有效期24小时。请及时将生成的图像下载并转存到您自己的持久化存储服务中（如阿里云 OSS）。

<a id="风险防范"></a>

<a id="4a51361a6724r"></a>

#### 风险防范

-   **错误处理**：对任务查询结果中的 `task_status` 进行判断。对于 `FAILED` 状态，应记录 `code` 和 `message` 以便排查。部分错误（如系统超时）可能是瞬时的，可设计重试逻辑。
-   **内容安全**：API 会对输入和输出内容进行安全审核。若内容不合规，请求将会报错 `DataInspectionFailed` 错误。

<a id="api-参考"></a>

<a id="8202e9793agxx"></a>

## API 参考

关于万相-通用图像编辑模型的输入与输出参数，请参见[通用图像编辑API参考](../../../../model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md#42703589880ts)。

<a id="计费与限流"></a>

<a id="a585cbf27dck8"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型列表与价格](../../../get-started-with-models/models.md)。
    
-   模型限流请参见[万相](../../../get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   按成功生成的 **图像张数** 计费。仅当接口返回`task_status`为`SUCCEEDED` 并成功生成图像后，才会计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../../test-1/new-free-quota.md)。
    -   通用图像编辑还支持[节省计划](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)，抵扣顺序为 免费额度 > 节省计划 > 按量付费。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../../model-api-reference/preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="8ec3f7c0e0bns"></a>

## 常见问题

**Q: 为什么我的任务会失败（FAILED）？**

A: 任务失败的常见原因包括：

1.  内容审核不通过：输入或生成的图像内容触发了安全策略。
2.  参数错误：请求中的参数不合法，如 `function` 名称错误、URL 无法访问等。
3.  模型内部错误：模型在处理过程中遇到预期外的问题。请检查任务查询响应中的`code`和`error` 字段，获取具体错误码和信息，以便定位问题。
