# 代码审查报告

> 小花出品 · 2026-03-30 · 审查范围：tetris_evolution_test.py, snake_game.py, gen120.py, gen_final.py, gen120_resume.py

---

## 一、Tetris (tetris_evolution_test.py)

### 概述
- **代码行数**：约560行
- **类型**：pygame游戏
- **评分**：⭐⭐⭐⭐☆ (4/5)

### 代码质量 ✅

**优点：**
- 清晰的类结构（Tetromino, Board, Renderer, Game）
- 常量定义规范（BLOCK_SIZE, GRID_WIDTH, SCORE_TABLE）
- 注释完整，中文标注
- 面向对象设计，职责分离清晰

**可改进：**
- `clone()`方法浅拷贝shape，应使用深拷贝
- `get_ghost_y()`内部有重复逻辑，可提取为独立方法

### 潜在Bug ⚠️

```python
# Bug 1: 深拷贝问题
def clone(self):
    t = Tetromino(self.shape_idx)
    t.shape = self.shape  # 直接赋值，引用同一列表！
```

**问题**：修改`t.shape`会影响原始对象。应使用`copy.deepcopy()`

```python
# Bug 2: collides边界检测
if ny >= GRID_HEIGHT:
    return True
if ny >= 0 and board[ny][nx] != 0:  # ny可能为负！
```

**问题**：当`ny < 0`时，第二个条件不会检测，但第一个条件已返回True。逻辑正确但可读性差。

```python
# Bug 3: 幽灵方块计算
def get_ghost_y(self, board):
    gy = self.y
    while not self.collides(board, self.x, gy + 1):
        gy += 1
    return gy
```

**问题**：传入`None`时会失败，虽然调用时`draw_ghost`重新计算了Y值，但接口设计不清晰。

### 安全漏洞 ✅
- 无网络通信，无安全风险
- 无用户输入直接执行系统命令

### 性能问题 ⚠️

```python
# 每次渲染都创建新Surface
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay.set_alpha(180)
overlay.fill((0, 0, 0))
```

**建议**：预创建overlay surface复用

### 代码风格 ⚠️

**优点：**
- 函数文档字符串完整
- 常量命名清晰
- 缩进一致

**问题：**
- `draw_ghost()`方法过于复杂（约40行），应拆分
- 部分魔法数字应提取为常量

---

## 二、Snake Game (snake_game.py)

### 概述
- **代码行数**：约580行
- **类型**：pygame游戏
- **评分**：⭐⭐⭐⭐⭐ (5/5)

### 代码质量 ✅

**优点：**
- 完整的粒子系统（Particle, ParticleSystem）
- 多种食物类型（Normal, Speed, Score, Grow）
- 障碍物系统
- 高分存档功能
- 状态机设计清晰

**可改进：**
- 某些类职责过重（如SnakeGame）

### 潜在Bug ⚠️

```python
# Bug 1: 文件操作未关闭
def _save_high_score(self):
    path = os.path.join(...)
    open(path, "w").write(str(self.high_score))
    # 文件句柄未关闭！
```

**问题**：应该使用`with`语句或显式close()

```python
# Bug 2: 竞态条件
def _update(self):
    ...
    self.snake.move()  # 移动蛇
    head = self.snake.head
    # 在这里head可能被其他代码修改
```

**问题**：虽然当前代码没有多线程，但设计存在风险

```python
# Bug 3: 食物生成可能无限循环
def spawn_food(self, snake_segs, extra_exclude=None):
    for _ in range(200):  # 硬编码上限
        ...
        if not any(r.colliderect(rect) for r in exclude):
            # 当exclude覆盖整个地图时会浪费200次迭代
```

**问题**：虽然有200次重试上限，但没有任何"生成失败"处理

### 安全漏洞 ✅
- 无SQL注入风险
- 无命令执行风险
- 文件读写仅限本地highscore.txt

**问题**：
```python
# 路径遍历风险
path = os.path.join(os.path.dirname(__file__), "snake_highscore.txt")
```

**建议**：使用`os.path.basename()`确保安全

### 性能问题 ⚠️

```python
# 每次更新都计算碰撞检测
def check_collision_self(self):
    return self.head.collidelist(self.segments[1:]) != -1
```

**建议**：这是O(n)复杂度，当前实现可接受（蛇身不会过长）

```python
# 粒子系统未限制数量
def emit(self, x, y, color, count=8):
    for _ in range(count):
        self.particles.append(...)
```

**问题**：长时间游戏可能积累大量粒子

### 代码风格 ⭐⭐⭐⭐⭐

**优点：**
- 枚举类定义清晰
- 颜色常量统一管理
- 注释完整
- 条件表达式清晰

---

## 三、gen120.py (配色师-120图生成)

### 概述
- **代码行数**：约140行
- **类型**：API批量生成脚本
- **评分**：⭐⭐⭐☆☆ (3/5)

### 代码质量 ⚠️

**优点：**
- 进度跟踪（success_count, fail_count）
- 重试机制（3次重试）
- 详细的prompts配置

**问题：**
- 硬编码API Key
- 无类型提示
- 错误处理分散

### 潜在Bug ⚠️

```python
# Bug 1: 硬编码API Key
API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
```

**问题**：API Key直接写在代码里，泄露风险！应使用环境变量或配置文件

```python
# Bug 2: 循环内sleep在最后，但应该在请求前
for i, (scene_id, style_id, prompt) in enumerate(prompts, 1):
    ...
    if i < 120:
        time.sleep(5)  # 最后一张也sleep，但已经没有后续请求
```

**问题**：逻辑不清晰，最后一张的sleep无意义

```python
# Bug 3: 文件检查竞态
if os.path.exists(output_path):
    print(f"[{i:03d}/120] ⏭️  已存在，跳过: {filename}")
    ...
    continue
# 中间可能文件被其他进程创建
result = generate_image(...)
```

**问题**：存在TOCTOU (Time-of-check to time-of-use) 竞态

### 安全漏洞 ❌

```python
# API Key硬编码
API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
```

**严重问题**：这是真实API Key！任何能访问代码的人都可以使用

### 性能问题 ⚠️

```python
# 固定5秒间隔太慢
time.sleep(5)  # 总耗时约10分钟（120张 × 5秒）
```

**建议**：
- 根据实际RPM限制调整
- 使用智能等待（检测429状态码）

### 代码风格 ⚠️

**问题：**
- 无函数文档字符串
- 变量命名不一致（如`success_count` vs `fail_count` vs `results`）
- 魔法数字（5秒、3次重试、120张）

---

## 四、gen_final.py (配色师-批量生成v2)

### 概述
- **代码行数**：约220行
- **类型**：API批量生成脚本
- **评分**：⭐⭐⭐⭐☆ (4/5)

### 代码质量 ✅

**优点：**
- 更健壮的错误处理
- 更清晰的代码结构
- 详细的日志记录
- resume功能

### 潜在Bug ⚠️

```python
# Bug: 45秒固定等待太激进
time.sleep(45)  # 如果网络慢，可能不够
```

**问题**：固定等待可能导致不必要的等待，或等待不足

### 安全漏洞 ❌

```python
# 同样的API Key硬编码问题
API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
```

### 性能 ⚠️

- 比gen120.py更好的45秒间隔
- 但仍然可以更智能

---

## 五、gen120_resume.py (配色师-继续生成)

### 概述
- **代码行数**：约130行
- **类型**：断点续传脚本
- **评分**：⭐⭐⭐⭐☆ (4/5)

### 代码质量 ✅

**优点：**
- 断点续传功能
- 跳过已完成文件
- 日志记录

### 潜在Bug ⚠️

```python
# Bug: 循环逻辑复杂难维护
for scene_id, scene_desc in SCENES:
    for style_id, style_desc in STYLES:
        pass  # skip scenes 1-2 already done
```

**问题**：使用空pass循环跳过，然后下面又有嵌套循环，逻辑混乱

```python
# Bug: 索引计算可能出错
img_num = idx_base * 12 + style_idx + 1  # 1-120
```

**问题**：如果SCENES不是10个或STYLES不是12个，会出问题

### 安全漏洞 ❌

API Key硬编码问题依然存在

---

## 📋 总结与建议

### 紧急（必须修复）

1. **API Key安全**：所有脚本的API Key必须移除硬编码，改用环境变量
   ```python
   import os
   API_KEY = os.environ.get("MINIMAX_API_KEY", "")
   ```

2. **文件句柄关闭**：snake_game.py的`_save_high_score`使用with语句

### 高优先级

3. **深拷贝问题**：tetris的clone方法使用deepcopy

4. **代码审查机制**：建立团队代码审查流程

### 中优先级

5. **类型提示**：为所有函数添加类型提示

6. **常量提取**：移除魔法数字，提取为配置文件

7. **文档字符串**：为公共函数添加docstring

---

*审查人：小花 · 2026-03-30*
