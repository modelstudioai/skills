# token plan playbooks

`token plan playbooks` 是一组经过实测验证的端到端 AI 应用模式集合，覆盖 AI Coding、内容创作、资料与数据处理、生活娱乐、求职职场五大场景，共 42 个具体玩法。每个 playbook 提供结构化提示词模板、模型调用链路说明及实测产出示例，适用于订阅 Token Plan 的开发者快速复现高价值工作流。实际 Credits 消耗与输出效果请以控制台“用量详情”为准。

## 支持的模型与功能

Playbooks 调用底层多模态模型组合，非单一模型能力：
- **文本理解与生成**：Qwen3.5-plus（长上下文）、Qwen3.8-flash（低延迟高吞吐）  
- **视觉理解与生成**：Qwen3.8-flash-vl（截图/文档/长图解析）、wan3.0-video（视频生成）  
- **代码与结构化输出**：Qwen3.5-plus（支持 JSON Schema 强约束输出，如 `token-plan-playbook-cmd-guard.md` 中要求的 5 字段固定格式）  
- **Agent 编排**：OpenClaw（支持多步工具调用，如 [一句话规划周末出游 · 多步 Agent](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-weekend-planner.md)）  

> **注意**：文档中提及的 `wan3.0-video` 在当前生产环境已统一为 `wan3.5-video`，旧链接仍可访问但建议在新实现中使用新版模型标识；该不一致已在 [玩法攻略](../../raw/token-plan-user-guide/token-plan-playbooks.md) 的后续修订版中同步。

## 关键参数

所有 playbooks 均依赖以下核心参数控制行为与输出质量：
- `model`：必须显式指定（如 `qwen3.8-flash-vl`, `wan3.5-video`），不可省略  
- `response_format`：对结构化输出类玩法（如 `token-plan-playbook-cmd-guard.md`、`token-plan-playbook-drama-script.md`）必须设为 `json_object` 并提供严格 schema  
- `max_tokens`：视觉理解类（如截图分析、票据 OCR）建议 ≥ 2048；视频生成类需按帧率预估（30 秒视频建议 ≥ 4096）  
- `tools`：Agent 类玩法（如 `token-plan-playbook-openclaw-agent.md`）需声明可用工具集，未声明则禁用联网/文件读取等扩展能力  

## 使用方式

1. **定位 playbook**：从 [玩法攻略](../../raw/token-plan-user-guide/token-plan-playbooks.md) 分类速览或玩法总表中选择目标场景与具体条目  
2. **复用提示词模板**：每个 playbook 页面（如 [AI 代码安全审计 · 定位到修复](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-code-security.md)）提供可直接粘贴的提示词结构，含角色设定、输入约束与输出指令  
3. **构造请求体**：按对应模型的 API 规范组装，特别注意多模态输入（如 `images: ["data:image/png;base64,..."]`）与 `response_format` 配置  
4. **验证输出结构**：对 JSON 输出类玩法，务必校验字段完整性（如 `token-plan-playbook-commit-writer.md` 要求 `type`, `scope`, `subject`, `body`, `isBreakingChange` 五字段全量存在）  

## 限制和注意事项

- **Credits 计费粒度**：按实际调用的模型与输入 token 数计费，视觉模型按图像分辨率与数量额外计费（详见控制台用量明细），非按“玩法”统一定价  
- **输入长度限制**：Qwen3.5-plus 最大上下文为 32768 tokens，但 `token-plan-playbook-doc-qa.md` 等长文档玩法建议分块提交，避免截断  
- **多模态输入一致性**：`token-plan-playbook-screenshot-to-code.md` 要求截图必须为清晰 UI 截图（非设计稿），模糊或含水印图像将导致 CSS 还原失败  
- **Agent 安全边界**：OpenClaw 类玩法（如 [OpenClaw 个人任务管家](../../raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-openclaw-agent.md)）默认禁用写文件、执行 shell 命令等高危动作，需显式授权才启用  
- **输出稳定性**：视频生成类（如 `token-plan-playbook-cinematic-broll.md`）受 seed 控制，相同提示词可能产生不同运镜，需固定 `seed` 参数复现结果

## 来源文档

- [玩法攻略](../../raw/token-plan-user-guide/token-plan-playbooks.md)


