# 我的模型

在我的模型中，可以统一管理您在阿里云百炼调优后的模型以及从 OSS 导入的模型（限 LoRA 微调和全参微调），涵盖首次 OSS 授权、模型文件准备与校验、导入表单填写、模型状态管理与常见问题排查，支持云端部署，提供高并发、低延迟的推理服务。

## 支持的模型

在[我的模型](https://bailian.console.aliyun.com/model/custom)页面，您可以管理以下两类模型：

-   **调优模型：**指在阿里云百炼调优后的模型，详见[模型调优支持的模型](https://help.aliyun.com/zh/model-studio/model-training-overview#adf01c4f4dqxd)。
    
-   **导入模型：**指从阿里云对象存储OSS导入的模型。支持导入部分经过 LoRA 微调或全参微调的模型。
    
    > 导入全参微调后的模型属于白名单功能，如需开通请联系客户经理。
    
    模型列表：
    
    #### 华北2（北京）
    
    **支持的模型**
    
    **模型名称**
    
    千问3
    
    千问3-32B
    
    千问3
    
    千问3-14B
    
    千问3
    
    千问3-8B
    
    千问3
    
    千问3-4B-Instruct-2507
    
    千问3-VL
    
    千问3-VL-8B-Instruct
    
    千问2.5
    
    千问2.5-72B-Instruct
    
    千问2.5
    
    千问2.5-32B-Instruct
    
    千问2.5
    
    千问2.5-14B-Instruct
    
    千问2.5
    
    千问2.5-7B-Instruct
    
    千问2.5-VL
    
    千问2.5-VL-72B-Instruct
    
    千问2.5-VL
    
    千问2.5-VL-7B-Instruct
    
    #### 新加坡
    
    **支持的模型**
    
    **模型名称**
    
    \-
    
    \-
    
    > 数据更新可能存在延迟，请以导入模型时界面实际显示为准。
    

## 导入模型

接下来为您介绍如何通过阿里云百炼控制台从OSS导入模型。

> 导入模型不支持通过API或命令行操作。

1.  在[我的模型](https://bailian.console.aliyun.com/model/custom)页面，单击**导入模型**，进入导入模型界面。
    
2.  输入**模型名称**，并选择导入模型的**基础模型**（即被微调的模型）。
    
3.  **导入方式**选择**从OSS导入**，暂不支持其它方式。您需要自行将已完成LoRA微调或全参微调的模型的相关文件[上传](https://help.aliyun.com/zh/oss/user-guide/upload-objects-to-oss/)至阿里云对象存储OSS。[查看模型文件示例](#8200512f30r63)
    
    **重要**
    
    -   首次导入请先按照界面提示完成授权，并为目标Bucket添加标签。详见下方[常见问题](#9412d1ca87761)中的「首次从 OSS 向阿里云百炼导入文件，应该如何操作？」。
    -   支持的OSS Bucket存储类型不包括归档、冷归档或深度冷归档。支持内容加密的Bucket。支持私有的Bucket。
    -   不支持访问OSS Bucket根目录下的文件，请您在OSS Bucket下选择已有的子目录或新建一个子目录供阿里云百炼访问。
    -   支持导入任意大小的模型文件，导入后将使用阿里云百炼提供的免费存储空间。
    
4.  单击**确定**后，系统将开始导入模型。在请求高峰时段，该过程可能需要较长时间，请耐心等待。
    

### 准备 LoRA 模型文件

导入前须将 LoRA 模型文件按以下要求存放在 OSS Bucket 的子目录中（不支持 Bucket 根目录），并在提交前通过系统的自动校验。模型文件须直接放在所选子目录下，系统会自动识别。

#### 必需文件与目录结构

子目录中须包含以下文件：adapter\_model.safetensors（LoRA 适配器权重，SafeTensors 格式）、adapter\_config.json（含 rank、alpha 等参数的配置文件）、config.json（基础模型配置）。选中目录后系统会自动校验这些文件的格式与完整性。

#### 训练参数约束

-   **rank 取值**：rank 必须为 8、16、32 或 64 之一，且同一模型的所有 LoRA 层须使用相同的 rank 值，否则无法导入。
-   **词汇表不可修改**：训练中添加新 token 或修改原始词汇表的模型无法导入，须与基础模型词汇表完全一致。
-   **对话模板不可修改**：训练中修改 chat\_template 的模型无法导入，须与基础模型默认配置一致。chat\_template 位于 config.json 或 tokenizer\_config.json 的 chat\_template 字段。
-   **视觉模型须冻结 VIT**：视觉语言模型必须冻结 Vision Transformer 部分。若 LoRA 适配器中包含 visual 相关权重参数（即未冻结 VIT），该模型无法导入。

可在导入前运行以下脚本检查 adapter\_model.safetensors 是否含 visual 开头的参数键，以判断 VIT 是否冻结。

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

判断方法：若脚本输出中存在以 visual 开头的参数键（如 visual.encoder.layer.0...），说明 VIT 部分未被冻结，该模型无法导入；若仅含 lora\_A、lora\_B 等 LoRA 相关参数键，则 VIT 已冻结，可正常导入。

#### 提交前自动校验

在导入页选中模型目录后，系统会自动调用文件校验接口检查目录下模型文件的格式与完整性。校验失败会在目录字段下方显示红标提示并阻断提交，须按提示修正文件后再提交。常见失败原因如缺少必需文件，对应错误码 AvailableModelFileNotFound。

### 导入表单字段

导入模型表单各字段含义如下：

**字段**

**说明**

**约束**

模型名称

输入模型的显示名称。

必填，最多 50 字符

基础模型

选择 LoRA 训练时的基座模型，须与训练基座一致。

必填，下拉选择

训练方式

可选项取决于所选基础模型，选择基础模型后自动渲染并默认选中第一项。

必填，下拉选择

导入来源

当前仅支持「从 OSS 导入」，无其他选项。

只读，默认选中

Bucket

选择存放模型文件的 OSS Bucket，仅列出已添加 bailian-datahub-access=read 标签的 Bucket。

必填，下拉选择

模型目录

在选定 Bucket 中浏览并选择模型 Checkpoint 所在子目录，不支持选 Bucket 根目录。

必填，树形选择

模型加密

平台自动为导出的模型文件开启 OSS 服务端加密（SSE-OSS），使用 OSS 完全托管密钥，加密算法为 AES256。

只读，平台强制

导入后的模型状态包括创建中（正在导入）、创建成功（可部署）、创建失败（导入失败）和已失效（源文件已变更）。

## 后续操作

### 管理我的模型

在[我的模型](https://bailian.console.aliyun.com/model/custom)页面可查看当前业务空间内所有已调优和导入的模型，并执行部署、删除等操作。

> **删除：**已部署的模型须先下线再删除；若模型来自[模型调优](https://bailian.console.aliyun.com/model/tuning)，本操作不会删除模型调优界面中的记录。

#### 状态与流转

导入的模型状态包括创建中、创建成功、创建失败和已失效。创建中表示正在导入；创建成功表示导入完成可部署；创建失败表示导入未成功；已失效表示创建成功后 OSS 源模型文件发生变更。列表对处于创建中状态的模型每 3 秒自动静默刷新，属正常行为，非接口异常。

创建失败状态旁附「详情」链接，悬停可查看失败错误码（如 AvailableModelFileNotFound）与对应的 oss://bucket/path 路径，用于定位失败文件。

已失效状态可悬停查看弹出框，展示「如下文件检测到更新」及发生变更的源文件名列表，提示须重新导入。

#### 操作列可用性

每行操作列固定提供**部署**、**增量训练**和**删除**三个按钮，按钮可用性取决于模型状态：

-   **部署**：仅创建成功状态可点击，点击后跳转部署创建页，部署操作详见[部署运维](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)；其余状态或无可选部署方式时按钮不可用。
-   **增量训练**：从 OSS 导入的模型不支持增量训练，按钮不可用。
-   **删除**：创建中状态不可删除；量化模型须前往模型压缩界面删除。

在操作列点击删除并确认后，仅删除百炼侧的模型记录，不影响 OSS 源文件。列表顶部搜索框可按模型名称筛选模型，支持清空重置。**来源**列按导入来源渲染：OSS 导入显示 oss://bucket/path，训练任务显示来源任务 ID（已删除则显示「训练任务已删除」）。**支持部署方式**列展示模型支持的部署方式和训练方式标签（如全参、LoRA 或量化标签），以及计费方式（如按 Token 计费、按模型单元计费），无可选部署方式时显示「-」。

所有操作按单个模型进行，不支持批量删除或批量部署。

### 调用我的模型

模型需成功部署后才能提供推理服务（只能通过API调用）。关于具体操作和计费方式，请参见[部署后调用](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

-   **关键限制：**在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)后的模型部署成功后，只能使用其所在业务空间的 API-KEY 调用，且目前仅支持通过[DashScope](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)方式调用，不支持通过OpenAI兼容方式调用。
-   **优化推理效果：**请在调用时显式配置推理超参（如`presence_penalty`、`frequency_penalty`和`repetition_penalty`等），并确保与您线下微调后的推理超参设置保持一致。

## 模型文件示例

-   LoRA微调后一般会生成两个checkpoint文件，分别是best\_model\_checkpoint（在验证集上表现最优的检查点）与last\_model\_checkpoint（最后一次保存的检查点）。您可以根据需求选择其中一个导入。
    
    请确保导入的模型文件中包含adapter\_model.safetensors和adapter\_config.json。如需了解LoRA微调方法，您可以参考[阿里云大模型ACP课程](https://edu.aliyun.com/course/3130200/)中的模型微调章节。
    
    checkpoint 文件目录中通常包含以下文件：`global_step100/`（子目录）、`README.md`、`adapter_config.json`、`adapter_model.safetensors`、`additional_config.json`、`configuration.json`、`generation_config.json`、`latest`、`rng_state_0.pth` 和 `rng_state_1.pth`。
    
-   全参微调需要导入的文件和开源模型保持一致。
    

## 常见问题

首次从 OSS 向阿里云百炼导入文件，应该如何操作？

如果您是首次从 OSS 向阿里云百炼导入文件，请先按照界面提示完成授权，并为目标 OSS Bucket 添加`bailian-datahub-access`标签，然后再进行导入。

> 如果您尚不清楚主账号和子账号的概念和区别，请先阅读[权限管理](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

#### 使用主账号

1.  单击**前往授权**。
    
    在 **导入方式** 中选择 **从OSS导入** 后，页面会显示"您还未授权OSS"的提示信息，在提示栏右侧找到 **前往授权** 链接。
    
2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)（必要条件）。
    
    > 通常秒级生效，服务高峰期可能会稍有延迟。
    
    > [遇到”本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](#9412d1ca87761)
    
3.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的**Bucket 列表**，即可查看您已创建的Bucket。
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
    3.  单击**创建标签**。
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
4.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

#### 使用 子账号

1.  单击**前往授权**。
    
2.  在弹出的对话框中，单击**确认授权**。界面会提示**授权失败**、**当前用户没有创建服务关联角色的权限**（因为当前子账号没有创建服务关联角色的权限。接下来需要先授予子账号创建服务关联角色的权限，再授予子账号通过阿里云百炼访问OSS的权限）。
    
    对话框中显示 Service Name 为 `datahub.sfm.aliyuncs.com`，服务关联角色名称为 `AliyunServiceRoleForSFMDataHubOSSImport`，执行该操作所需的用户权限为 `ram:CreateServiceLinkedRole`。
    
3.  授予子账号创建服务关联角色的权限。
    
    1.  **需主账号登录**[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理权限策略**，然后单击界面上的**创建权限策略**。
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

3.  输入权限策略名称后，单击**确定**。
    
    本示例中，权限策略名称为`服务关联角色`。
    
4.  在左侧导航栏，选择**身份管理用户**。在页面列表中找到待授权的子账号，然后单击子账号**操作**列的**添加权限**。
    
5.  在权限策略中选择刚才创建的权限策略（自定义策略），单击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
    
6.  授权子账号通过阿里云百炼访问OSS。
    
    1.  返回**导入模型**界面，单击**前往授权**。
        
        **导入方式**选择**OSS**后，界面提示**您还未授权OSS**。
        
    2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)（必要条件）。
        
        > 通常秒级生效，服务高峰期可能会稍有延迟。
        
        > [遇到”本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](#9412d1ca87761)
        
7.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的**Bucket 列表**，即可查看您已创建的Bucket。
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
    3.  单击**创建标签**。
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
8.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

遇到“10041495”报错怎么办？

一般是由于主账号尚未开通对象存储服务 OSS，处理步骤：

1.  需主账号前往[OSS管理控制台](https://oss.console.aliyun.com/)，按界面指引开通 OSS。
2.  返回阿里云百炼**导入模型**界面，再尝试授权。

导入失败提示 AvailableModelFileNotFound 怎么办？

该错误表示模型目录文件校验未通过（格式或完整性问题），不是单纯重传文件可解决。请检查所选目录是否包含齐全合规的 adapter\_model.safetensors、adapter\_config.json、config.json，并确认 rank、词汇表、chat\_template 等约束均满足，修正后重新选择目录提交。

模型状态显示「已失效」是怎么回事？

已失效表示该模型创建成功后，OSS 源模型文件发生了变更，属正常检测行为而非故障。将鼠标悬停在已失效状态上可查看发生变更的文件名列表，需重新导入模型方可恢复可用。

Bucket 下拉列表中目标 Bucket 不可选怎么办？

这是授权要求而非故障。新授权方式下，未添加 bailian-datahub-access=read 标签的 Bucket 在下拉中不可选。须到 OSS 管理控制台为目标 Bucket 添加该标签后返回导入页重新选择。

我的模型列表每隔几秒自动刷新是故障吗？

不是故障。列表检测到有处于创建中状态的模型时，会每 3 秒静默刷新以获取最新状态，无创建中状态时自动停止，属正常行为。

为什么导入的模型与本地使用 vLLM、SGLang 推理的效果不一致？

推理参数对齐详见[API部署指南](raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

删除导入的模型会影响 OSS 中的源文件吗？

不会。删除仅移除百炼侧的模型记录，需重新导入方可恢复；OSS 源文件归您所有，百炼仅通过 bailian-datahub-access=read 标签读取访问，删除模型不会改动 OSS 中的任何文件。

旧授权方式如何升级？

若您此前使用的是旧授权方式，导入页 Bucket 字段下方会提示「建议转换为新的 Bucket 授权方式，提升安全性」并提供「直接转换」链接。点击后弹出确认框，确认即可升级为服务关联角色授权方式，升级不影响原有数据。
