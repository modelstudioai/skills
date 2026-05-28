# 模型导入

**[我的模型](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_center)**页面用于管理您创建和导入的模型。通过该页面，您可以将本地训练的 LoRA 模型从阿里云对象存储 OSS 导入到百炼平台。

## 使用前提

导入前，请确保满足以下条件：

-   **OSS Bucket 准备**：已创建 OSS Bucket，并为目标 Bucket 添加标签。详见[首次从 OSS 导入模型文件](#ed9633f0476gu)。
    
    **说明**
    
    -   支持的 OSS Bucket 存储类型不包括归档、冷归档或深度冷归档。支持内容加密的 Bucket。支持私有的Bucket。
        
    -   不支持访问OSS Bucket根目录下的文件，请您在OSS Bucket下选择已有的子目录或新建一个子目录供阿里云百炼访问。
        
    -   支持导入任意大小的模型文件，导入后将使用阿里云百炼提供的免费存储空间。
        
    
-   **模型文件准备**：模型文件需符合[导入要求与限制](#h2-file-format-constraints)。模型文件夹需直接放在 OSS Bucket 中，系统会自动识别。
    

## 支持导入的基础模型

当前支持导入以下基础模型的 LoRA 微调版本：

模型系列

模型名称

千问3

千问3-32B

千问3-14B

千问3-8B

千问3-4B-Instruct-2507

千问3-VL

千问3-VL-8B-Instruct

千问2.5

千问2.5-72B-Instruct

千问2.5-32B-Instruct

千问2.5-14B-Instruct

千问2.5-7B-Instruct

千问2.5-VL

千问2.5-VL-72B-Instruct

千问2.5-VL-7B-Instruct

## 操作步骤

按照以下步骤将 LoRA 模型从 OSS 导入到百炼平台：

1.  在**我的模型**页面，点击**导入模型**按钮。
    
2.  在导入模型页面中，填写以下信息：
    
    -   **模型名称**：输入模型的显示名称，最多50个字符。
        
    -   **基础模型**：选择该 LoRA 模型对应的基础模型。
        
    -   **导入来源**：当前仅支持"从OSS导入"，系统已默认选中。
        
    -   **Bucket**：选择存储模型文件的 OSS Bucket。
        
3.  确认信息无误后，点击**确定**提交导入请求。系统将自动验证模型文件格式和完整性，验证通过后开始导入。导入完成后，您可以在**[我的模型](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_center)**页面查看导入的模型，并进行部署、增量训练等操作。
    

## 导入要求与限制

**重要**

重要：当前版本仅支持导入 LoRA（Low-Rank Adaptation）模型，不支持导入全参微调模型。

导入 LoRA 模型前，请确保满足以下要求：

-   **必需文件**：OSS Bucket 中需包含以下文件：
    
    -   **adapter\_model.safetensors**：LoRA 适配器的权重文件，采用 SafeTensors 格式存储。
        
    -   **adapter\_config.json**：LoRA 适配器的配置文件，包含 rank、alpha 等关键参数信息。
        
-   **rank 参数限制**：rank 值必须为 8、16、32 或 64 中的一个，且同一模型的所有 LoRA 层必须使用相同的 rank 值。
    
-   **修改词汇表的模型**：如果训练过程中添加了新 token 或修改了原始词汇表（vocab），该模型无法导入。系统要求使用与基础模型完全一致的词汇表。
    
-   **修改对话模板的模型**：如果训练过程中修改了 chat\_template 配置，该模型无法导入。系统仅支持使用与对应开源基础模型默认配置一致的 chat\_template。
    
    chat\_template 配置通常位于以下位置：
    
    -   模型的 config.json 文件中的 `chat_template` 字段。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1185949671/p1049475.png)
        
    -   tokenizer\_config.json 文件中的 `chat_template` 字段。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1185949671/p1049476.png)
        
-   **未冻结 VIT 的视觉语言模型**：对于 VL（Vision-Language）模型，必须冻结 Vision Transformer（VIT）部分。如果 LoRA adapter 中包含 visual 相关的权重参数（即未冻结 VIT），该模型无法导入。
    
    可以运行以下代码判断。
    
    ```
    from safetensors import safe_open
    import argparse
    
    def print_safetensor_structure(file_path):
        print(f"Loading safetensor file: {file_path}")
        print("="*80)
        
        with safe_open(file_path, framework="pt") as f:
            keys = f.keys()
            print(f"Found {len(keys)} tensors in the file:\n")
            
            for key in sorted(keys):
                tensor = f.get_tensor(key)
                shape = tuple(tensor.shape)
                dtype = str(tensor.dtype)
                device = tensor.device if hasattr(tensor, 'device') else 'cpu'
                
                lora_tag = " [LoRA]" if "lora_A" in key or "lora_B" in key else ""
                
                print(f"[{dtype:>14}] {shape} | {key} {lora_tag}")
    
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Print structure of a .safetensors LoRA adapter.")
        parser.add_argument("filepath", type=str, help="Path to the .safetensors file")
        args = parser.parse_args()
    
        print_safetensor_structure(args.filepath)
    ```
    
    判断方法：检查 adapt\_model.safetensors 文件中是否包含 `visual` 相关的权重参数。如果文件中存在以 `visual` 开头的参数键（例如 `visual.encoder.layer.0...`），说明 VIT 部分未被冻结，该模型无法导入。
    
    ![冻结VIT的adapter文件示例](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1185949671/p1049184.png)
    
    ![未冻结VIT的adapter文件示例（包含visual参数）](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1185949671/p1049183.png)
    

## 常见问题

#### **为什么导入的模型与本地使用 vLLM、SGLang 推理的效果不一致？**

百炼平台的推理引擎参数设置可能与您本地使用的推理框架默认值不同。为确保效果一致，建议在调用 API 时调整以下参数：

参数名称

推荐值（对应 vLLM 默认值）

temperature

取值范围：\[0, 2)。设置为 1.0 等同于 vLLM 引擎默认值。

top\_p

取值范围：(0, 1.0\]。设置为 1.0 等同于 vLLM 引擎默认值。

top\_k

取值为 None 或大于 100 时，表示不启用 top\_k 策略，此时仅有 top\_p 策略生效。设置为 99 不支持全采样，该值接近 vLLM 默认值 0（全采样）。

presence\_penalty

取值范围：\[-2.0, 2.0\]。设置为 0 等同于 vLLM 引擎默认值。

repetition\_penalty（DashScope 协议）

提高 repetition\_penalty 可以降低模型生成的重复度，1.0 表示不做惩罚。取值范围：大于 0。设置为 1.0 等同于 vLLM 引擎默认值。

说明：以上参数值基于 vLLM 引擎的默认配置。如果您的本地环境使用 SGLang 或其他推理框架，请参考对应框架的文档调整参数。

**首次从 OSS 向阿里云百炼导入文件，应该如何操作？**

如果您是首次从 OSS 向阿里云百炼导入文件，请先按照界面提示完成授权，并为目标 OSS Bucket 添加`bailian-datahub-access`标签，然后再进行导入。

> 如果您尚不清楚主账号和子账号的概念和区别，请先阅读[权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview)。

### 使用主账号

1.  单击**前往授权**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7865858471/p961834.png)
    
2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#32a41eac73z64)（必要条件）。
    
    > 通常秒级生效，服务高峰期可能会稍有延迟。
    
    > [遇到“本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](https://help.aliyun.com/zh/model-studio/my-model-center#a25cf9b36eh5o)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p937216.png)
    
3.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的****Bucket 列表****，即可查看您已创建的Bucket。
        
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p937209.png)
        
    3.  单击**创建标签**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903515.png)
        
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903517.png)
        
4.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

### 使用**子账号**

1.  单击**前往授权**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7865858471/p961834.png)
    
2.  在弹出的对话框中，单击**确认授权**。界面会提示**授权失败**、**当前用户没有创建服务关联角色的权限**（因为当前子账号没有创建服务关联角色的权限。接下来需要先授予子账号创建服务关联角色的权限，再授予子账号通过阿里云百炼访问OSS的权限）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p913212.png)
    
3.  授予子账号创建服务关联角色的权限。
    
    1.  **需主账号登录**[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后单击界面上的**创建权限策略**。
        
    2.  在**脚本编辑**的`Effect`、`Action`、`Resource`、`Condition`中分别输入以下脚本中的对应内容后，单击**确定**。
        
        ```
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "datahub.sfm.aliyuncs.com"
                }
            }
        }
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903452.png)
        
    3.  输入权限策略名称后，单击**确定**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903416.png)
        
    4.  在左侧导航栏，选择**身份管理** > **用户**。在页面列表中找到待授权的子账号，然后单击子账号**操作**列的**添加权限**。
        
    5.  在权限策略中选择刚才创建的权限策略（自定义策略），单击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4482537371/p907087.png)
        
4.  授权子账号通过阿里云百炼访问OSS。
    
    1.  返回**导入模型**界面，单击**前往授权**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p937184.png)
        
    2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#32a41eac73z64)（必要条件）。
        
        > 通常秒级生效，服务高峰期可能会稍有延迟。
        
        > [遇到“本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](https://help.aliyun.com/zh/model-studio/my-model-center#a25cf9b36eh5o)
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p937216.png)
        
5.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的****Bucket 列表****，即可查看您已创建的Bucket。
        
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105663471/p937209.png)
        
    3.  单击**创建标签**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903515.png)
        
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903517.png)
        
6.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

**遇到“10041495”报错怎么办？**

一般是由于主账号尚未开通对象存储服务 OSS，处理步骤：

1.  需主账号前往[OSS管理控制台](https://oss.console.aliyun.com/)，按界面指引开通 OSS。
    
2.  返回阿里云百炼**导入模型**界面，再尝试授权。
