# 微调图像生成模型

当使用万相进行**图像生成**时，若通过[Prompt 优化](https://help.aliyun.com/zh/model-studio/text-to-video-prompt)仍无法满足对**特定风格、IP形象或画面效果**的定制需求，请使用**模型微调**。

## **适用范围**

-   **适用部署模式及地域**：本文描述的功能仅在华北2（北京）地域可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   **开通账号权限**：若使用[阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    
-   **支持微调的方式**：SFT-LoRA高效微调。
    
-   **支持微调的模型**：
    
    -   图像生成（文生图/图生图）：wan2.7-image-pro、wan2.7-image。
        

## **如何微调模型**

## 文生图

**微调目标：训练一个人物LoRA模型**。

预期效果：输入一段提示词，模型自动生成特定人物在符合提示词场景下的描述。

**输入提示词**

人物在拥挤的早高峰地铁车厢内，抓着扶手，背景是模糊的乘客和车窗外的隧道灯光，身穿普通的上班族白衬衫和黑色西裤，人物站立面向镜头，半身照，写实抓拍感。

**输出图像（微调前-文生图）**

![7217b6ac-789d-43c3-aaa5-22647532de52\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433450871/p1075807.png)

> 无参考图无法生成特定人物形象。

**输出图像（微调后）**

![1\_24](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433450871/p1075796.png)

> 微调后的模型能稳定复现训练集中的特定人物形象。

## 图生图

**微调目标：训练一个"末日废土红黑机甲"LoRA模型**。

预期效果：输入一张人物图像，无需提示词，模型自动生成人物“**末日废土红黑机甲**”风格的图像。

**输入图像**

![29\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433450871/p1075797.jpg)

**输出图像（微调前）**

![output\_0\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433450871/p1075799.png)

> 无法通过提示词每次生成固定风格的“末日废土红黑机甲”特效。

**输出图像（微调后）**

![29\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433450871/p1075798.jpg)

> 微调后的模型无需提示词即能复现训练集中的特定“末日废土红黑机甲”特效。

**微调目标：训练一个"IP角色风格化"LoRA模型**。

预期效果：输入一段文本描述或一张参考图像，模型自动生成符合特定IP角色风格的图像。

运行下述代码前，请[开通百炼服务](https://help.aliyun.com/zh/model-studio/get-api-key)，并[配置API Key](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

### **步骤1：上传数据集**

将本地的数据集（.zip 格式）上传到阿里云百炼平台，并获取文件 ID (`**file_id**`)。

训练集样例数据：格式请参见[训练集](#d2dc0825ca6fv)。

-   图像生成-文生图：[wan-image-t2i-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260601/iszvtr/wan-image-t2i-training.zip)
    
-   图像生成-图生图：[wan-image-i2i-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260610/yynsck/wan-image-i2i-training.zip)
    

**请求示例**

> 本示例使用文生图，仅上传训练集，系统将自动从训练集中划分一部分作为验证集。

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'files=@"./wan-image-t2i-training-dataset.zip"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a fine-tune training data file for wan"'
```

**响应示例**

请保存 `file_id`，这是上传数据集的唯一标识。

```
{
    "data": {
        "uploaded_files": [
            {
                "name": "wan-image-t2i-training-dataset.zip",
                "file_id": "3bff1ef7-f72d-4285-bb75-xxxxxx"
            }
        ],
        "failed_uploads": []
    },
    "request_id": "1f3f1c5b-7418-4976-aaea-xxxxxx"
}
```

### **步骤2：微调模型**

##### **步骤2.1 创建微调任务**

使用步骤1中的文件ID启动训练任务。

**请求示例**

请将`<替换为训练数据集的文件id>`完整替换为上一步获取的`file_id`。完整参数说明与格式约束请参见[超参数](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#5f391e4b3cezf)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-image-pro",
    "training_file_ids": ["<替换为训练数据集的文件id>"],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "learning_rate": 3e-5,
        "max_steps": 800,
        "eval_steps": 200,
        "max_token_length": "1k",
        "gradient_clip": 0.5,
        "weight_decay": 0.02,
        "max_pixels": "1k",
        "val_img_size": "1k",
        "generation_type": "t2i",
        "lora_rank": 32,
        "save_total_limit": 10
    }
}'
```

**说明**

**训练耗时**（仅供参考）：

-   文生图（t2i）：2K，300 步，约 77 分钟。
    
-   图生图（i2i）：2K，300 步，约 110 分钟。
    

**响应示例**

关注 `output` 中的三个关键参数：

-   `job_id`：任务ID，用于查询进度。
    
-   `finetuned_output`：微调后的新模型名称，后续部署和调用时必须使用此名称。
    
-   `status`：模型训练状态。创建微调任务后，初始状态为PENDING，表示训练待开始。
    

```
{
    ...
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "PENDING",
        "finetuned_output": "xxxx-ft-202511111122-xxxx",
        ...
    }
}
```

##### **步骤2.2 查询微调任务状态**

通过步骤2.1获得的 `job_id` 查询任务进度，轮询以下接口直到 `status` 变为 **SUCCEEDED**。

**请求示例**

请将 URL 中的 `<替换为微调任务job_id>` 完整替换为`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

关注`output` 字段的两个参数：

-   `status`：当它的值变为 **SUCCEEDED** 时，表示模型已训练完毕，可以进行模型部署。
    
-   `usage`：模型训练消耗的总Token数量，用于模型训练计费。
    

```
{
    ...
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "SUCCEEDED",
        "usage": 432000,
        ...
    }
}
```

### **步骤3：部署微调后的模型**

##### **步骤3.1 部署模型为在线服务**

当微调任务的状态为 **SUCCEEDED** 后，将模型部署为在线服务。

**请求示例**

请将`<替换为模型名称model_name>` 完整替换为[创建微调任务](#bc825b6ec11y2)的输出参数`finetuned_output`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "capacity": 1,
    "plan": "lora"
}'
```

**响应示例**

关注 `output` 中的两个参数：

-   `deployed_model`：部署的模型名称，用于查询部署状态和调用模型。
    
-   `status`：模型部署状态。部署微调模型后，初始状态为PENDING，表示部署未开始。
    

```
{
    ...
    "output": {
        "deployed_model": "wan2.7-image-pro-xxxxxxxxxxxx",
        "status": "PENDING",
        ...
    }
}
```

##### **步骤3.2 查询部署状态**

查询部署状态，轮询以下接口直到 `status` 变为 **RUNNING**。

**说明**

本文示例的微调模型，部署过程预计需要 **5～10分钟**。

**请求示例**

请将`<替换为deployed_model>`完整替换为步骤3.1输出参数`deployed_model`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为deployed_model>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

关注`output`字段的两个参数：

-   `status`：当状态变为 **RUNNING** 时，表示模型已部署成功，可以开始调用。
    
-   `deployed_model`：部署的模型名称。
    

```
{
    ...
    "output": {
        "status": "RUNNING",
        "deployed_model": "wan2.7-image-pro-xxxxxxxxxxxx",
        ...
    }
}
```

### **步骤4：**调用模型生成图像

模型部署成功后（即部署状态`status`为 **RUNNING** ），即可发起调用。

**步骤4.1：创建图像生成任务，并获取task\_id**

**请求示例**

请将`<替换为部署名称deployed_model>`完整替换为上一步输出的`deployed_model`值。

## 文生图

输入一段包含触发词的文本描述，模型自动生成符合训练风格的图像。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "<替换为部署名称deployed_model>",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "s86b5p, 人物在拥挤的早高峰地铁车厢内，抓着扶手，背景是模糊的乘客和车窗外的隧道灯光，身穿普通的上班族白衬衫和黑色西裤，人物站立面向镜头，半身照，写实抓拍感。"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1
    }
}'
```

## 图生图

输入一张参考图像和编辑指令，模型基于参考图像生成符合训练风格的图像。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "<替换为部署名称deployed_model>",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "<替换为参考图像URL>"},
                    {"text": "s86b5p, Change the background to an elevator with red lighting. Change the character clothing to red tight-fitting mech armor with black stripe decorations."}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1
    }
}'
```

**响应示例**

请复制并保存`task_id`，用于下一步结果查询。

```
{
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx",
    "output": {
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx",
        "task_status": "PENDING"
    }
}
```

**输入参数说明**

**说明**

调用微调后的 LoRA 模型时，输入参数用法与[万相-图像生成与编辑2.7 API](https://help.aliyun.com/zh/model-studio/wan-image-generation-and-editing-api-reference)保持一致。

下表仅列出 LoRA 模型调用时的**关键参数说明**。

**字段**

**类型**

**必选**

**描述**

**示例值**

model

string

是

模型名称。必须使用已成功部署且部署状态为RUNNING的微调模型。

wan2.7-image-pro-xxxxxxxxxxxx

input.messages\[\].content\[\].text

string

是

文本提示词。建议包含触发词以激活 LoRA 风格。

s86b5p, 人物在午后静谧的私人图书馆...

parameters.size

string

否

输出图片分辨率。

-   **方式一：指定输出图片的分辨率（推荐）**
    
    -   支持 1K、2K（默认）、4K 三种规格
        
    -   **适用范围**：
        
        -   文生图：支持1K、2K、4K。
            
        -   图像编辑：支持1K、2K。
            
    -   **各规格总像素**：1K：1024\*1024、2K：2048\*2048、4K：4096\*4096
        
-   **方式二：指定生成图像的宽高像素值**
    
    -   文生图：总像素在 \[768\*768, 4096\*4096\] 之间，宽高比范围为 \[1:8, 8:1\]。
        
    -   图像编辑：总像素在 \[768\*768, 2048\*2048\] 之间，宽高比范围为 \[1:8, 8:1\]。
        

2K

parameters.n

integer

否

生成图像数量，取值范围 1~4，默认为 1。

1

**步骤4.2：根据task\_id查询结果**

使用`task_id`轮询任务状态，直到 `task_status` 变为 SUCCEEDED，从`output.choices[].message.content[].image`获取图像URL。

**请求示例**

> 请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

> 图像URL有效期为24小时，请及时下载图像。

```
{
    "request_id": "3f2ebb4e-3d47-97b5-xxxx-xxxxxx",
    "output": {
        "task_id": "aeea547c-e24e-4acb-xxxx-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-05-29 17:35:23.826",
        "scheduled_time": "2026-05-29 17:35:23.865",
        "end_time": "2026-05-29 17:36:32.498",
        "finished": true,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/xxx.png?Expires=xxxxxx"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "size": "2048*2048",
        "total_tokens": 770,
        "image_count": 1,
        "output_tokens": 691,
        "input_tokens": 79
    }
}
```

## **构建自定义数据集**

除了使用本文示例数据体验微调流程外，您也可以构建自己的数据集进行微调。

数据集应包含 **训练集**（必须）和 **验证集**（可选，支持从训练集自动划分）。所有文件请打包为`**.zip**` 格式，文件名建议仅使用英文、数字、下划线或短横线。

### **数据集格式**

#### **训练集：必须提供**

## 文生图

训练集包括**训练目标图像和标注文件（data.jsonl）**。

-   训练集样例：wan-image-t2i-training.zip。
    
-   zip包目录结构：
    
    ```
    wan-image-t2i-training-dataset.zip
    ├── data.jsonl      # 必须固定命名为data.jsonl，最大支持 20MB
    ├── 1_0.png         # 训练目标图像，最大分辨率4096*4096，单张≤20MB，支持PNG/JPG/JPEG/WEBP/BMP
    ├── 1_1.png         # 文件名仅支持英文字符，平铺结构（禁止子目录）
    └── 1_2.png
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为 JSON 对象。
    
    ```
    {
      "prompt": "s86b5p, 人物在午后静谧的私人图书馆，身后是高耸的深色胡桃木书架，阳光透过百叶窗洒下条纹状的光影，身穿柔软的米色绞花针织毛衣，人物站立面向镜头，半身照，画面具有细腻的胶片颗粒感。",
      "img_path": "./1_0.png"
    }
    ```
    

## 图生图

训练集包括**参考图像（输入）、训练目标图像（输出）和标注文件（data.jsonl）**。

-   训练集样例：wan-image-i2i-training.zip。
    
-   zip包目录结构：
    
    ```
    wan-image-i2i-training-dataset.zip
    ├── data.jsonl      # 必须固定命名为data.jsonl，最大支持 20MB
    ├── 1_0.jpg         # 训练目标图像（输出）
    ├── 1_1.jpg         # 参考图像（输入）
    ├── 6_0.jpg         # 训练目标图像（输出）
    └── 6_1.jpg         # 参考图像（输入）
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为 JSON 对象。
    
    ```
    {
      "prompt": "s86b5p, Change the background to an elevator with red lighting, featuring large floor-to-ceiling windows. Change the character's clothing to red tight-fitting mech armor with black stripe decorations.",
      "input_img": "./1_1.jpg",
      "img_path": "./1_0.jpg"
    }
    ```
    

**说明**

-   data.jsonl 必须为 Line-delimited JSONL 格式（每行一个独立 JSON 对象），**禁止**使用 JSON 数组格式（即文件首字符不能是 `[`）。
    
-   zip 包内文件必须平铺放置，**禁止**使用子目录。文件名仅支持英文字符（禁止中文、空格、特殊字符）。
    

#### **验证集：可选**

验证集包括**标注文件（data.jsonl）和可选的参考图像（图生图模式需要）**，无需提供目标图像。训练任务会在每个评估节点，自动调用模型服务，使用验证集的 Prompt（和参考图像）生成预览图像。

-   验证集**：**
    
    -   **文生图：**[wan-image-t2i-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260601/ulrlhp/wan-image-t2i-valid-dataset.zip)
        
    -   **图生图：**[wan-image-i2i-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260610/jrggzt/wan-image-i2i-valid-dataset.zip)
        
-   zip包目录结构：
    
    ```
    wan-image-i2i-valid-dataset.zip
    ├── data.jsonl       # 必须固定命名为data.jsonl，最大支持 20MB
    ├── input_001.png    # 可选，图生图模式的参考图像
    └── input_002.png
    ```
    
-   标注文件（data.jsonl）：每一行代表一条验证数据，必须为 JSON 对象。
    
    ## 文生图
    
    ```
    {
        "prompt": "s86b5p, 人物在拥挤的早高峰地铁车厢内，抓着扶手，背景是模糊的乘客和车窗外的隧道灯光，身穿普通的上班族白衬衫和黑色西裤，人物站立面向镜头，半身照，写实抓拍感。"
    }
    ```
    
    ## 图生图
    
    ```
    {
        "prompt": "s86b5p, Change the background to an elevator with red lighting, featuring large floor-to-ceiling windows. Change the character's clothing to red tight-fitting mech armor with black stripe decorations.",
        "input_img": "./input_001.png"
    }
    ```
    

### **数据规模与限制**

-   **数据量**：建议至少提供 **25张** 图像（推荐 50 张以上效果更佳）。要求同一角色/风格，多场景多角度，内容描述一致。
    
-   **Zip压缩包**：通过 API 上传时，总包大小 ≤ 1GB。
    
-   **训练图像要求**：
    
    -   图像格式支持BMP、JPEG、PNG、WEBP。
        
    -   图像分辨率 ≤ 4096×4096。
        
    -   单个图像文件大小 ≤ 20MB。
        

### **数据收集和清洗**

###### **1\. 确定微调场景**

万相支持**图像生成**的微调场景包括：

-   **IP角色风格化**：让模型学会特定IP角色的绘画风格，如二次元人物、吉祥物形象等。
    
-   **固定画面风格**：提升模型对特定艺术风格的复现度，如扁平插画、水墨画、像素风等。
    
-   **特定场景生成**：复刻特定的构图模式或场景模板，如商品展示图、海报版式等。
    

###### **2\. 获取原始素材**

-   AI 生成筛选：利用"万相"基础模型批量生成图像，再人工挑选出最符合目标效果的优质样本。这是最常用的方法。
    
-   真实拍摄：如果您的目标是追求高真实感的场景（如产品实拍、人物摄影等），使用实拍素材是最佳选择。
    
-   三维软件渲染：对于需要控制细节的场景或3D渲染风格，建议使用 3D 软件（如 Blender、C4D）制作素材。
    

###### **3\. 清洗数据**

**维度**

**正面要求**

**负面案例**

**一致性**

**核心特征必须高度统一**。

例如：训练"扁平插画风格"，所有图像必须都是相同的线条粗细和配色方案。

**风格混杂**。

数据集中既有厚涂风格，又有扁平风格。模型不知道该学哪种风格。

**多样性**

**主体与场景越丰富越好**。

覆盖不同主体（男女老少、猫狗建筑）和不同构图（远景、近景、特写）。同时，分辨率和长宽比应尽可能多样化。

**单一场景或主体**。

所有图像都是"穿红衣的人在白墙前"。模型会误以为"红衣"和"白墙"是风格的一部分，换了场景就不会生成了。

**均衡性**

**各类型数据比例均衡**。

如果包含多种风格，数量应大致相等。

**比例严重失调**。

90%是人像图像，10%是风景图像。模型可能在生成风景图像时效果不佳。

**纯净度**

**画面干净清晰**。

使用无干扰的原始素材。

**有干扰元素**。

图像中带有水印、明显的黑边或噪点。模型可能会把水印当成风格学进去_。_

**分辨率**

**分辨率适中**。

建议训练图像分辨率不超过 2048×2048，过大的图像会增加训练时间。

**分辨率差异过大**。

训练集中既有 256×256 的小图，又有 4096×4096 的大图，会影响训练稳定性。

### **图像标注：为图像编写Prompt**

在数据集的标注文件（data.jsonl）中，每张图像都有对应的一段 Prompt。Prompt 是用来描述**目标图像**的画面内容，Prompt 的质量直接决定模型"学什么"。

#### **Prompt编写公式**

**Prompt = \[主体描述\] + \[背景描述\] + \[触发词\] + \[风格描述\]**

**Prompt描述项**

**说明**

**填写建议**

**示例**

**主体描述**

描述画面中原本存在的人或物

必填

一位年轻女性身着红色中式长衫...

**背景描述**

描述画面中主体所处的环境

必填

背景是被绿色的藤蔓覆盖的砖墙...

**触发词**

一个无实际意义的稀有词汇

推荐填写

s86b5p 或 m01aa

**风格描述**

详细描述目标图像的艺术风格和画面特征

推荐填写

采用扁平化插画风格，以简洁流畅的线条、鲜明平涂色彩突出主体立体感与现代设计感。

##### **关于"触发词"**

-   **触发词是什么？**
    
    它相当于一个 **"视觉锚点"** 。因为很多复杂的视觉风格（如某种独特的画面质感、特定的色彩搭配）很难用文字精确描述，所以用这个词强制告诉模型：当你看到 s86b5p 时，就必须生成这种特定的视觉风格。
    
-   **为什么要使用它？**
    
    模型微调是建立"文本"与"图像特征"的映射关系。触发词就是那个把"难以言传的风格"绑定到一个独一无二的词上，让模型能够锁定目标。
    
-   **既然有了触发词，为什么还要详细描述风格？**
    
    两者分工不同，配合使用效果更好。
    
    -   风格描述：负责解释 "画面应该是什么样的"。它告诉模型基础的艺术风格和视觉特征，通常多个样本的风格描述是一致的。
        
    -   触发词：负责解释 "风格具体是什么样"。它代表了那些文字无法精确描述的独特视觉特征。
        

## **使用验证集评估模型**

### **指定验证集**

微调任务必须包含训练集，验证集则是可选项。您可以选择由系统**自动划分**或**手动上传**验证集，具体指定方式如下：

##### **方式一：未上传验证集（系统自动划分）**

在[创建微调任务](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#e702c9786b40q)时，如果没有单独上传验证集（即未传入`validation_file_ids`参数），系统将根据`split`从训练集划分验证集，默认 0.9。即 90% 用于训练，10% 用作验证。

##### **方式二：主动上传验证集（通过 validation\_file\_ids 指定）**

如果您希望使用一套自己准备的数据来评估Checkpoint，而不是依赖系统随机划分，可以上传自定义验证集。

注意：一旦选择主动上传，系统将**完全忽略**上述自动划分规则，仅使用您上传的数据进行验证。

**操作步骤：主动上传验证集**

1.  **准备验证集**：将验证数据打包成一个独立的 `.zip` 文件，请参见[验证集格式](#4a214aadd60df)。
    
2.  **上传验证集**：调用[上传数据集](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#Kv4zB)接口，上传这个验证集 `.zip` 文件，获得一个专属的文件ID。
    
3.  **创建任务时指定验证集**：在调用[创建微调任务](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#e702c9786b40q)接口时，将这个文件ID填入 `validation_file_ids` 参数中。
    
    ```
    {
        "model":"wan2.7-image-pro",
        "training_file_ids":[ "<训练集的文件id>" ],
        "validation_file_ids": [ "<自定义验证集的文件id>" ],
        ...
    }
    ```
    

### **挑选最佳Checkpoint进行部署**

在训练过程中，系统会定期保存模型的"快照"（即 Checkpoint）。默认情况下，系统会输出**最后一个Checkpoint**作为最终的微调模型。但中间过程产出的Checkpoint效果可能优于最终版本，您可以从中挑选出最满意的一个进行部署。

系统将按照[超参数](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#5f391e4b3cezf)`eval_steps`设定的间隔，在**验证集**上运行Checkpoint并生成预览图像。

-   **如何评估**：通过直接观察生成的预览图像来判断效果。
    
-   **挑选标准**：找到效果最好、且风格最贴合的那个 Checkpoint 。
    

#### **操作步骤**

##### **步骤1：查看Checkpoint生成的预览效果**

##### **步骤1.1 查询已通过验证的Checkpoint列表**

该接口仅返回通过验证集验证、**且成功生成预览图像的 Checkpoint**，验证失败的不会列出。

**请求示例**

-   `<替换为微调任务job_id>`：完整替换为[创建微调任务接口](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#e69160039ceah)的输出参数`job_id`。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-results' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

此接口返回一个仅包含成功通过验证的Checkpoint名称的列表。

```
{
    "request_id": "da1310f5-5a21-4e29-99d4-xxxxxx",
    "output": [
        {
            "checkpoint": "checkpoint-160"
        },
        ...
    ]
}
```

##### **步骤1.2 查询Checkpoint对应的验证集结果**

从上一步返回的 Checkpoint 列表中选择一个（例如"checkpoint-160"），查看其生成的图像效果。

**请求示例**

-   `<替换为微调任务job_id>`： 完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如"checkpoint-160"。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-details/<替换为选择的checkpoint>?page_no=1&page_size=10' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

预览图像URL为`img_path`，有效期为24小时，请及时下载图像并查看效果。重复此步骤，比较多个Checkpoint的效果，找出最满意的一个。

```
{
    "request_id": "375b3ad0-d3fa-451f-b629-xxxxxxx",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 5,
        "list": [
            {
                "img_path": "https://finetune-result.oss-cn-wulanchabu.aliyuncs.com/xxx.png?Expires=xxxxxx",
                "prompt": "s86b5p, Change the background to an elevator equipped with a white ceiling lighting, featuring large floor-to-ceiling windows. Change the character's clothing to red tight-fitting mech armor with black stripe decorations.",
                "input_img": "https://finetune-result.oss-cn-wulanchabu.aliyuncs.com/val_dataset/input_001.png?Expires=xxxxxx"
            },
            ...
        ]
    }
}
```

##### **步骤2：导出Checkpoint，并获取待部署的模型名称**

##### **步骤2.1 导出模型**

假设"checkpoint-160"的效果最佳，接下来是将其导出。

**请求示例**

-   `<替换为微调任务job_id>`： 完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如"checkpoint-160"。
    
-   `<替换为控制台展示的导出模型名称>`：完整替换为自定义的模型名称，仅用于控制台展示，例如"wan2.5-checkpoint-160"。该名称必须全局唯一，不支持重复名称多次导出，参数填写请参见[导出Checkpoint](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#2636e0fdfewpw)。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/export/<替换为待导出的checkpoint>?model_name=<替换为控制台展示的导出模型名称>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

响应参数`output=true`，表示导出请求已成功创建。

```
{
    "request_id": "0817d1ed-b6b6-4383-9650-xxxxx",
    "output": true
}
```

##### **步骤2.2 查询部署后的新模型名称**

查询所有Checkpoint的状态，确认导出已完成，并获取它专属的、用于部署的新模型名称（`**model_name**`）。

**请求示例**

-   `<替换为微调任务job_id>` ：完整替换为[创建微调任务](#bc825b6ec11y2)输出参数`job_id`的值。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/checkpoints' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

在返回列表中定位导出的 Checkpoint（如 checkpoint-160）。当其 `status` 变为 **SUCCEEDED** 时，表示导出成功；此时返回的 `**model_name**` 字段即为导出后的新模型名称。

```
{
    "request_id": "b0e33c6e-404b-4524-87ac-xxxxxx",
    "output": [
         ...,
        {
            "create_time": "2025-11-11T13:27:29",
            "full_name": "ft-202511111122-496e:checkpoint-160",
            "job_id": "ft-202511111122-496e",
            "checkpoint": "checkpoint-160",                             
            "model_name": "xxxx-ft-202511111122-xxxx-c160", // 重要字段，将用于模型部署和调用
            "model_display_name": "xxxx-ft-202511111122-xxxx", 
            "status": "SUCCEEDED" // 成功导出的checkpoint
        },
        ...
        
    ]
}
```

##### **步骤3：部署并调用模型**

在成功导出 Checkpoint 并获取 `**model_name**` 后，请按照以下步骤执行后续操作：

-   [模型部署](#0ad4c110b58ui)：在输入参数 `model_name`，填入导出后获取到的具体值。
    
-   [模型调用](#543cc07530gl2)：参照接口说明，调用已部署模型。
    

## **计费说明**

-   **模型训练：收费。**详情请参见[模型训练计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。
    
    -   费用 = 训练 Tokens 总量 × 单价。
        
    -   训练结束后，在[查询微调任务状态](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference#a242dac535nqt)接口 `usage` 字段查看训练消耗的总 Token 数。
        
    
    下表列出了文生图（t2i）训练中常见训练步数（Step）及预估费用。该数据仅供参考，实际训练效果请以最终交付为准，费用请以正式账单为准。详细计费公式请参见[模型训练计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。
    
    **图片分辨率**
    
    **常见Step步数**
    
    **Token消耗预估**
    
    **费用预估（元）**
    
    1K
    
    500
    
    64,000,000
    
    5,120
    
    1000
    
    128,000,000
    
    10,240
    
    2000
    
    256,000,000
    
    20,480
    
    2K
    
    500
    
    116,100,000
    
    9,288
    
    1000
    
    232,200,000
    
    18,576
    
    2000
    
    464,400,000
    
    37,152
    
-   **模型部署与调用**：部署免费，调用按微调的基础模型的标准调用价格计费。
    
    **模型名称**
    
    **Lora部署调用价格**
    
    wan2.7-image-pro
    
    0.50元/张
    
    wan2.7-image
    
    0.20元/张
    

## **API文档**

[视频/图像生成模型微调 API 参考](https://help.aliyun.com/zh/model-studio/wan-generation-finetune-api-reference)

## **常见问题**

#### **Q：如何设计一个好的触发词？**

A: 规则如下：

-   推荐使用无实际语义的稀有字符组合，如 s86b5p、m01aa、EVEAven638123。确保在基模词表中无语义含义。
    
-   **避免**使用常用英语单词（如 beautiful, fire, dance），否则会污染模型原本对这些词的理解。
