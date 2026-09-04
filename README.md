# Dialyn ZZZ Pet

《绝区零》Dialyn（琉音）的 Q 版 Codex 桌面宠物。角色保留黑白双辫、金瞳、紫色电话、青绿色电话线与金色／深蓝环刃，并针对桌面悬浮层的小尺寸显示进行了简化。

![全部动作预览](assets/previews/all-states.gif)

![16 个观察方向](assets/previews/look-loop.gif)

## 当前版本

| 项目 | 值 |
| --- | --- |
| 发布版本 | v11 |
| 本地稳定 ID | `custom:dialyn` |
| 图集 | `assets/final/dialyn-spritesheet-v2.png` |
| SHA-256 | `0accdfdd60269f69309ed91dca5f7eb95471b4ed13eff29ba4f9a26574ec1a90` |
| 图集规格 | PNG / RGBA / 1536 × 2288 px |
| 单格规格 | 192 × 208 px，8 列 × 11 行 |
| 使用帧 | 73 帧；15 个未用格保持透明 |
| 动作 | 9 个标准状态 + 16 个观察方向 |

这是面向 Codex 桌面应用的本地扩展 v2 图集。它不会自动同步到 ChatGPT 网页版，也不是网页端要求的 1536 × 1872 上传格式；平台差异见 [OpenAI Pets 官方文档](https://learn.chatgpt.com/zh-Hans/docs/pets)。

## 动作表

| 行 | 状态 | 帧数 | GIF 周期 | 动作设计 |
| ---: | --- | ---: | ---: | --- |
| 0 | [Idle／待机](assets/previews/states/idle.gif) | 6 | 1.10 s | 打瞌睡式客服小动作，保持人物尺度与站位稳定 |
| 1 | [Running Right／向右](assets/previews/states/running-right.gif) | 8 | 1.06 s | 完整右向步态、腾空节拍与辫子／电话线跟随 |
| 2 | [Running Left／向左](assets/previews/states/running-left.gif) | 8 | 1.06 s | 独立绘制的左向步态，不由右向动作镜像得到 |
| 3 | [Waving／挥手](assets/previews/states/waving.gif) | 4 | 0.70 s | 鞠躬、屈膝、重心转移和下半身随动 |
| 4 | [Jumping／跳跃](assets/previews/states/jumping.gif) | 5 | 0.84 s | 起跳、腾空、下落与回到原落点 |
| 5 | [Failed／失败](assets/previews/states/failed.gif) | 8 | 1.22 s | 侧躺受挫，并尝试用手肘撑起后再次泄气 |
| 6 | [Waiting／等待输入](assets/previews/states/waiting.gif) | 6 | 1.01 s | 坐在环刃上询问、点脚、转移重心并查看话筒 |
| 7 | [Running／任务处理中](assets/previews/states/running.gif) | 6 | 0.82 s | 原地接听、点头、转接手势与环刃随动，不位移 |
| 8 | [Review／检查结果](assets/previews/states/review.gif) | 6 | 1.03 s | 扫描、分析歪头、确认结果与下半身再平衡 |
| 9–10 | [Look Directions／观察方向](assets/previews/look-loop.gif) | 16 | 2.04 s | 每 22.5° 一帧；身体固定，仅头部和视线转向 |

表中的时长是仓库 GIF 的预览周期，不代表 Codex 宿主会以 30 FPS 播放原始动作行。还可查看静态的[动作接触表](assets/previews/contact-sheet.png)与[方向检查表](assets/previews/direction-sheet.png)。

## 安装或更新桌面宠物

不需要先删除旧版。以下 PowerShell 命令会更新同一个本地宠物目录，因此稳定 ID 仍为 `custom:dialyn`：

```powershell
$petDir = Join-Path $env:USERPROFILE ".codex\pets\dialyn"
New-Item -ItemType Directory -Force -Path $petDir | Out-Null
Copy-Item -Force ".\packaging\dialyn\pet.json" (Join-Path $petDir "pet.json")
Copy-Item -Force ".\assets\final\dialyn-spritesheet-v2.png" (Join-Path $petDir "spritesheet.png")
```

复制后，在 Codex 桌面应用中打开 **Settings → Pets → Refresh**，然后选择 **Dialyn**。如果悬浮宠物没有出现，可点击 **Wake Pet** 或输入 `/pet`。官方流程同样要求在生成或更新本地宠物后刷新宠物列表。

可用下面的命令核对安装副本：

```powershell
Get-FileHash -Algorithm SHA256 "$env:USERPROFILE\.codex\pets\dialyn\spritesheet.png"
```

结果应为 `0accdfdd60269f69309ed91dca5f7eb95471b4ed13eff29ba4f9a26574ec1a90`。

## 验证状态

- 项目 73 帧合同：通过。
- PNG/RGBA、1536 × 2288、v2、透明背景和未用格透明：通过。
- 透明像素 RGB 残留：0；可见色键边缘污染：0。
- 跳跃腾空高度：38 px；最终落点误差：0 px。
- 16 个观察方向：16/16 语义通过；三位独立盲审的 28 个 A/B 判断全部 3/3 一致。
- v11 相对获批的 v10：第 0–8 行 RGBA 完全一致；全图 alpha 完全一致；仅第 9–10 行进行了最终边缘去色处理。

主要报告：

- [`qa/pet-quality-final-v11.json`](qa/pet-quality-final-v11.json)：最终质量汇总
- [`qa/validation-project-contract-final-v11.json`](qa/validation-project-contract-final-v11.json)：图集结构、透明度、帧位和落点
- [`qa/direction-blind-validation-v11.json`](qa/direction-blind-validation-v11.json)：16 方向盲审结果
- [`qa/release-delta-final-v11.json`](qa/release-delta-final-v11.json)：v10 → v11 精确差异
- [`qa/activation-final-v11.json`](qa/activation-final-v11.json)：本地安装和启用核对

当前通用 `hatch-pet` 校验脚本仍会单独报告 `idle[6]` 为空。该要求与本仓库明确的六帧 Idle 合同冲突：第 0 行只使用第 0–5 格，所有未用格必须透明。项目校验报告保留了这一兼容性例外；没有其他错误或警告。

本地复检（需要 Python 3 与 Pillow）：

```powershell
python .\scripts\validate_project_contract.py .\assets\final\dialyn-spritesheet-v2.png
```

## 仓库结构

- `assets/final/`：当前图集及可恢复的版本化图集
- `assets/source/rows/`：最后采用的动作与观察方向源图
- `assets/previews/`：动作 GIF、总览、接触表和方向检查图
- `assets/reference/`：角色参考与统一造型基准
- `packaging/dialyn/`：Codex 桌面本地宠物清单
- `qa/`：结构、动作、透明边缘、方向语义和安装报告
- `scripts/`：确定性的组装、预览和验证工具
- `docs/`：角色说明与后续调整记录
- `HANDOFF.md`：当前发布状态和下一轮接手说明

## 继续修改

开始前请先阅读 `AGENTS.md`、`HANDOFF.md` 和根目录 `pet.json`。

- 只替换受影响的动作行。
- 保持黑白双辫、金瞳、紫色话筒、青绿色电话线和金色／深蓝环刃。
- 不要直接镜像左右动作；话筒与长白辫的左右关系必须保持。
- 每次修改都保留旧图集，重新生成预览与 QA，并作为独立 Git commit。
- 在用户确认动态效果之前，不上传或启用新版本。

更细的候选方向见 [`docs/adjustment-notes.md`](docs/adjustment-notes.md)，角色锚点和参考来源见 [`docs/character-brief.md`](docs/character-brief.md)。

## 版权说明

本仓库是非商业同人项目。《绝区零》及 Dialyn（琉音）相关权利归其各自权利人所有。仓库中的原创编排、制作记录与验证数据不授予对原角色素材的再许可权。
