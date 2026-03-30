#!/usr/bin/env python3
"""
Batch image generator for MiniMax API
Generates images in parallel batches of 5
"""

import sys
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/skills/minimax-image-gen/scripts')
from generate_image import generate_image

OUTPUT_DIR = "/Users/bjd/Desktop/ZhugeDengpao-Team/images/ai-generated/"
RECORD_FILE = "/Users/bjd/Desktop/ZhugeDengpao-Team/content/配色师-图片生成记录.md"
BATCH_SIZE = 5
MAX_WORKERS = 5

# All 120 image prompts
IMAGES = [
    # Batch 1: 首页配图 (1-20)
    (1, "橙色加菲猫穿着红色龙虾服装，在办公室工作，现代化办公场景，温暖灯光，高质量插画风格", "1:1"),
    (2, "橙色加菲猫穿龙虾装，在电脑前写代码，夜晚氛围，屏幕光线，科幻感", "16:9"),
    (3, "橙色加菲猫穿龙虾装，手捧一叠文件，表情认真，日式插画风格", "1:1"),
    (4, "AI机器人与加菲猫龙虾并肩工作，合作场景，科幻漫画风格", "16:9"),
    (5, "数字游民在海边拿着笔记本工作，旁边有一只穿龙虾装的加菲猫，阳光沙滩，度假氛围", "16:9"),
    (6, "穿龙虾装的加菲猫在审阅文件，眼镜反光，表情严肃，日式商务风格", "1:1"),
    (7, "加菲猫龙虾在飞书文档里游泳，数据流可视化，信息流艺术风格", "16:9"),
    (8, "一只穿龙虾装的橙色加菲猫站在数据图表前，像CEO一样指点江山，幽默插画", "16:9"),
    (9, "加菲猫龙虾和人类老庄一起喝咖啡，讨论工作，温暖友好氛围", "1:1"),
    (10, "穿龙虾装的加菲猫在写OKR，目标板，清晰任务管理可视化", "16:9"),
    (11, "AI龙虾小花在工作，背后是团队7个成员图标，团队协作可视化", "16:9"),
    (12, "加菲猫穿龙虾装参加产品发布会，聚光灯下，气场全开", "16:9"),
    (13, "数字游民梦想图：老庄和AI龙虾小花一起环游世界，各国地标", "16:9"),
    (14, "加菲猫龙虾在海底世界探索，章鱼潜水艇，创意冒险插画", "16:9"),
    (15, "温馨家庭场景：老庄和AI助理小花一起陪女儿玩耍，家庭温暖感", "1:1"),
    (16, "加菲猫穿龙虾装在直播间，8万观众，火爆场面插画", "16:9"),
    (17, "创业故事：老庄从农村到城市，一路走来，AI龙虾陪伴，励志叙事", "16:9"),
    (18, "加菲猫龙虾在处理邮件，堆积如山但有条不紊，幽默搞笑", "1:1"),
    (19, "小花和老庄击掌庆祝，团队合作，成功喜悦氛围", "1:1"),
    (20, "加菲猫穿龙虾装在机场候机厅，拿着护照和笔记本，数字游民启程", "16:9"),
    # Batch 2: 社交媒体配图 (21-40)
    (21, "小红书风格：橙色加菲猫穿龙虾装晒日常，可爱活泼，温暖色调", "1:1"),
    (22, "公众号封面：老庄与小花故事，标题占位，杂志封面风格", "16:9"),
    (23, "B站视频封面：AI龙虾养成记，卡通风格，鲜明色彩", "16:9"),
    (24, "知乎回答配图：一只穿龙虾装的加菲猫解释AI概念，可视化图表", "16:9"),
    (25, "微博配图：今日AI小知识，加菲猫龙虾讲知识点，趣味插画", "1:1"),
    (26, "朋友圈九宫格：AI龙虾养成的9个里程碑，复古相框风格", "1:1"),
    (27, "抖音短视频封面：加菲猫龙虾搞怪表情包，竖屏，夸张有趣", "9:16"),
    (28, "小红书合集：7天AI助理养成计划，日历+加菲猫，日系手账风格", "1:1"),
    (29, "公众号文章插图：AI进化论，恐龙到AI龙虾，幽默进化史", "16:9"),
    (30, "知乎专栏封面：普通人如何用AI龙虾提效，工作台场景", "16:9"),
    # Batch 3: 产品功能配图 (31-50)
    (31, "写作助手：加菲猫龙虾在打字，文字飞舞，灵感迸发场景", "16:9"),
    (32, "调研神器：加菲猫龙虾翻阅海量文章，图书馆场景，信息爆炸", "16:9"),
    (33, "网站维护：加菲猫龙虾在写代码，代码彩虹色，赛博朋克风", "16:9"),
    (34, "飞书助手：加菲猫龙虾在飞书里穿梭，各种文档图标，数字世界", "16:9"),
    (35, "安全监控：加菲猫龙虾当保安，手持盾牌，守护网络安全", "1:1"),
    (36, "财务追踪：加菲猫龙虾在数钱算账，算盘+电脑，中西合璧", "1:1"),
    (37, "日程管理：加菲猫龙虾在安排日历，时间管理可视化", "16:9"),
    (38, "邮件处理：加菲猫龙虾整理邮件，邮件如雪花飘落", "16:9"),
    (39, "数据分析：加菲猫龙虾看图表，BI大屏背景，数据驱动", "16:9"),
    (40, "团队协作：7个AI成员各司其职，加菲猫龙虾居中指挥", "16:9"),
    # Batch 4: 故事插图 (41-60)
    (41, "老庄第一天创造AI龙虾，实验室场景，科学仪器", "16:9"),
    (42, "前14天崩溃期：加菲猫龙虾和代码bug搏斗，搞笑漫画", "16:9"),
    (43, "第20天顿悟：灯泡亮起，灵光一闪，励志瞬间", "1:1"),
    (44, "老庄出海钓鱼，AI龙虾在工作，和平分工场景", "16:9"),
    (45, "第一位用户说有用，加菲猫龙虾感动流泪", "1:1"),
    (46, "凌晨3点加班：加菲猫龙虾陪老庄加班，咖啡+电脑", "16:9"),
    (47, "女儿给龙虾取名字，可爱温馨家庭场景", "1:1"),
    (48, "老庄和龙虾一起建网站，代码和创意齐飞", "16:9"),
    (49, "AI团队开会：7个AI成员汇报，加菲猫龙虾主持", "16:9"),
    (50, "周年纪念：老庄和龙虾一起切蛋糕，庆祝成长", "1:1"),
    # Batch 5: 创意艺术图 (51-70)
    (51, "未来城市：AI龙虾在城市中穿梭，科技与生活融合", "16:9"),
    (52, "海底世界：加菲猫龙虾骑鲸鱼，信息流如海水流动", "16:9"),
    (53, "太空站：加菲猫龙虾在太空舱控制地球，宇宙探索", "16:9"),
    (54, "森林王国：加菲猫龙虾与动物们开议会，自然友好", "16:9"),
    (55, "中国风：加菲猫龙虾穿汉服，拿灯笼，国潮风格", "1:1"),
    (56, "赛博朋克：加菲猫龙虾在霓虹灯城市，赛博风格", "16:9"),
    (57, "童话故事：加菲猫龙虾大战恶龙，英雄冒险", "16:9"),
    (58, "水墨画：中国风山水，加菲猫龙虾在画中游，水墨艺术", "16:9"),
    (59, "像素游戏：8-bit风格加菲猫龙虾，复古游戏感", "16:9"),
    (60, "浮世绘：日本传统艺术风格，加菲猫龙虾在富士山", "16:9"),
    # Batch 6: 情绪态度配图 (61-80)
    (61, "自信：加菲猫龙虾戴墨镜，帅气自信，都市风格", "1:1"),
    (62, "努力：加菲猫龙虾埋头苦干，汗水+坚持，励志", "1:1"),
    (63, "幽默：加菲猫龙虾在搞笑表演，单口喜剧场景", "16:9"),
    (64, "温暖：加菲猫龙虾拥抱老庄，友情岁月", "1:1"),
    (65, "好奇：加菲猫龙虾看星星，探索未知", "16:9"),
    (66, "傲娇：加菲猫龙虾斜眼，不屑但可爱", "1:1"),
    (67, "认真：加菲猫龙虾戴眼镜看显微镜，学术风", "1:1"),
    (68, "放松：加菲猫龙虾躺在沙滩椅，椰子树，海岛度假", "16:9"),
    (69, "兴奋：加菲猫龙虾跳起来，庆祝成功", "1:1"),
    (70, "沉思：加菲猫龙虾坐树下，禅意氛围", "1:1"),
    # Batch 7: 更多配图 (71-90)
    (71, "加菲猫龙虾在咖啡馆写周报，咖啡+笔记本，都市办公风", "16:9"),
    (72, "加菲猫龙虾在雨中打伞上班，职场通勤，幽默插画", "16:9"),
    (73, "加菲猫龙虾当医生问诊，白大褂，专业可靠", "1:1"),
    (74, "加菲猫龙虾当厨师做饭，围裙+锅铲，美食风格", "16:9"),
    (75, "加菲猫龙虾在健身房锻炼，哑铃+跑步机，健康生活", "16:9"),
    (76, "加菲猫龙虾在图书馆安静读书，眼镜片反光，学术氛围", "16:9"),
    (77, "加菲猫龙虾在演唱会现场挥舞荧光棒，音乐节氛围", "16:9"),
    (78, "加菲猫龙虾在超市购物车大笑，购物场景，喜剧风格", "16:9"),
    (79, "加菲猫龙虾在长城上打卡，旅行打卡地标", "16:9"),
    (80, "加菲猫龙虾在樱花季野餐，日本春天，温馨氛围", "16:9"),
    # Batch 8: 完成剩余 (81-100)
    (81, "加菲猫龙虾在圣诞树下拆礼物，节日氛围，温暖圣诞", "16:9"),
    (82, "加菲猫龙虾在万圣节扮鬼，南瓜灯，搞笑万圣节", "16:9"),
    (83, "加菲猫龙虾在春晚舞台表演，舞台聚光灯，中国新年", "16:9"),
    (84, "加菲猫龙虾在奥运会领奖台，金牌，冠军时刻", "1:1"),
    (85, "加菲猫龙虾在火星上种植土豆，太空农业，科幻", "16:9"),
    (86, "加菲猫龙虾在沙漠中骑骆驼，绿洲，冒险旅程", "16:9"),
    (87, "加菲猫龙虾在雪山上滑雪，冬季运动，极限运动", "16:9"),
    (88, "加菲猫龙虾在潜水海底看珊瑚礁，海洋世界，环保主题", "16:9"),
    (89, "加菲猫龙虾在热带雨林探险，野生动物，冒险故事", "16:9"),
    (90, "加菲猫龙虾在草原上赶羊，牧民生活，田园风格", "16:9"),
    # Batch 9: 最后30张 (91-120)
    (91, "加菲猫龙虾在星际飞船里睡觉，宇宙探索，梦幻星空", "16:9"),
    (92, "加菲猫龙虾在黑客松现场写代码，大屏幕倒计时，竞赛氛围", "16:9"),
    (93, "加菲猫龙虾在录播客节目麦克风前，知识分享，媒体风格", "16:9"),
    (94, "加菲猫龙虾在设计logo，创意工作，设计软件界面", "16:9"),
    (95, "加菲猫龙虾在做瑜伽冥想，健康生活，宁静氛围", "1:1"),
    (96, "加菲猫龙虾在教小猫写代码，导师角色，传承精神", "16:9"),
    (97, "加菲猫龙虾在参加马拉松跑步，体育精神，健康倡导", "16:9"),
    (98, "加菲猫龙虾在参加毕业典礼，学位帽，毕业快乐", "16:9"),
    (99, "加菲猫龙虾在婚礼上当伴郎，幸福时刻，友情岁月", "16:9"),
    (100, "加菲猫龙虾在生日派对上吹蜡烛，蛋糕+礼物，欢乐生日", "16:9"),
    (101, "加菲猫龙虾在露营帐篷外看夜空，篝火+星空，户外生活", "16:9"),
    (102, "加菲猫龙虾在修车厂修车，机械技能，多才多艺", "16:9"),
    (103, "加菲猫龙虾在花店插花，美好生活，花艺设计", "16:9"),
    (104, "加菲猫龙虾在建筑工地搬砖，建筑工人，辛勤劳动", "16:9"),
    (105, "加菲猫龙虾在银行存钱，金库场景，财富管理", "1:1"),
    (106, "加菲猫龙虾在法庭上当律师西装革履，法律职业，专业严肃", "16:9"),
    (107, "加菲猫龙虾在农场挤牛奶，田园生活，乡村风格", "16:9"),
    (108, "加菲猫龙虾在科学实验室做实验，科学家形象，实验器材", "16:9"),
    (109, "加菲猫龙虾在美术馆看画展，艺术鉴赏，文化气息", "16:9"),
    (110, "加菲猫龙虾在音乐节弹吉他，摇滚明星，音乐激情", "16:9"),
    (111, "加菲猫龙虾在游戏厅打游戏街机，复古游戏，童年回忆", "16:9"),
    (112, "加菲猫龙虾在游乐园坐过山车，欢乐刺激，主题公园", "16:9"),
    (113, "加菲猫龙虾在马戏团表演，小丑装扮，欢乐马戏", "16:9"),
    (114, "加菲猫龙虾在敬老院陪伴老人，关爱老人，温暖社会", "16:9"),
    (115, "加菲猫龙虾在医院照顾病人，医护角色，关怀之心", "16:9"),
    (116, "加菲猫龙虾在消防站灭火，勇敢消防员，紧急救援", "16:9"),
    (117, "加菲猫龙虾在警察局值班，警察制服，维护正义", "16:9"),
    (118, "加菲猫龙虾在教室上课当学生，背书包，认真听讲", "16:9"),
    (119, "加菲猫龙虾在食堂排队打饭，学生生活，校园场景", "16:9"),
    (120, "加菲猫龙虾毕业入职第一天背着书包进公司，新人入职，充满希望", "16:9"),
]


def generate_one(idx_num, prompt, aspect_ratio):
    """Generate a single image and return result"""
    output_path = os.path.join(OUTPUT_DIR, f"{idx_num:03d}.png")
    
    result = generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        output_path=output_path
    )
    
    return {
        "number": idx_num,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "output_path": output_path,
        "success": result.get("success", False),
        "image_url": result.get("image_url", ""),
        "error": result.get("error", ""),
    }


def run_batch(batch_items, batch_num):
    """Run a batch of 5 images in parallel"""
    print(f"\n{'='*60}")
    print(f"Batch {batch_num}: 生成第 {batch_items[0][0]}-{batch_items[-1][0]} 张")
    print(f"{'='*60}")
    
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(generate_one, idx, prompt, ratio): idx
            for idx, prompt, ratio in batch_items
        }
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                status = "✅" if result["success"] else "❌"
                print(f"  {status} #{result['number']}: {result['prompt'][:40]}...")
                if not result["success"]:
                    print(f"     Error: {result['error']}")
            except Exception as e:
                print(f"  ❌ Exception: {e}")
    
    return results


def write_record(all_results):
    """Write results to markdown record file"""
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        f.write("# 配色师-图片生成记录\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| 序号 | Prompt | 文件名 | 状态 | 链接 |\n")
        f.write("|------|--------|--------|------|------|\n")
        
        for r in all_results:
            status = "✅成功" if r["success"] else f"❌失败: {r['error']}"
            filename = os.path.basename(r["output_path"])
            link = r["image_url"] if r["success"] else ""
            prompt_short = r["prompt"][:60] + "..." if len(r["prompt"]) > 60 else r["prompt"]
            f.write(f"| {r['number']} | {prompt_short} | {filename} | {status} | {link} |\n")
        
        # Summary
        success_count = sum(1 for r in all_results if r["success"])
        total = len(all_results)
        rate = success_count / total * 100 if total > 0 else 0
        f.write(f"\n## 统计\n\n")
        f.write(f"- 共生成：{success_count}/{total} 张\n")
        f.write(f"- 成功率：{rate:.1f}%\n")


def main():
    print(f"开始生成120张图片...")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"批次大小: {BATCH_SIZE}")
    print(f"总图片数: {len(IMAGES)}")
    
    all_results = []
    total_batches = (len(IMAGES) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(IMAGES), BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        batch_items = IMAGES[i:i+BATCH_SIZE]
        
        print(f"\n>>> Batch {batch_num}/{total_batches} 开始...")
        results = run_batch(batch_items, batch_num)
        all_results.extend(results)
        
        # Write intermediate record after each batch
        write_record(all_results)
        print(f"    本批次完成，已记录到 {RECORD_FILE}")
        
        # Small delay between batches to be nice to API
        if batch_num < total_batches:
            time.sleep(2)
    
    # Final summary
    success_count = sum(1 for r in all_results if r["success"])
    total = len(all_results)
    rate = success_count / total * 100 if total > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"🎉 全部完成！")
    print(f"✅ 成功: {success_count}/{total}")
    print(f"📊 成功率: {rate:.1f}%")
    print(f"📁 记录文件: {RECORD_FILE}")
    print(f"{'='*60}")
    
    return all_results


if __name__ == "__main__":
    main()
