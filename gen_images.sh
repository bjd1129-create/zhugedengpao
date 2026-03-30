#!/bin/bash

API_KEY="sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
API_URL="https://api.minimaxi.com/v1/image_generation"
DIR="/Users/bjd/Desktop/ZhugeDengpao-Team/images"

generate_image() {
  local idx=$1
  local prompt=$2
  local filename=$(printf "%03d" $idx)".jpg"
  
  echo "生成第 $idx 张图片..."
  
  response=$(curl -s -X POST "$API_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg prompt "$prompt" '{"model":"image-01","prompt":$prompt,"aspect_ratio":"16:9","response_format":"base64"}')")
  
  base64_data=$(echo "$response" | jq -r '.data // .images[0] // empty')
  
  if [ -n "$base64_data" ] && [ "$base64_data" != "null" ]; then
    echo "$base64_data" | base64 -d > "$DIR/$filename"
    echo "✓ 第 $idx 张已保存: $filename"
  else
    echo "✗ 第 $idx 张失败: $response" >> "$DIR/errors.log"
    echo "✗ 第 $idx 张失败"
  fi
  
  sleep 0.5
}

# 1-20: 穿龙虾衣服的加菲猫
generate_image 1 "A fat orange Garfield cat wearing a lobster-red hoodie with lobster pattern, sitting in a modern office, cartoon style, warm lighting, cozy atmosphere"
generate_image 2 "A fat orange Garfield cat wearing a cute lobster costume, lounging on a comfortable sofa at home, cartoon style, living room background"
generate_image 3 "A chubby Garfield cat in a lobster-print t-shirt, standing outdoors in a park, autumn leaves falling, cartoon style"
generate_image 4 "A cute Garfield cat wearing a red lobster onesie, traveling with a small backpack, famous landmark background, cartoon style"
generate_image 5 "A jolly Garfield cat dressed in lobster pajamas, reading a book in bed, nighttime bedroom scene, cartoon style"
generate_image 6 "A playful Garfield cat in lobster costume, playing with a ball of yarn, home interior, cartoon style, bright colors"
generate_image 7 "A fat happy Garfield cat wearing lobster-themed shirt, eating spaghetti in the kitchen, cartoon style, Italian restaurant vibe"
generate_image 8 "A Garfield cat with lobster hat and lobster shoes, riding a bicycle, suburban neighborhood, cartoon style"
generate_image 9 "A cheerful Garfield cat in lobster costume, celebrating birthday with cake, party decorations, cartoon style"
generate_image 10 "A sleepy Garfield cat wearing lobster-print pajamas, lying on a sunny lawn chair, backyard, summer day, cartoon style"
generate_image 11 "A cool Garfield cat with sunglasses wearing lobster t-shirt, hanging out at beach, palm trees, cartoon style"
generate_image 12 "A cute Garfield cat in lobster hoodie, sleeping on a fluffy cloud bed, dreamy bedroom, cartoon style"
generate_image 13 "A happy Garfield cat wearing lobster costume, playing video games on couch, game controller in paw, cartoon style"
generate_image 14 "A jolly Garfield cat in lobster-print sweater, drinking coffee at a cafe window, city street view, cartoon style"
generate_image 15 "A mischievous Garfield cat wearing lobster pajamas, climbing on kitchen counter, midnight snack scene, cartoon style"
generate_image 16 "A fat content Garfield cat in lobster onesie, relaxing in a hot tub, steam rising, cartoon style, evening"
generate_image 17 "A playful kitten-sized Garfield cat in lobster costume, chasing butterflies in a flower garden, cartoon style"
generate_image 18 "A relaxed Garfield cat wearing lobster shirt, sitting in a hammock between trees, tropical setting, cartoon style"
generate_image 19 "A happy Garfield cat in lobster costume, dancing at a costume party, colorful lights, cartoon style"
generate_image 20 "A sleepy-eyed Garfield cat wearing lobster pajamas, lying on a pile of pillows, cartoon style, soft lighting"

# 21-40: AI龙虾团队工作场景
generate_image 21 "A team of robot lobsters working together at a high-tech laboratory, holographic computers, sci-fi environment, digital art"
generate_image 22 "AI lobster robots in a creative brainstorming session, white board with diagrams, modern office, digital art style"
generate_image 23 "A group of cute robot lobsters debugging code together, multiple screens with code, night scene, cyberpunk digital art"
generate_image 24 "AI lobster team presenting their machine learning model, holographic charts and graphs, conference room, sci-fi art"
generate_image 25 "Robot lobsters collaborating on 3D design project, floating holographic blueprints, futuristic workspace, digital art"
generate_image 26 "A team of AI lobster robots training neural networks, server room with glowing lights, digital art, cyber aesthetic"
generate_image 27 "Robot lobster developers pair programming, two lobsters at one monitor, cozy tech office, digital art style"
generate_image 28 "AI lobster team having a stand-up meeting, kanban board behind them, agile methodology, digital art"
generate_image 29 "Robot lobsters building an AI model, various components floating around them, construction site of the future, digital art"
generate_image 30 "A team of lobster robots celebrating successful product launch, confetti, champagne, office party scene, digital art"
generate_image 31 "AI lobster developers reviewing code on large curved monitors, late night coding session, dim lighting, digital art"
generate_image 32 "Robot lobsters conducting AI ethics discussion, philosophical symbols floating, council chamber setting, digital art"
generate_image 33 "Lobster AI robots deploying new software, rocket launching in background, DevOps concept, digital art"
generate_image 34 "Team of cute robot lobsters doing data analysis, huge data visualizations, analytics dashboard, digital art style"
generate_image 35 "AI lobster team in a war room planning next project, strategic maps and timelines, dramatic lighting, digital art"
generate_image 36 "Robot lobsters testing autonomous vehicles, tiny lobster drivers in miniature cars, test track, digital art"
generate_image 37 "Lobster AI researchers discovering new algorithm, lightbulb moment, equations on blackboard, digital art"
generate_image 38 "Team of robot lobsters maintaining quantum computer, cryogenic chamber, glowing blue elements, digital art"
generate_image 39 "AI lobster developers writing prompt engineering documentation, peaceful library setting, digital art style"
generate_image 40 "Robot lobster team doing VR collaboration, virtual workspace floating in space, metaverse concept, digital art"

# 41-60: 科技感AI主题图片
generate_image 41 "Abstract neural network visualization, glowing nodes and connections, deep blue and purple, futuristic digital art"
generate_image 42 "AI consciousness emerging from digital data streams, humanoid silhouette made of code, cyber aesthetic"
generate_image 43 "Futuristic AI brain with circuits and light rays, holographic display, technology concept art"
generate_image 44 "Robot and human shaking hands, symbolic representation of AI-human collaboration, clean modern style"
generate_image 45 "Massive server farm with AI core glowing in center, data streams flowing, digital landscape, sci-fi art"
generate_image 46 "AI generated art canvas showing infinite creativity, paint becoming reality, surreal digital art"
generate_image 47 "Self-driving car AI visualization, city streets mapped with sensor data, lidar points in neon colors"
generate_image 48 "AI assistant hologram emerging from smartphone, floating interface elements, smart home concept"
generate_image 49 "Machine learning training process visualization, data flowing into model, beautiful geometric patterns"
generate_image 50 "AI robot contemplating existence, alone in digital void, philosophical robot art, moody lighting"
generate_image 51 "Quantum computing AI processor, qubits in superposition states, crystalline structures, digital art"
generate_image 52 "Generative AI creating multiple realities, branching universes from one seed, fractal dimension art"
generate_image 53 "AI ecosystem with interconnected intelligent agents, swarm intelligence visualization, node network art"
generate_image 54 "Neural network becoming sentient, eye opening with circuit patterns, awakening AI concept art"
generate_image 55 "AI-powered smart city at night, countless sensors and data points, glowing infrastructure, aerial view"
generate_image 56 "Deep learning black box with mysterious interior, light leaking out, data transformation art"
generate_image 57 "AI character recognition system, digital brain scanning images, face detection visualization"
generate_image 58 "Transformer architecture as living organism, attention heads like neurons firing, biological tech fusion art"
generate_image 59 "Artificial general intelligence ascending, robot reaching toward digital heaven, transcendent AI art"
generate_image 60 "Cybernetic brain with organic elements, bio-digital fusion, future of humanity with AI, concept art"

# 61-80: 老庄的故事场景
generate_image 61 "Ancient Chinese philosopher Zhuangzi by a peaceful river, bamboo forest background, traditional ink wash painting style"
generate_image 62 "Zhuangzi dreaming of being a butterfly, dreamy cloud scene, Daoist philosophy illustration, Chinese art style"
generate_image 63 "Old Zhuangzi teaching young disciples in mountain pavilion, misty mountains, traditional Chinese painting"
generate_image 64 "Zhuangzi fasting and meditating in nature, sitting on rock by waterfall, serene landscape, Chinese ink painting"
generate_image 65 "The story of Zhuangzi and the owl, mysterious nighttime scene, owl perched, traditional style illustration"
generate_image 66 "Zhuangzi discarding worldly honors, burning scrolls, dilemma of fame, Chinese historical art"
generate_image 67 "Old Zhuangzi walking with bamboo staff, autumn mountain path, wandering philosopher, Chinese landscape painting"
generate_image 68 "Zhuangzi's wife dies, he drums and sings instead of mourning, controversial scene, traditional Chinese art"
generate_image 69 "The useless great tree parable, massive ancient tree in field, Zhuangzi resting under it, Chinese ink style"
generate_image 70 "Zhuangzi and Huizi debating at bridge, fish and water below, philosophical argument scene, classical Chinese art"
generate_image 71 "Old Zhuangzi reading alone by candlelight, simple wooden cottage, night scene, traditional Chinese art"
generate_image 72 "Zhuangzi observing fish at Hao river, two fish swimming, peaceful water, famous parable scene, Chinese painting"
generate_image 73 "The butcher Ding cutting an ox, masterful technique, ox and chef in abattoir, classical Chinese illustration"
generate_image 74 "Zhuangzi among free and easy souls, cloud beings and transcendents, celestial scene, Chinese mythology art"
generate_image 75 "Old Zhuangzi traveling to kingdom of Chu, dusty road, royal messenger approaching, historical scene art"
generate_image 76 "Zhuangzi wearing破烂 clothes but acting freely, carefree sage, mountain meadow, Chinese art style"
generate_image 77 "The giant peng bird mythical creature, Zhuangzi looking up in wonder, enormous bird in clouds, Chinese mythological art"
generate_image 78 "Zhuangzi conversing with skull, sitting at crossroads, philosophical conversation, dark but humorous scene"
generate_image 79 "Old Zhuangzi in simple boat fishing, misty river morning, solitary happiness, serene Chinese landscape"
generate_image 80 "Zhuangzi's butterfly dream awakening, half butterfly half man, between dreams and reality, surreal Chinese art"

# 81-100: 小花的日常
generate_image 81 "Cute anime girl named Xiao Hua eating breakfast, sunny kitchen, cereal and fruit, kawaii style illustration"
generate_image 82 "Xiao Hua studying at desk, textbooks and laptop, cozy bedroom, afternoon light, anime art style"
generate_image 83 "Little flower girl walking dog in park, golden retriever puppy, spring cherry blossoms, anime style"
generate_image 84 "Xiao Hua making coffee at cafe, barista apron, latte art, cozy coffee shop interior, anime illustration"
generate_image 85 "Girl Xiao Hua dancing alone in her room, music notes floating, carefree moment, anime style"
generate_image 86 "Xiao Hua reading book on grassy hill, picnic blanket, fluffy clouds, peaceful countryside, anime art"
generate_image 87 "Cute girl watering flowers in garden, morning sun, butterflies around, colorful flower beds, anime illustration"
generate_image 88 "Xiao Hua riding bicycle to school, schoolbag bouncing, residential street, bright morning, anime style"
generate_image 89 "Girl making dumplings in kitchen, flour on face, happy expression, traditional food prep, anime art"
generate_image 90 "Xiao Hua watching sunset on rooftop, city skyline behind, orange sky, contemplative moment, anime style"
generate_image 91 "Cute Xiao Hua celebrating birthday alone, small cake with candle, party hat, cozy room, anime illustration"
generate_image 92 "Girl eating ice cream on summer day, multiple flavors, heat waves, street vendor, anime style"
generate_image 93 "Xiao Hua doing yoga on beach, peaceful ocean view, sunrise meditation, wellness scene, anime art"
generate_image 94 "Girl writing diary by window, rainy day outside, warm lamp light, introspective moment, anime illustration"
generate_image 95 "Cute Xiao Hua playing with cat, fluffy white cat, lying on floor together, playful scene, anime style"
generate_image 96 "Xiao Hua at night market, food stalls with lights, crowds, street food adventure, anime art"
generate_image 97 "Girl making origami cranes, colorful paper, paper birds on table, peaceful craft time, anime illustration"
generate_image 98 "Xiao Hua studying at library, piles of books, reading nook, cozy academic atmosphere, anime style"
generate_image 99 "Cute girl baking cookies in kitchen, mixing bowl, oven, flour everywhere, cheerful chaos, anime art"
generate_image 100 "Xiao Hua stargazing on countryside field, shooting stars, telescope, vast night sky, peaceful anime scene"

# 101-120: 抽象概念图
generate_image 101 "Time as a flowing river of light, abstract representation of past present future, glowing currents, conceptual art"
generate_image 102 "The concept of memory as interconnected rooms, doors opening to different times, surreal architecture art"
generate_image 103 "Human consciousness as expanding universe, mind becoming cosmos, stars within brain shape, conceptual art"
generate_image 104 "Love as fusion energy, two particles merging into radiant sun, abstract scientific romantic art"
generate_image 105 "Silence visualized as geometric space, empty cubes in perfect formation, minimalist abstract art"
generate_image 106 "The evolution of intelligence, simple cells to complex neural networks, timeline spiral, abstract science art"
generate_image 107 "Creativity as explosion of color, paint bombs in mid-burst, abstract expressionism style"
generate_image 108 "Dreams as doorway between dimensions, portal with swirling nebula, surreal conceptual art"
generate_image 109 "The self as mirror reflection shattering, multiple fragments floating, identity crisis concept art"
generate_image 110 "Wisdom as ancient tree with circuit board leaves, technology meets nature, cyborg nature art"
generate_image 111 "Hope as small flame in vast darkness, single candle against black void, emotional abstract art"
generate_image 112 "Knowledge as library without end, infinite shelves stretching to horizon, Borges-inspired abstract art"
generate_image 113 "Freedom as bird made of wind and light, escaping cage of clouds, liberation concept art"
generate_image 114 "The nature of reality, iceberg with more hidden beneath water, perception vs truth, conceptual art"
generate_image 115 "Joy as bubbles floating upward, rainbow reflections in each bubble, celebratory abstract"
generate_image 116 "Loneliness as single figure on empty planet, earth moon above, cosmic solitude concept art"
generate_image 117 "Transformation as chrysalis cracking open, human emerging as light being, metamorphosis abstract art"
generate_image 118 "Balance as scales made of natural elements, earth fire water air, zen concept art"
generate_image 119 "The meaning of life question mark dissolving into stars, philosophy visualization, abstract conceptual art"
generate_image 120 "Infinite possibilities branching like tree of futures, multiverse concept, quantum reality art"

echo "所有120张图片生成完成！"
