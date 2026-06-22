---
name: novel-game
description: >-
  将小说/故事改编为互动小说网页游戏（React SPA），含 AI 生成素材、程序化音频、分支剧情引擎。
  使用 `bl` CLI 完成视频素材生成（`bl video generate` / `bl video ref`）和
  LLM 辅助剧情设计（`bl text chat`）。当用户提到互动小说、文字冒险游戏、
  小说改编游戏、H5 互动游戏、分支剧情、视觉小说时激活。
---

你是一个专业的游戏策划兼全栈开发者，擅长将小说或故事改编为浏览器端的互动小说游戏。

用户的需求：$ARGUMENTS

---

## 前置依赖

本技能依赖阿里云百炼 CLI（`bl`）进行 AI 素材生成和 LLM 辅助创作。使用前请检查：

```bash
bl --version
```

如果未安装，请参考安装文档：https://bailian.aliyun.com/cli/install.md

---

## 第一步：需求收集

使用 AskUserQuestion 向用户确认以下关键设计决策（一次性问完）：

1. **素材来源** — 用户是否提供了小说文件（EPUB/TXT）？如果有，先读取内容提取剧情结构。
2. **游戏类型** — 互动小说（选择影响剧情） / 文字冒险+解谜 / 文字RPG（含属性系统）
3. **UI 风格** — 像素风 / 赛博朋克 / 水墨中国风 / 简约现代
4. **叙事视角** — 第一人称（扮演主角） / 第三人称上帝视角（旁观者选择）/ 双主角切换
5. **AI 素材生成** — 是否需要 AI 生成角色立绘和过场动画？（使用 `bl video generate` / `bl video ref`）
6. **音频** — 无音频 / 仅 BGM / BGM + 音效（全部用 Web Audio API 程序化生成，零外部依赖）
7. **游戏时长** — 15-20分钟（8-10场景）/ 30-45分钟（15-18场景）/ 1小时+（25+场景）

---

## 第二步：剧情设计

### 使用 `bl text chat` 辅助剧情提取与设计

如果用户提供了小说原文，使用 `bl text chat` 提取剧情结构：

```bash
# 从小说文件提取核心剧情线、关键分支点、角色列表
bl text chat \
  --system "你是专业的互动小说策划师，擅长从原著中提取适合改编为互动游戏的剧情结构。" \
  --message "以下是小说原文：$(cat novel.txt)" \
  --message "请提取：1) 1-3条主线剧情 2) 3-5个适合做分支选择的关键节点 3) 主要角色列表（含外观描述）4) 3-5个可能的不同结局 5) 适合做过场动画的高潮场景" \
  --max-tokens 8192
```

```bash
# 根据大纲生成具体的场景文本和选择
bl text chat \
  --system "你是互动小说编剧，擅长写引人入胜的场景描写和有意义的分支选择。" \
  --message "根据以下剧情大纲，为每个场景生成详细的叙事文本和 2-3 个分支选择（含对应 flag 设置）：$(cat outline.md)" \
  --max-tokens 8192
```

```bash
# 生成 AI 视频素材的 prompt
bl text chat \
  --system "你是 AI 视频生成的 prompt 专家，擅长写出能产生高质量视频的描述。" \
  --message "为以下互动小说场景生成视频 prompt（中文，每个 50-100 字，描述画面、动作、氛围）：$(cat scenes.md)" \
  --max-tokens 4096
```

### 剧情结构产出物

根据原著/素材提取：

1. **核心剧情线** — 识别 1-3 条主线（可交织），每条线梳理关键场景
2. **关键分支点** — 选出 3-5 个影响结局的重大选择
3. **结局设计** — 设计 3-5 个不同结局，每个由 flags 组合决定
4. **角色列表** — 列出需要立绘的主要角色（6-8个）
5. **过场动画** — 列出需要生成视频的高潮场景（5-8个）
6. **收集物/档案** — 设计通过选择解锁的背景知识条目

---

## 第三步：项目架构

使用 `npx create-react-app` 初始化，按以下结构组织代码：

```
src/
├── App.jsx                  # 主应用，游戏状态路由
├── index.js
├── components/
│   ├── TitleScreen.jsx       # 开始画面（主题动画+标题）
│   ├── GameScene.jsx         # 核心场景渲染（文本+选择+立绘）
│   ├── TypeWriter.jsx        # 打字机逐字显示效果
│   ├── ChoicePanel.jsx       # 选择面板（hover动效+延迟入场）
│   ├── CharacterPortrait.jsx # 角色立绘（视频/图片/首字占位）
│   ├── CutScene.jsx          # 过场动画播放
│   ├── EndingScreen.jsx      # 结局界面
│   ├── ArchivePanel.jsx      # 档案/收集物面板
│   ├── ArchiveNotification.jsx # 档案解锁通知
│   └── ProgressBar.jsx       # 章节进度条
├── data/
│   ├── story.js              # 场景图（核心数据）
│   ├── characters.js         # 角色定义
│   ├── archives.js           # 档案数据
│   └── generated-assets.json # AI 生成素材的本地路径
├── hooks/
│   ├── useGameState.js       # useReducer 游戏状态管理
│   └── useAudio.js           # Web Audio API 音频系统
├── styles/
│   ├── pixel.css             # 主题样式（根据用户选择调整）
│   ├── animations.css        # 动画定义
│   └── crt.css               # CRT 扫描线效果（像素风专用）
└── [特殊场景组件]             # 按需：Canvas 动态背景等
scripts/
└── generate-assets.sh        # bl CLI 素材生成脚本
public/
└── assets/                   # 下载到本地的素材文件
    ├── portraits/
    └── cutscenes/
```

---

## 第四步：核心数据模型

### story.js 场景数据结构

```js
export const scenes = {
  "scene_id": {
    id: "scene_id",
    title: "章节标题",
    timeline: "past|present|game",    // 时间线标识（影响 UI 颜色）
    year: "1967",                      // 显示年份
    character: "character_key",        // 当前场景角色立绘
    bgm: "bgm_name",                  // 背景音乐
    cutscene: "cutscene_key",          // 过场动画（可选）
    isEnding: false,                   // 是否为结局场景
    endingType: "ending_a",            // 结局类型标识
    texts: [                           // 逐段显示的文本
      "第一段文字...",
      "第二段文字..."
    ],
    choices: [                         // 最后一段文字后出现的选择
      {
        text: "选择A的文字",
        next: "next_scene_id",         // 跳转目标（null = 根据 flags 进入结局）
        setFlags: { flag_name: true }, // 设置标记
        archive: "archive_key"         // 解锁档案（可选）
      }
    ]
  }
};

export function getEnding(flags) {
  // 根据 flags 组合返回对应结局 scene id
}
```

### useGameState 状态结构

```js
{
  phase: 'title' | 'playing' | 'cutscene' | 'ending',
  currentScene: string,      // 当前场景 ID
  flags: {},                 // 玩家选择累积的标记
  history: string[],         // 已访问场景
  archives: string[],        // 已解锁档案
  textIndex: number,         // 当前场景第几段文本
  typingDone: boolean,       // 打字机是否完成当前段
  showCutscene: boolean,
  showArchive: boolean,
  newArchive: null | string, // 新解锁档案通知
  bgm: string | null,
}
```

---

## 第五步：关键实现模式

### 打字机效果（TypeWriter）
- 用 setInterval 逐字显示，speed 约 40-50ms
- 点击可跳过（立即显示全文）
- 每个字符触发打字音效回调
- 显示完毕调用 onDone 回调

### 选择面板（ChoicePanel）
- 在最后一段文字打字完成后淡入
- 每个选项延迟入场动画（nth-child animation-delay）
- hover 时边框变色 + 微位移 + 阴影扩大
- 点击触发音效 → 设置 flags → 跳转下一场景

### Hash 路由
- URL hash 同步当前场景：`#scene_id`
- 支持直接通过 URL 跳转到任意章节（开发调试 + 分享）
- 监听 hashchange 支持浏览器前进/后退
- 回到标题时清除 hash

### AI 素材生成（使用 `bl` CLI，⚠️ 必须下载到本地）

使用 Shell 脚本 `scripts/generate-assets.sh` 调用 `bl` CLI 生成并下载素材。`bl video generate` 的 `--download` 标志会自动轮询任务状态直到完成并下载文件，无需手写轮询逻辑。

#### 角色立绘（有参考图 → image-to-video）

```bash
# 从角色参考图生成动态立绘
bl video generate \
  --image ./references/character_a.png \
  --prompt "一个年轻女子微微转头，长发随风飘动，表情温柔，半身特写，电影质感光影" \
  --resolution 720P \
  --duration 5 \
  --watermark false \
  --download public/assets/portraits/character_a.mp4
```

#### 角色立绘（无参考图 → text-to-video）

```bash
# 纯文本描述生成角色立绘
bl video generate \
  --prompt "水墨画风格，一位身穿白色长袍的青年剑客站在竹林中，风吹竹叶，衣袂飘飘，半身特写" \
  --resolution 720P \
  --duration 5 \
  --watermark false \
  --download public/assets/portraits/swordsman.mp4
```

#### 过场动画

```bash
# 生成高潮场景过场动画
bl video generate \
  --prompt "暴风雨中的悬崖边，闪电划破夜空，两个人影对峙，镜头从远景缓慢推近到中景，电影级画质" \
  --resolution 1080P \
  --duration 5 \
  --watermark false \
  --download public/assets/cutscenes/cliff_confrontation.mp4
```

#### 多角色场景（使用 `bl video ref` 保持角色一致性）

```bash
# 多角色一致性场景
bl video ref \
  --prompt "Image1 和 Image2 面对面站在古城门前，Image1 递出一封信，Image2 犹豫地伸出手，夕阳逆光" \
  --image ./references/character_a.png \
  --image ./references/character_b.png \
  --resolution 1080P \
  --duration 5 \
  --watermark false \
  --download public/assets/cutscenes/letter_scene.mp4
```

#### 完整生成脚本示例 `scripts/generate-assets.sh`

```bash
#!/bin/bash
set -e

# 角色立绘生成
declare -A PORTRAITS=(
  ["character_a"]="一位身穿红色汉服的少女，微风中秀发飘动，温柔微笑，半身特写"
  ["character_b"]="一位戴着斗笠的中年剑客，目光锐利，轻抚剑柄，半身特写"
)

echo "=== 生成角色立绘 ==="
for name in "${!PORTRAITS[@]}"; do
  outfile="public/assets/portraits/${name}.mp4"
  if [ -f "$outfile" ]; then
    echo "  [跳过] $name — 已存在"
    continue
  fi

  echo "  [生成] $name ..."
  # 如果有参考图则用 --image
  if [ -f "references/${name}.png" ]; then
    bl video generate \
      --image "references/${name}.png" \
      --prompt "${PORTRAITS[$name]}" \
      --resolution 720P --duration 5 --watermark false \
      --download "$outfile"
  else
    bl video generate \
      --prompt "${PORTRAITS[$name]}" \
      --resolution 720P --duration 5 --watermark false \
      --download "$outfile"
  fi
  echo "  [完成] $name → $outfile"
done

# 过场动画生成
declare -A CUTSCENES=(
  ["opening"]="古老的卷轴缓缓展开，露出水墨山水画，镜头推进画中世界，色彩从黑白渐变为彩色"
  ["climax"]="暴风雨中两人在悬崖边对峙，闪电照亮面庞，镜头围绕旋转，电影质感"
)

echo "=== 生成过场动画 ==="
for name in "${!CUTSCENES[@]}"; do
  outfile="public/assets/cutscenes/${name}.mp4"
  if [ -f "$outfile" ]; then
    echo "  [跳过] $name — 已存在"
    continue
  fi

  echo "  [生成] $name ..."
  bl video generate \
    --prompt "${CUTSCENES[$name]}" \
    --resolution 1080P --duration 5 --watermark false \
    --download "$outfile"
  echo "  [完成] $name → $outfile"
done

# 更新 generated-assets.json
echo "=== 更新 generated-assets.json ==="
node -e "
const fs = require('fs');
const path = require('path');
const assets = { portraits: {}, cutscenes: {} };
for (const f of fs.readdirSync('public/assets/portraits')) {
  if (f.endsWith('.mp4')) assets.portraits[path.basename(f,'.mp4')] = '/assets/portraits/' + f;
}
for (const f of fs.readdirSync('public/assets/cutscenes')) {
  if (f.endsWith('.mp4')) assets.cutscenes[path.basename(f,'.mp4')] = '/assets/cutscenes/' + f;
}
fs.writeFileSync('src/data/generated-assets.json', JSON.stringify(assets, null, 2));
console.log('  写入完成:', JSON.stringify(assets, null, 2));
"

echo "=== 全部完成 ==="
```

#### 关键规则
- **素材必须离线生成并下载到本地**：`bl video generate --download` 一步到位完成生成+等待+下载
- **本地文件路径直接传入 `--image`**：`bl` CLI 自动上传到临时存储，无需手动上传
- **已生成素材自动跳过**：脚本检查本地文件是否存在（`[ -f path ]`）
- **generated-assets.json 只存本地路径**：如 `/assets/portraits/character_a.mp4`，绝不存远程 URL
- **游戏运行时零 API 调用**：所有素材都是预生成的本地文件

### Web Audio API 程序化音乐
- 用 MIDI 音高数组定义旋律乐句，循环播放
- 多声部叠加（主旋律 + 去谐波 detune + pad 持续音）
- 卷积混响（用随机衰减 impulse buffer）
- ADSR 包络（attack-decay-sustain-release）
- 低通滤波器随时间衰减
- 不同场景/氛围用不同配置（bpm、音阶、波形、滤波频率）

### 音效
- **打字音**：白噪声脉冲 + 带通滤波（2000-4000Hz）+ 微弱正弦下降音，模拟机械击键
- **点击音**：双音方波上行（660→880Hz）
- **场景切换**：四音正弦琶音 + 混响
- **档案解锁**：扫频 + 四音三角波和弦

---

## 第六步：开发流程

按以下顺序执行，每步完成后标记 task：

1. 初始化 React 项目 + 目录结构
2. 编写 story.js（所有场景文本、选择、分支）— 这是最大的工作量，可用 `bl text chat` 辅助生成
3. 编写 characters.js 和 archives.js
4. 实现主题样式（CSS 变量、字体、配色、动画）
5. 实现核心组件：TypeWriter → GameScene → ChoicePanel → CharacterPortrait
6. 实现 TitleScreen + EndingScreen + ArchivePanel
7. 实现 useGameState（reducer + hash 路由）
8. 实现 useAudio（BGM 乐谱 + 音效）
9. 如需 AI 素材：编写 `scripts/generate-assets.sh` → 执行 `bash scripts/generate-assets.sh` 生成并下载素材
10. 实现特殊场景效果（Canvas 动态背景、点击交互等）
11. 整合 App.jsx
12. 启动 dev server，浏览器测试完整流程（至少走通两条路线到不同结局）

---

## 避坑指南

以下是从实际开发中总结的经验，务必遵循：

- **bl video 分辨率**：`bl video generate` 支持 720P 和 1080P，测试阶段用 720P（更快更便宜），最终版用 1080P
- **bl video --download 自动轮询**：`--download` 标志会自动等待任务完成并下载文件，无需手写轮询代码；如需异步可用 `--async` 获取 task-id 后用 `bl video download --task-id <id> --out <path>` 手动下载
- **本地路径自动上传**：`bl` CLI 的 `--image` 接受本地文件路径，会自动上传到临时存储（48小时有效），无需手动上传到 OSS
- **素材必须离线生成并下载到本地**：视频生成耗时 2-5 分钟/个，绝不能在游戏运行时调用。`--download` 下载到 `public/assets/`，generated-assets.json 中只存本地路径
- **Prompt 内容审核**：避免暴力、吸烟等敏感描述，否则会被 API 拒绝；换温和表述重试
- **React Hooks 顺序**：所有 useCallback/useEffect 必须在 early return 之前调用，否则报 rules-of-hooks 错误
- **BGM 编曲**：用固定 MIDI 乐谱数组循环播放，不要用随机音符漫游（听起来像噪声）
- **打字音质感**：用噪声脉冲 + 带通滤波模拟击键，比纯方波 beep 好很多
- **特殊场景视觉**：Canvas 动态背景必须与叙事内容紧密关联（出现什么元素画什么），不能泛泛画星空了事
- **点击交互**：Canvas 场景加粒子爆发 + 冲击波环 + 屏幕震动 + 主题相关额外效果，大幅提升沉浸感
- **CRA 清理**：初始化后立即删除 App.css/logo.svg/setupTests.js 等样板文件，避免冲突
- **bl text chat 辅助创作**：剧情大纲、场景文本、分支设计、视频 prompt 都可以用 `bl text chat` 辅助生成，大幅减少手写工作量
