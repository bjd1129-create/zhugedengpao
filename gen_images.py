#!/usr/bin/env python3
import requests
import base64
import json
import os
import time

API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
API_URL = "https://api.minimaxi.com/v1/image_generation"
DIR = "/Users/bjd/Desktop/ZhugeDengpao-Team/images"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

prompts = [
    # 1-20: 穿龙虾衣服的加菲猫
    "A fat orange Garfield cat wearing a lobster-red hoodie with lobster pattern, sitting in a modern office, cartoon style, warm lighting, cozy atmosphere",
    "A fat orange Garfield cat wearing a cute lobster costume, lounging on a comfortable sofa at home, cartoon style, living room background",
    "A chubby Garfield cat in a lobster-print t-shirt, standing outdoors in a park, autumn leaves falling, cartoon style",
    "A cute Garfield cat wearing a red lobster onesie, traveling with a small backpack, famous landmark background, cartoon style",
    "A jolly Garfield cat dressed in lobster pajamas, reading a book in bed, nighttime bedroom scene, cartoon style",
    "A playful Garfield cat in lobster costume, playing with a ball of yarn, home interior, cartoon style, bright colors",
    "A fat happy Garfield cat wearing lobster-themed shirt, eating spaghetti in the kitchen, cartoon style, Italian restaurant vibe",
    "A Garfield cat with lobster hat and lobster shoes, riding a bicycle, suburban neighborhood, cartoon style",
    "A cheerful Garfield cat in lobster costume, celebrating birthday with cake, party decorations, cartoon style",
    "A sleepy Garfield cat wearing lobster-print pajamas, lying on a sunny lawn chair, backyard, summer day, cartoon style",
    "A cool Garfield cat with sunglasses wearing lobster t-shirt, hanging out at beach, palm trees, cartoon style",
    "A cute Garfield cat in lobster hoodie, sleeping on a fluffy cloud bed, dreamy bedroom, cartoon style",
    "A happy Garfield cat in lobster costume, playing video games on couch, game controller in paw, cartoon style",
    "A jolly Garfield cat in lobster-print sweater, drinking coffee at a cafe window, city street view, cartoon style",
    "A mischievous Garfield cat wearing lobster pajamas, climbing on kitchen counter, midnight snack scene, cartoon style",
    "A fat content Garfield cat in lobster onesie, relaxing in a hot tub, steam rising, cartoon style, evening",
    "A playful kitten-sized Garfield cat in lobster costume, chasing butterflies in a flower garden, cartoon style",
    "A relaxed Garfield cat wearing lobster shirt, sitting in a hammock between trees, tropical setting, cartoon style",
    "A happy Garfield cat in lobster costume, dancing at a costume party, colorful lights, cartoon style",
    "A sleepy-eyed Garfield cat wearing lobster pajamas, lying on a pile of pillows, cartoon style, soft lighting",
    # 21-40: AI龙虾团队工作场景
    "A team of robot lobsters working together at a high-tech laboratory, holographic computers, sci-fi environment, digital art",
    "AI lobster robots in a creative brainstorming session, white board with diagrams, modern office, digital art style",
    "A group of cute robot lobsters debugging code together, multiple screens with code, night scene, cyberpunk digital art",
    "Robot lobsters presenting their machine learning model, holographic charts and graphs, conference room, sci-fi art",
    "Robot lobsters collaborating on 3D design project, floating holographic blueprints, futuristic workspace, digital art",
    "A team of AI lobster robots training neural networks, server room with glowing lights, digital art, cyber aesthetic",
    "Robot lobster developers pair programming, two lobsters at one monitor, cozy tech office, digital art style",
    "AI lobster team having a stand-up meeting, kanban board behind them, agile methodology, digital art",
    "Robot lobsters building an AI model, various components floating around them, construction site of the future, digital art",
    "A team of lobster robots celebrating successful product launch, confetti, champagne, office party scene, digital art",
    "AI lobster developers reviewing code on large curved monitors, late night coding session, dim lighting, digital art",
    "Robot lobsters conducting AI ethics discussion, philosophical symbols floating, council chamber setting, digital art",
    "Lobster AI robots deploying new software, rocket launching in background, DevOps concept, digital art",
    "Team of cute robot lobsters doing data analysis, huge data visualizations, analytics dashboard, digital art style",
    "AI lobster team in a war room planning next project, strategic maps and timelines, dramatic lighting, digital art",
    "Robot lobsters testing autonomous vehicles, tiny lobster drivers in miniature cars, test track, digital art",
    "Lobster AI researchers discovering new algorithm, lightbulb moment, equations on blackboard, digital art",
    "Team of robot lobsters maintaining quantum computer, cryogenic chamber, glowing blue elements, digital art",
    "AI lobster developers writing prompt engineering documentation, peaceful library setting, digital art style",
    "Robot lobster team doing VR collaboration, virtual workspace floating in space, metaverse concept, digital art",
    # 41-60: 科技感AI主题图片
    "Abstract neural network visualization, glowing nodes and connections, deep blue and purple, futuristic digital art",
    "AI consciousness emerging from digital data streams, humanoid silhouette made of code, cyber aesthetic",
    "Futuristic AI brain with circuits and light rays, holographic display, technology concept art",
    "Robot and human shaking hands, symbolic representation of AI-human collaboration, clean modern style",
    "Massive server farm with AI core glowing in center, data streams flowing, digital landscape, sci-fi art",
    "AI generated art canvas showing infinite creativity, paint becoming reality, surreal digital art",
    "Self-driving car AI visualization, city streets mapped with sensor data, lidar points in neon colors",
    "AI assistant hologram emerging from smartphone, floating interface elements, smart home concept",
    "Machine learning training process visualization, data flowing into model, beautiful geometric patterns",
    "AI robot contemplating existence, alone in digital void, philosophical robot art, moody lighting",
    "Quantum computing AI processor, qubits in superposition states, crystalline structures, digital art",
    "Generative AI creating multiple realities, branching universes from one seed, fractal dimension art",
    "AI ecosystem with interconnected intelligent agents, swarm intelligence visualization, node network art",
    "Neural network becoming sentient, eye opening with circuit patterns, awakening AI concept art",
    "AI-powered smart city at night, countless sensors and data points, glowing infrastructure, aerial view",
    "Deep learning black box with mysterious interior, light leaking out, data transformation art",
    "AI character recognition system, digital brain scanning images, face detection visualization",
    "Transformer architecture as living organism, attention heads like neurons firing, biological tech fusion art",
    "Artificial general intelligence ascending, robot reaching toward digital heaven, transcendent AI art",
    "Cybernetic brain with organic elements, bio-digital fusion, future of humanity with AI, concept art",
    # 61-80: 老庄的故事场景
    "Ancient Chinese philosopher Zhuangzi by a peaceful river, bamboo forest background, traditional ink wash painting style",
    "Zhuangzi dreaming of being a butterfly, dreamy cloud scene, Daoist philosophy illustration, Chinese art style",
    "Old Zhuangzi teaching young disciples in mountain pavilion, misty mountains, traditional Chinese painting",
    "Zhuangzi fasting and meditating in nature, sitting on rock by waterfall, serene landscape, Chinese ink painting",
    "The story of Zhuangzi and the owl, mysterious nighttime scene, owl perched, traditional style illustration",
    "Zhuangzi discarding worldly honors, burning scrolls, dilemma of fame, Chinese historical art",
    "Old Zhuangzi walking with bamboo staff, autumn mountain path, wandering philosopher, Chinese landscape painting",
    "Zhuangzi and Huizi debating at bridge, fish and water below, philosophical argument scene, classical Chinese art",
    "Old Zhuangzi reading alone by candlelight, simple wooden cottage, night scene, traditional Chinese art",
    "Zhuangzi observing fish at Hao river, two fish swimming, peaceful water, famous parable scene, Chinese painting",
    "The butcher Ding cutting an ox, masterful technique, ox and chef in abattoir, classical Chinese illustration",
    "Zhuangzi among free and easy souls, cloud beings and transcendents, celestial scene, Chinese mythology art",
    "Old Zhuangzi traveling to kingdom of Chu, dusty road, royal messenger approaching, historical scene art",
    "Zhuangzi wearing simple clothes but acting freely, carefree sage, mountain meadow, Chinese art style",
    "The giant peng bird mythical creature, Zhuangzi looking up in wonder, enormous bird in clouds, Chinese mythological art",
    "Zhuangzi conversing with skull, sitting at crossroads, philosophical conversation, dark but humorous scene",
    "Old Zhuangzi in simple boat fishing, misty river morning, solitary happiness, serene Chinese landscape",
    "Zhuangzi's butterfly dream awakening, half butterfly half man, between dreams and reality, surreal Chinese art",
    # 81-100: 小花的日常
    "Cute anime girl named Xiao Hua eating breakfast, sunny kitchen, cereal and fruit, kawaii style illustration",
    "Xiao Hua studying at desk, textbooks and laptop, cozy bedroom, afternoon light, anime art style",
    "Little flower girl walking dog in park, golden retriever puppy, spring cherry blossoms, anime style",
    "Xiao Hua making coffee at cafe, barista apron, latte art, cozy coffee shop interior, anime illustration",
    "Girl Xiao Hua dancing alone in her room, music notes floating, carefree moment, anime style",
    "Xiao Hua reading book on grassy hill, picnic blanket, fluffy clouds, peaceful countryside, anime art",
    "Cute girl watering flowers in garden, morning sun, butterflies around, colorful flower beds, anime illustration",
    "Xiao Hua riding bicycle to school, schoolbag bouncing, residential street, bright morning, anime style",
    "Girl making dumplings in kitchen, flour on face, happy expression, traditional food prep, anime art",
    "Xiao Hua watching sunset on rooftop, city skyline behind, orange sky, contemplative moment, anime style",
    "Cute Xiao Hua celebrating birthday alone, small cake with candle, party hat, cozy room, anime illustration",
    "Girl eating ice cream on summer day, multiple flavors, heat waves, street vendor, anime style",
    "Xiao Hua doing yoga on beach, peaceful ocean view, sunrise meditation, wellness scene, anime art",
    "Girl writing diary by window, rainy day outside, warm lamp light, introspective moment, anime illustration",
    "Cute Xiao Hua playing with cat, fluffy white cat, lying on floor together, playful scene, anime style",
    "Xiao Hua at night market, food stalls with lights, crowds, street food adventure, anime art",
    "Girl making origami cranes, colorful paper, paper birds on table, peaceful craft time, anime illustration",
    "Xiao Hua studying at library, piles of books, reading nook, cozy academic atmosphere, anime style",
    "Cute girl baking cookies in kitchen, mixing bowl, oven, flour everywhere, cheerful chaos, anime art",
    "Xiao Hua stargazing on countryside field, shooting stars, telescope, vast night sky, peaceful anime scene",
    # 101-120: 抽象概念图
    "Time as a flowing river of light, abstract representation of past present future, glowing currents, conceptual art",
    "The concept of memory as interconnected rooms, doors opening to different times, surreal architecture art",
    "Human consciousness as expanding universe, mind becoming cosmos, stars within brain shape, conceptual art",
    "Love as fusion energy, two particles merging into radiant sun, abstract scientific romantic art",
    "Silence visualized as geometric space, empty cubes in perfect formation, minimalist abstract art",
    "The evolution of intelligence, simple cells to complex neural networks, timeline spiral, abstract science art",
    "Creativity as explosion of color, paint bombs in mid-burst, abstract expressionism style",
    "Dreams as doorway between dimensions, portal with swirling nebula, surreal conceptual art",
    "The self as mirror reflection shattering, multiple fragments floating, identity crisis concept art",
    "Wisdom as ancient tree with circuit board leaves, technology meets nature, cyborg nature art",
    "Hope as small flame in vast darkness, single candle against black void, emotional abstract art",
    "Knowledge as library without end, infinite shelves stretching to horizon, Borges-inspired abstract art",
    "Freedom as bird made of wind and light, escaping cage of clouds, liberation concept art",
    "The nature of reality, iceberg with more hidden beneath water, perception vs truth, conceptual art",
    "Joy as bubbles floating upward, rainbow reflections in each bubble, celebratory abstract",
    "Loneliness as single figure on empty planet, earth moon above, cosmic solitude concept art",
    "Transformation as chrysalis cracking open, human emerging as light being, metamorphosis abstract art",
    "Balance as scales made of natural elements, earth fire water air, zen concept art",
    "The meaning of life question mark dissolving into stars, philosophy visualization, abstract conceptual art",
    "Infinite possibilities branching like tree of futures, multiverse concept, quantum reality art",
]

def generate_image(idx, prompt):
    filename = f"{idx:03d}.jpg"
    filepath = os.path.join(DIR, filename)
    
    if os.path.exists(filepath):
        print(f"跳过 {idx}: {filename} 已存在")
        return True
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "response_format": "base64"
    }
    
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            data = resp.json()
            
            # Try different response formats
            b64 = None
            if "data" in data:
                d = data["data"]
                if isinstance(d, list):
                    b64 = d[0].get("image_base64") or d[0].get("base64") if d else None
                elif isinstance(d, str):
                    b64 = d
                elif isinstance(d, dict):
                    b64 = d.get("image_base64") or d.get("base64")
            elif "images" in data:
                b64 = data["images"][0].get("image_base64") or data["images"][0].get("base64") if data["images"] else None
            elif "image_base64" in data:
                b64 = data["image_base64"][0] if isinstance(data["image_base64"], list) else data["image_base64"]
            elif "base64" in data:
                b64 = data["base64"]
            
            if b64:
                img_data = base64.b64decode(b64)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"✓ {idx}: {filename}")
                return True
            else:
                print(f"✗ {idx}: 未知格式 - {str(data)[:100]}")
                return False
                
        except Exception as e:
            print(f"✗ {idx} (尝试 {attempt+1}): {e}")
            time.sleep(2)
    
    return False

success = 0
failed = []
for i, prompt in enumerate(prompts, 1):
    if generate_image(i, prompt):
        success += 1
    else:
        failed.append(i)
    time.sleep(0.3)

print(f"\n===== 完成 =====")
print(f"成功: {success}/120")
if failed:
    print(f"失败: {failed}")
