# Skill

Skill 是可添加到智能体应用的能力包，用于让智能体在对话中自动处理特定类型的任务。通过 Skill，智能体无需额外编码即可获得文件处理、数据分析等专业能力。

## 什么是 Skill

添加 Skill 后，智能体可以在对话中自动识别匹配的任务并调用对应 Skill 进行处理，无需额外编写代码或接入外部工具。

百炼提供两类 Skill：

-   **官方 Skill**：平台预置的通用 Skill，覆盖常见文件处理场景。无需配置，添加后即可使用。
    
-   **自定义 Skill**：通过上传 ZIP 技能包创建。适用于官方 Skill 未覆盖的业务场景，如特定行业的数据处理、自定义文件格式解析等。
    

## 官方 Skill

百炼提供多个官方 Skill，覆盖常见的文件处理场景。官方 Skill 由平台统一维护，无需配置，添加后即可使用。

官方 Skill 持续更新中，可在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看最新列表。

## 创建自定义 Skill

当官方 Skill 无法满足业务需求时，可通过上传 ZIP 技能包创建自定义 Skill。ZIP 技能包需满足以下要求：

**要求**

**说明**

必须包含 SKILL.md

ZIP 包根目录下必须有 `SKILL.md` 文件，用于定义 Skill 元信息。

大小限制

整个 ZIP 包不超过 10 MB。

名称唯一

SKILL.md 中的 `name` 字段不可与当前账号下已有 Skill 重名。

### SKILL.md 编写规范

`SKILL.md` 使用 YAML 格式定义 Skill 的名称和描述。格式如下：

```
name: my-custom-skill
description: "Skill 的功能描述，包含触发条件、适用场景和不适用场景。"
```

**字段说明**

**字段**

**必填**

**说明**

name

是

Skill 的唯一标识名称。建议使用小写英文和连字符，如 `data-cleaner`、`invoice-parser`。

description

是

描述 Skill 的触发条件和处理能力。智能体根据此描述判断是否调用该 Skill，因此描述的质量直接影响 Skill 的调用准确率。

**description 编写建议**

description 的质量决定了智能体调用 Skill 的准确性。建议包含以下信息：

1.  **适用的输入类型**：明确 Skill 处理的文件格式或数据类型。
    
2.  **支持的操作**：列出 Skill 可以执行的具体操作。
    
3.  **触发关键词**：用户对话中可能出现的、应触发该 Skill 的关键词或表达方式。
    
4.  **不适用的场景**：标注不应触发该 Skill 的场景，避免误调用。
    

**完整示例**

以下是官方 xlsx Skill 的 SKILL.md 示例：

```
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
```

该示例中：

-   明确了支持的文件格式（.xlsx、.xlsm、.csv、.tsv）。
    
-   列出了适用操作（读取、编辑、创建、格式转换、数据清洗等）。
    
-   包含了触发场景描述（用户提到文件名或路径时也应触发）。
    
-   标注了不适用的场景（产出物为 Word、HTML、Python 脚本等情况）。
    

### 上传并创建

1.  在控制台左侧导航栏，选择**组件** > **Skill 管理**。
    
2.  点击右上角**自定义 Skill**按钮。
    
3.  在弹窗中，点击上传区域选择 ZIP 文件，或直接将文件拖拽到上传区域。
    
4.  点击**确认**提交。
    

提交后，系统会自动审查 Skill 内容，预计耗时约 2 分钟。

-   **审查通过**：Skill 出现在**自定义 Skill** 标签页中，可添加到智能体应用。
    
-   **审查未通过**：请根据提示修改 SKILL.md 内容后重新上传。
    

### 更新自定义 Skill

重新上传同名 Skill 的 ZIP 包时，系统会创建新版本。更新流程与首次创建一致：

1.  修改本地 ZIP 包中的内容（如更新 SKILL.md 中的 description）。
    
2.  在**自定义 Skill** 标签页中，重新上传 ZIP 包。
    
3.  审查通过后，已添加该 Skill 的智能体会自动使用最新版本。
    

## 添加 Skill 到智能体

可通过以下两种方式将 Skill（官方或自定义）添加到智能体应用。添加后，智能体在对话中遇到匹配 Skill 描述的任务时，会自动调用该 Skill 执行处理。

### 方式一：从 Skill 详情页添加

1.  在控制台左侧导航栏，选择**组件** > **Skill 管理**，点击目标 Skill 卡片进入详情页。
    
2.  点击右上角**添加到智能体**。
    
3.  在弹出的应用列表中选择目标应用，确认添加。
    

### 方式二：在应用配置中添加

1.  进入目标智能体应用的**应用配置**页面。
    
2.  在左侧配置面板中找到**技能**区域，点击 Skill 右侧的加号。
    
3.  从 Skill 列表中选择需要的 Skill，确认添加。
    

## 查看 Skill 详情

1.  在控制台左侧导航栏，选择**组件** > **Skill 管理**。
    
2.  在**官方 Skill** 或**自定义 Skill** 标签页中，点击目标 Skill 卡片进入详情页。
    

详情页包含两个标签：

-   **概览**：展示 Skill 的名称、当前版本号、功能描述和属性信息。通过版本下拉框可切换查看历史版本。
    
-   **更新记录**：展示该 Skill 全部版本的发布时间和变更内容。
    

官方 Skill 由平台统一维护和更新，已添加到智能体的官方 Skill 会自动使用最新版本。自定义 Skill 通过重新上传同名 ZIP 包来更新版本。

## 测试 Skill 效果

添加 Skill 后，可在应用配置页面右侧的对话窗格中测试效果。

例如，在对话窗格中发送：`帮我创建一个包含本月销售数据的表格，按地区分列统计`

智能体将调用 xlsx Skill，生成包含分列统计的 .xlsx 文件并提供下载。
