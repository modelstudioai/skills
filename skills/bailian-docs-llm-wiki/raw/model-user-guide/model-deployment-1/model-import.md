# 模型导入

介绍百炼平台从阿里云 OSS 导入 LoRA 模型的全流程操作，涵盖首次 OSS 授权、模型文件准备、导入表单填写、导入模型管理与常见问题排查。

## 模型导入概述

本篇介绍将本地训练的 LoRA 模型从阿里云对象存储 OSS 导入到百炼平台的全流程，覆盖首次 OSS 授权、模型文件准备、导入表单填写、模型查看管理与删除，以及导入失败、已失效等常见问题排查。导入成功后即可部署服务，部署、扩缩容与下线操作详见[部署运维](#)，通过 API 完成部署与调用详见[使用 API 进行模型部署](#)，部署前置概念与计费方案对比详见[模型部署简介](#)，本篇与三者构成概念、导入、部署、调用的完整链路。

导入页基础模型字段由平台接口动态返回当前支持导入的基础模型清单，可能随版本更新，请以控制台可选列表为准。当前支持的基础模型如下：

**当前支持的基础模型清单（点击展开）**

以下清单由后端接口动态返回，可能随版本更新而调整，请以控制台实际可选项为准。

**模型系列**

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

训练方式可选项取决于所选基础模型的声明，选择基础模型后训练方式字段自动渲染可选项并默认选中第一项。当前版本仅支持导入 LoRA 模型，全参微调模型不可导入。

导入来源仅支持「从 OSS 导入」一项，表单中默认选中且无其他选项，暂不支持从其他渠道导入模型。

导入成功后的模型状态为创建成功，可在[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)列表中部署服务；从 OSS 导入的模型不支持增量训练，如需迭代请重新训练后再次导入。导入后将使用百炼提供的免费存储空间存放模型记录。

## 首次导入前完成 OSS 授权

首次从 OSS 导入模型前，须完成 OSS 服务关联角色授权，并为目标 Bucket 添加访问标签。授权通过导入页一键完成，授权后系统自动创建服务关联角色 AliyunServiceRoleForSFMDataHubOSSImport（服务名 datahub.sfm.aliyuncs.com，权限策略 AliyunServiceRolePolicyForSFMDataHubOSSImport），通常秒级生效。服务关联角色说明详见[OSS 服务关联角色](#)，主账号与子账号的概念与区别详见[主账号与子账号](#)。

在[导入模型页](https://bailian.console.aliyun.com/#/efm/model_center/import_model)的「导入来源」选择「从 OSS 导入」后，若未授权，OSS 字段区会提示「您还未授权OSS」并显示「前往授权」链接，确定按钮在未授权时不可用。主账号与子账号的授权路径不同，请按账号类型选择。

【截图：ss-oss-auth-01.png — 导入页 OSS 字段区「您还未授权OSS」提示与「前往授权」入口，及授权弹窗】

### 使用主账号

1.  在导入模型页「导入来源」选择「从 OSS 导入」后，页面提示「您还未授权OSS」，在提示栏右侧点击「前往授权」。
    
2.  在弹出的对话框中点击「立即授权」，系统自动创建服务关联角色 AliyunServiceRoleForSFMDataHubOSSImport，通常秒级生效，服务高峰期可能稍有延迟。
    
3.  为目标 OSS Bucket 添加标签：访问 OSS 管理控制台的 Bucket 列表，找到目标 Bucket，悬停标签列图标并点击「前往编辑」→「创建标签」，添加标签名 bailian-datahub-access、标签值 read，保存。
    
4.  返回导入模型页，重新选择目标 Bucket 再尝试导入。百炼不支持访问 Bucket 根目录下的文件，须选择 Bucket 下已有的子目录或新建子目录。
    

### 使用子账号

1.  在导入模型页「导入来源」选择「从 OSS 导入」后，页面提示「您还未授权OSS」，点击「前往授权」。
    
2.  在弹出的对话框中点击「立即授权」，界面提示「授权失败：当前用户没有创建服务关联角色的权限」。对话框显示 Service Name 为 datahub.sfm.aliyuncs.com，服务关联角色名称为 AliyunServiceRoleForSFMDataHubOSSImport，所需用户权限为 ram:CreateServiceLinkedRole。须先由主账号授予子账号创建服务关联角色的权限，再由子账号完成授权。
    
3.  由主账号授予子账号创建服务关联角色的权限：
    
    1.  主账号登录 RAM 控制台，在左侧导航栏选择「权限管理 → 权限策略」，点击「创建权限策略」。
        
    2.  选择「脚本编辑」，在 Effect、Action、Resource、Condition 中分别输入以下脚本内容，点击「确定」：
        
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
        
    3.  输入权限策略名称（示例：服务关联角色）后点击「确定」。
        
    4.  在左侧导航栏选择「身份管理 → 用户」，找到待授权的子账号，点击操作列**新增授权**。
        
    5.  选择刚才创建的自定义权限策略，点击「确认新增授权」，子账号即拥有创建服务关联角色的权限。
        
4.  返回导入模型页点击「前往授权」，在弹出的对话框中点击「立即授权」，系统自动创建服务关联角色，通常秒级生效。
    
5.  为目标 OSS Bucket 添加 bailian-datahub-access=read 标签（操作同主账号步骤 3），然后返回导入模型页重新选择目标 Bucket。百炼不支持访问 Bucket 根目录下的文件。
    

授权后须为目标 OSS Bucket 添加标签：标签名为 bailian-datahub-access，标签值为 read。该标签用于标记百炼可访问的 Bucket，未添加此标签的 Bucket 在下拉列表中不可选，须到[OSS 管理控制台](https://oss.console.aliyun.com/)添加标签后重新选择。

OSS Bucket 存储类型不支持归档、冷归档或深度冷归档，支持内容加密的 Bucket 与私有 Bucket。百炼不支持访问 Bucket 根目录下的文件，须选择 Bucket 下已有的子目录或新建子目录。

### 旧授权方式升级

若您此前使用的是旧授权方式，导入页 Bucket 字段下方会提示「建议转换为新的 Bucket 授权方式，提升安全性」并提供「直接转换」链接。点击后弹出确认框，确认即可升级为服务关联角色授权方式，升级不影响原有数据。

### 未开通 OSS 产品

若主账号尚未开通对象存储 OSS，导入页会提示「您还未开通OSS」并提供前往购买的链接。须由主账号前往 OSS 控制台开通 OSS 后返回导入页重新授权。

## 准备 LoRA 模型文件

导入前须将 LoRA 模型文件按以下要求存放在 OSS Bucket 的子目录中（不支持 Bucket 根目录），并在提交前通过系统的自动校验。模型文件须直接放在所选子目录下，系统会自动识别。

当前版本仅支持导入 LoRA 模型，不支持导入全参微调模型。

### 必需文件与目录结构

子目录中须包含以下文件：adapter\_model.safetensors（LoRA 适配器权重，SafeTensors 格式）、adapter\_config.json（含 rank、alpha 等参数的配置文件）、config.json（基础模型配置）。选中目录后系统会自动校验这些文件的格式与完整性。

### 训练参数约束

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

【截图：ss-safetensors-out-01.png — safetensors 结构检查脚本输出示例，展示冻结 VIT 的 adapter 文件仅含 lora\_A、lora\_B 参数键】

### 提交前自动校验

在[导入页](https://bailian.console.aliyun.com/#/efm/model_center/import_model)选中模型目录后，系统会自动调用文件校验接口检查目录下模型文件的格式与完整性。校验失败会在目录字段下方显示红标提示并阻断提交，须按提示修正文件后再提交。常见失败原因如缺少必需文件，对应错误码 AvailableModelFileNotFound。

【截图：ss-dir-browser-01.png — 模型目录浏览器选中子目录后的文件自动校验结果】

## 导入 LoRA 模型

完成 OSS 授权并准备好模型文件后，在[百炼控制台·我的模型](https://bailian.console.aliyun.com/#/efm/model_center)页面点击右上角「导入模型」按钮进入创建页，按以下步骤完成导入。

1.  在「我的模型」页面，点击右上角的「导入模型」按钮进入导入模型创建页。
    
2.  按下方表格填写模型信息，其中基础模型须与 LoRA 训练时的基座一致，Bucket 须已添加 bailian-datahub-access=read 标签，模型目录选中后系统会自动校验文件。
    
3.  确认信息无误后点击确定提交，系统自动验证文件格式和完整性，通过后开始导入；如需放弃点击取消返回列表页。导入后可在[管理导入的模型](#sec-manage)查看状态。
    

导入模型表单各字段含义如下：

【截图：ss-import-form-01.png — 导入模型创建页 7 字段表单全貌】

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

若尚未完成 OSS 授权，确定按钮不可用，须先完成[首次导入前完成 OSS 授权](#sec-authorize-oss)后再提交。导入成功后即可部署，部署操作详见[部署运维](#)。

导入后的模型状态包括创建中（正在导入）、创建成功（可部署）、创建失败（导入失败）和已失效（源文件已变更）。

## 管理导入的模型

导入提交后返回[我的模型](https://bailian.console.aliyun.com/#/efm/model_center)列表页，可查看与管理所有导入的模型。列表展示模型名称、模型 ID（附复制按钮）、基础模型、来源、支持部署方式、状态、创建时间与操作列，右上角提供导入模型入口与刷新按钮。

【截图：ss-my-model-list-01.png — 我的模型列表页，含名称、基础模型、来源、部署方式、状态、创建时间、操作列】

### 状态与流转

模型状态包括创建中、创建成功、创建失败和已失效。创建中表示正在导入；创建成功表示导入完成可部署；创建失败表示导入未成功；已失效表示创建成功后 OSS 源模型文件发生变更。列表对处于创建中状态的模型每 3 秒自动静默刷新，属正常行为，非接口异常。

创建失败状态旁附「详情」链接，悬停可查看失败错误码（如 AvailableModelFileNotFound）与对应的 oss://bucket/path 路径，用于定位失败文件。

已失效状态可悬停查看弹出框，展示「如下文件检测到更新」及发生变更的源文件名列表，提示须重新导入。

【截图：ss-status-popover-01.png — 已失效状态气泡弹出框文件变更列表与创建失败悬浮提示错误码】

### 操作列可用性

-   **部署**：仅创建成功状态可点击，点击后跳转部署创建页，部署操作详见[部署运维](#)；其余状态或无可选部署方式时按钮不可用。
    
-   **增量训练**：从 OSS 导入的模型不支持增量训练，按钮不可用。
    
-   **删除**：创建中状态不可删除；量化模型须前往模型压缩界面删除。
    

在操作列点击删除并确认后，仅删除百炼侧的模型记录，不影响 OSS 源文件。其余状态删除时会调用删除接口清理记录。

删除操作不可恢复：仅移除百炼侧的模型记录，须重新导入才能恢复；不会删除 OSS 中的源文件。

列表顶部搜索框可按模型名称筛选模型，支持清空重置。来源列按导入来源渲染：OSS 导入显示 oss://bucket/path，训练任务显示来源任务 ID（已删除则显示「训练任务已删除」），并标注全参、LoRA 或量化标签。通过 API 调用已部署模型详见[使用 API 进行模型部署](#)。

所有操作按单个模型进行，不支持批量删除或批量部署。

## 常见问题

汇总导入过程中常见的问题与处理方式。

**导入失败提示 AvailableModelFileNotFound 怎么办？**

该错误表示模型目录文件校验未通过（格式或完整性问题），不是单纯重传文件可解决。请检查所选目录是否包含齐全合规的 adapter\_model.safetensors、adapter\_config.json、config.json，并确认 rank、词汇表、chat\_template 等约束均满足，修正后重新选择目录提交。

**模型状态显示「已失效」是怎么回事？**

已失效表示该模型创建成功后，OSS 源模型文件发生了变更，属正常检测行为而非故障。将鼠标悬停在已失效状态上可查看发生变更的文件名列表，需重新导入模型方可恢复可用。

**遇到「10041495」报错怎么办？**

一般是由于主账号尚未开通对象存储服务 OSS。须由主账号前往 OSS 管理控制台按界面指引开通 OSS，再返回百炼导入模型界面重新尝试授权。

**子账号授权 OSS 失败怎么办？**

子账号授权失败是因为没有创建服务关联角色的权限，并非真失败。须先由主账号在 RAM 控制台创建自定义权限策略（操作为 ram:CreateServiceLinkedRole，针对服务 datahub.sfm.aliyuncs.com）并授予子账号，再由子账号重新点击授权。OSS 服务关联角色说明详见[OSS 服务关联角色](#)。

**Bucket 下拉列表中目标 Bucket 不可选怎么办？**

这是授权要求而非故障。新授权方式下，未添加 bailian-datahub-access=read 标签的 Bucket 在下拉中不可选。须到 OSS 管理控制台为目标 Bucket 添加该标签后返回导入页重新选择。

**我的模型列表每隔几秒自动刷新是故障吗？**

不是故障。列表检测到有处于创建中状态的模型时，会每 3 秒静默刷新以获取最新状态，无创建中状态时自动停止，属正常行为。

**为什么导入的模型与本地使用 vLLM、SGLang 推理的效果不一致？**

百炼推理引擎的参数默认值可能与本地推理框架不同，并非模型导入有误。为对齐 vLLM 默认值，建议调用时参考下表设置参数；使用 SGLang 等其他框架请参考对应文档调整。该参数对照属部署与调用范畴，详见[使用 API 进行模型部署](#)。

**参数名称**

**推荐值（对应 vLLM 默认值）**

temperature

取值范围 \[0, 2)，设置为 1.0 等同于 vLLM 引擎默认值。

top\_p

取值范围 (0, 1.0\]，设置为 1.0 等同于 vLLM 引擎默认值。

top\_k

取值为 None 或大于 100 时不启用 top\_k 策略，仅 top\_p 生效；设置为 99 不支持全采样，接近 vLLM 默认值 0（全采样）。

presence\_penalty

取值范围 \[-2.0, 2.0\]，设置为 0 等同于 vLLM 引擎默认值。

repetition\_penalty（DashScope 协议）

提高可降低生成重复度，1.0 表示不惩罚；取值范围大于 0，设置为 1.0 等同于 vLLM 引擎默认值。

**删除导入的模型会影响 OSS 中的源文件吗？**

不会。删除仅移除百炼侧的模型记录，需重新导入方可恢复；OSS 源文件归您所有，百炼仅通过 bailian-datahub-access=read 标签读取访问，删除模型不会改动 OSS 中的任何文件。
