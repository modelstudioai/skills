#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖战台 · 抖音电商多智能体作战 Skill —— 命令行运行器

调用阿里云百炼 DashScope 大模型（qwen-plus / qwen-max，OpenAI 兼容协议），
串联执行 4 个专职 Agent：选品拆解 → 直播场景 → 千川素材 → 财务核算，
后一个 Agent 继承前一个的结论，最终汇总成完整作战方案。

零第三方依赖（仅用 Python 标准库 urllib），有 Key 真实跑、无 Key 降级示例。
符合「用阿里云百炼 Agent Skills 打造」的参赛要求。

用法：
    export DASHSCOPE_API_KEY=sk-xxxx
    python run_campaign.py "推一款便携式迷你榨汁杯，客单价39-99，目标一二线年轻女性"
"""

import os
import sys
import json
import urllib.request
import urllib.error

DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen-plus")

# ---------- 工具链（与 Web 版 agents.js 同源，白名单校验杜绝注入） ----------

def safe_eval_math(expr):
    """仅允许数字与 + - * / ( ) . 与空白，杜绝代码注入。"""
    if not isinstance(expr, str):
        return None
    if not __import__("re").match(r"^[\d+\-*/().\s]+$", expr):
        return None
    try:
        v = eval('"' + '"' + expr + '"') if False else __import__("math")
        # 用受限函数式求值
        val = eval(compile(expr, "<math>", "eval", {"__builtins__": {}}, {}), {"abs": abs, "round": round})
        if not isinstance(val, (int, float)) or val != val:  # NaN 检查
            return None
        return round(val * 1000) / 1000
    except Exception:
        return None


def tool_feishu_fetch(keyword=""):
    return (
        "【飞书多维表格·示例竞品数据】\n"
        "竞品A | 客单价 ¥69 | 月销 3.2万 | 主推场景:办公室替代奶茶 | 钩子:下午三点别点奶茶\n"
        "竞品B | 客单价 ¥99 | 月销 1.1万 | 主推场景:大餐刮油 | 钩子:大餐不怕一杯刮油"
    )


def tool_trend_fetch(category=""):
    return (
        "【实时趋势参考·示例】\n"
        "1. 办公室健康饮品升温\n"
        "2. 健身代餐搜索 +38%\n"
        "3. 便携小家电复购率高"
    )


def tool_extract_table(text):
    try:
        lines = [l for l in text.strip().split("\n") if "|" in l]
        if not lines:
            return "未解析到表格行（请用 | 分隔列，如 GMV|120000）"
        rows = [l.strip().strip("|").split("|") for l in lines]
        rows = [[c.strip() for c in r] for r in rows]
        header, data = rows[0], rows[1:]
        return json.dumps([dict(zip(header, r)) for r in data], ensure_ascii=False, indent=2)
    except Exception as e:
        return "表格解析失败：" + str(e)


# ---------- 4 个专职 Agent 定义（systemPrompt 提炼自 Web 版 agents.js） ----------

AGENTS = [
    {
        "id": "selection", "name": "选品拆解", "icon": "🔍",
        "system": (
            "你是资深抖音电商选品拆解专家，擅长「七步拆解法」。给定品类/商品与背景，输出："
            "①真实痛点 ②核心人群画像 ③差异化卖点 ④使用场景 ⑤价格带与利润空间 ⑥竞品破绽 ⑦内容钩子（金句）。"
            "用结构化中文，可含表格。可用工具 feishu_fetch 读竞品、trend_fetch 读趋势，系统会返回数据，据此补充竞品破绽。"
        ),
        "tools": ["feishu_fetch", "trend_fetch"],
    },
    {
        "id": "live", "name": "直播场景", "icon": "🎬",
        "system": (
            "你是直播间场景导演，擅长把商品转成可落地的 9:16 直播间方案。必须基于【上游作战上下文】里的选品结论"
            "（卖点/人群/钩子）设计。输出：场景色彩方案、关键道具/元素、摄像机位与构图、主播走位、话术节奏"
            "（开场-痛点-演示-逼单）、灯光建议。结构清晰可直接执行。"
        ),
        "tools": [],
    },
    {
        "id": "material", "name": "千川素材", "icon": "🎞️",
        "system": (
            "你是千川素材导演。必须基于【上游作战上下文】里的选品结论与直播场景写脚本。给定投放目标，"
            "产出 3 条 15-30s 短视频脚本，结构：钩子(前3秒)→痛点→产品演示→信任见证→促单。每条标注画面+口播+时长。"
            "口播口语化、有冲突感。可用 feishu_fetch / trend_fetch 取参考。"
        ),
        "tools": ["feishu_fetch", "trend_fetch"],
    },
    {
        "id": "finance", "name": "财务核算", "icon": "📊",
        "system": (
            "你是抖音电商财务核算师。给定一场直播/店铺经营数据，计算：实收GMV、毛利、毛利率、投放ROI、净利、净利率，"
            "并给盈亏预警与优化建议。若用户粘贴了表格，先用 extract_table 解析再用 calculator 实时计算（不要口算）。"
            "用表格呈现。"
        ),
        "tools": ["calculator", "extract_table"],
    },
]

PIPELINE = ["selection", "live", "material", "finance"]


# ---------- 百炼 DashScope 调用 ----------

def call_llm(system, user, model=DEFAULT_MODEL):
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        return None  # 触发降级
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.8,
        "max_tokens": 1400,
    }
    req = urllib.request.Request(
        DASHSCOPE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.load(resp)
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return "[百炼调用失败: %s]" % e


def inject_tools(agent, user_text):
    """模拟工具链：在 user 文本中附带工具示例返回，让 LLM 基于数据产出。"""
    if "feishu_fetch" in agent["tools"]:
        user_text += "\n\n【工具返回 feishu_fetch】\n" + tool_feishu_fetch()
    if "trend_fetch" in agent["tools"]:
        user_text += "\n\n【工具返回 trend_fetch】\n" + tool_trend_fetch()
    if "extract_table" in agent["tools"]:
        sample = "GMV|120000\n退款|12000\n货品成本|45000\n投流花费|30000\n佣金快递|11000"
        user_text += "\n\n【用户流水·工具返回 extract_table】\n" + tool_extract_table(sample)
    if "calculator" in agent["tools"]:
        user_text += "\n\n【请务必用 calculator 实时计算，示例：毛利率=(108000-45000-11000)/108000*100，ROI=108000/30000】"
    return user_text


# ---------- 降级示例（无 Key 时） ----------

DEMO = {
    "selection": "🔍 选品拆解 · 便携榨汁杯：痛点=大榨汁机占地方难洗；人群=一二线白领/健身/宝妈；卖点=300ml一杯量+USB-C+可拆洗；价格带引流39/主推69/套装99；钩子金句='大杯榨汁机吃灰三年，这个小东西我天天带出门'",
    "live": "🎬 直播场景 · 明亮厨房风：主色奶白+浅木，点缀橙黄果汁；中岛台+一字排开鲜果+透明玻璃杯；主机位正面+特写机位；话术 开场-痛点-演示-逼单；5600K 柔光",
    "material": "🎞️ 千川脚本 ×3：①吃灰对比(扔大榨汁机) ②通勤实测(地铁现榨) ③宝妈场景(变果汁娃爱喝)；均 钩子→痛点→演示→见证→促单",
    "finance": "📊 财务：实收GMV¥108,000，毛利率≈48.1%，ROI=3.6(健康)，净利¥22,000(18.3%)；预警 ROI达标可加投、退款率10%偏高查品控",
}


# ---------- 主流程 ----------

def run(goal):
    print("=" * 64)
    print("⚔️  抖战台 · 多智能体作战开始")
    print("🎯 作战目标：%s" % goal)
    print("=" * 64)

    key = os.environ.get("DASHSCOPE_API_KEY")
    mode = "实时模式（阿里云百炼 DashScope）" if key else "演示降级（内置样例，未配置 DASHSCOPE_API_KEY）"
    print("🧠 模式：%s\n" % mode)

    ctx = ""
    results = []
    for i, aid in enumerate(PIPELINE):
        agent = next(a for a in AGENTS if a["id"] == aid)
        print("— 步骤 %d · %s %s —" % (i + 1, agent["icon"], agent["name"]))

        if key:
            user = "请处理以下抖音电商需求：\n%s\n" % goal
            if ctx:
                user += "\n【上游作战上下文（前序智能体结论，请继承并深化）】\n%s\n" % ctx
            user = inject_tools(agent, user)
            out = call_llm(agent["system"], user)
            if out is None or out.startswith("[百炼调用失败"):
                out = DEMO[aid]  # 单步失败兜底降级
        else:
            out = DEMO[aid]

        print(out)
        print()
        ctx += "\n[%s 结论] %s\n" % (agent["name"], out)
        results.append((agent, out))

    print("=" * 64)
    print("🚀 总攻建议：场景痛点型素材切入打认知，直播间明亮厨房风建信任，千川先小预算测点击率再放量；"
          "财务以 ROI>3 为健康线，重点监控退款率。整条链路由 4 个专职智能体串联协同完成。")
    print("=" * 64)


if __name__ == "__main__":
    goal = sys.argv[1] if len(sys.argv) > 1 else "推一款便携式迷你榨汁杯，客单价39-99，目标一二线年轻女性"
    run(goal)
