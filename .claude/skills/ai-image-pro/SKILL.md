---
name: ai-image-pro
description: Generate beautiful AI images from simple Thai or English prompts using the Prompt Autopilot framework. Runs GPT Image 2 via Kie AI with an automatic Google Gemini fallback, and ships 16 ready-to-use scene presets (UGC, cinematic, product-luxury, etc.) plus the AVB-6 prompt ladder, so even "สร้างรูปภูเขาไฟฟูจิ" produces a polished image.
---

# AI-Image Pro

วางคำสั่งง่าย ๆ แล้วรับภาพสวยกลับมา สกิลนี้ใช้ **Prompt Autopilot** คิด prompt ให้คุณเองโดยอัตโนมัติ ผ่านสูตร AVB-6 และ 16 ฉากภาพสำเร็จ

## Outcome

ไฟล์ภาพในโฟลเดอร์ dated ภายใต้ `generations/` พร้อม `prompt.md` (มนุษย์อ่าน), `.json` sidecar (เครื่องอ่าน) และสำเนาใน `~/Downloads/`

## สิ่งที่ได้

- **Prompt Autopilot** ระบบคิด prompt ให้อัตโนมัติ คุณไม่ต้องเขียนเอง
- **16 ฉากภาพ** ใช้ได้ทันที: UGC, cinematic, hyperreal portrait, macro close-up, product-luxury, product-shoot, anime, comic storyboard, editorial magazine, editorial illustration, editorial collage, social design, isometric, notebook sketch, technical annotation, text typography
- **AVB-6 Framework** สูตร 6 ขั้นทำภาพสวย: Subject, Setting, Vantage, Lighting, Mood, Style
- **ระบบซ่อมภาพ** เมื่อภาพออกมาพลาสติก/ปลอม แมปจุดผิดแล้วแก้เฉพาะจุดนั้น ไม่ต้องเริ่มใหม่

## การติดตั้ง (ครั้งเดียว)

วางโฟลเดอร์ `AI-Image-Pro` ทั้งโฟลเดอร์ไว้ที่ `.claude/skills/ai-image-pro/` ในโปรเจกต์ที่ต้องการใช้ แล้วเปิด Claude Code ใหม่ ที่เหลือสกิลจัดการเองใน Step 0

## API key เก็บที่ไหน

**ที่ root ของโปรเจกต์ ในไฟล์ `.env`** ที่เดียว ไม่ใช่ในโฟลเดอร์สกิล

สคริปต์หา project root โดยไต่ขึ้นไปมองหา `.claude/` หรือ `.git/` ไม่ใช่นับชั้น ดังนั้นรันจากโฟลเดอร์ย่อยชั้นไหนของโปรเจกต์ก็เจอไฟล์เดียวกัน ตัวแปรที่ export ไว้ใน shell ชนะไฟล์เสมอ

`doctor --init-env` จะสร้าง `.env` ที่ project root ให้ พร้อม**เติมบรรทัด `.env` ลง `.gitignore` ให้อัตโนมัติ** ไม่ทับของเดิม รันซ้ำไม่เพิ่มบรรทัดซ้ำ

เหตุผลที่ห้ามไว้ในโฟลเดอร์สกิล: โฟลเดอร์สกิลเป็นของที่คนคัดลอกไปมา zip ส่งให้เพื่อน แชร์ต่อ ถ้า key อยู่ข้างในมันจะหลุดไปด้วยทุกครั้งโดยไม่มีใครรู้ตัว ส่วน project root ไม่ได้ถูกส่งไปด้วยตอนแชร์สกิล และมี `.gitignore` คุมอีกชั้น

โฟลเดอร์สกิลไม่ถูกเขียนตอนรันเลยสักไฟล์ ภาพที่เจนออกมาไปลงที่ `generations/` ในโปรเจกต์ที่กำลังทำงานอยู่

**ถ้าเจอ `.env` อยู่ในโฟลเดอร์สกิล** (จากเวอร์ชันเก่า) สคริปต์จะยังอ่านให้ แต่จะเตือนทุกครั้งที่รัน ให้ Claude ย้ายไฟล์ไป project root แล้วลบตัวเดิมทิ้ง และบอกผู้ใช้ว่าถ้าเคยส่งโฟลเดอร์นี้ให้ใครไปแล้ว ควรไปเพิกถอน key เดิมแล้วออกใหม่

## Context Needs

| File | Load level | Purpose |
|---|---|---|
| `references/prompt-framework.md` | **Required** ก่อนเขียน prompt เสมอ | AVB-6 สูตรหลัก |
| `references/styles.md` | ตอนเลือกฉาก | ดัชนี 16 ฉากและ Auto-Selection Triggers |
| `references/style-*.md` | ตอนใช้ฉากนั้น ๆ | รายละเอียดแต่ละฉาก |
| `references/modifiers.md` | ตอนปรับแต่ง prompt | คลังคำศัพท์เรียงตาม 6 องค์ประกอบ |
| `references/camera-movements.md`, `lighting-sources.md` | ตอนเติม Vantage หรือ Lighting | คำศัพท์มุมกล้องและแสง |
| `references/model-selection.md` | ตอนเลือกหรือสลับเส้นทาง | เลือก provider และ model |
| `references/troubleshooting.md`, `de-plasticize-checklist.md` | ตอนผลลัพธ์ออกมาผิด | แมปอาการสู่องค์ประกอบที่ผิด |
| `references/prompt-patterns-gemini.md`, `prompt-patterns-kie.md` | ตอนปรับคำพูดต่อโมเดล | เทคนิคเฉพาะของแต่ละโมเดล |
| `references/character-consistency.md` | ตอนต้องตัวละครเดียวกันในหลายช็อต | workflow ภาพอ้างอิง |
| `references/json-formatting.md` | เฉพาะตอนเขียน prompt แบบ JSON | schema structured prompt |

## Dependencies

| Service | Required? | Provides | Without it |
|---|---|---|---|
| `KIE_API_KEY` | เส้นทางหลัก | GPT Image 2 (`gpt-image-2`) ผ่าน Kie AI และ base64 upload สำหรับภาพอ้างอิง | ภาพจะตกไปเส้นทางสำรอง Gemini อัตโนมัติ |
| `GEMINI_API_KEY` | เส้นทางสำรอง | Gemini 3 Pro Image ทางตรงจาก Google AI Studio (ฟรี ถูกกว่า) | ถ้า Kie ล้มเหลวและไม่มี Gemini ภาพจะรันไม่ได้ |
| `uv` | ใช่ | รันสคริปต์และ dependencies | สคริปต์รันไม่ได้ |

key ทั้งสองตัวอยู่ในไฟล์เดียวกันที่ `<project root>/.env` ไม่ใช่ในโฟลเดอร์สกิล

มี key ตัวใดตัวหนึ่งก็เจนภาพได้ เพราะสองเส้นทางสลับกันเองอัตโนมัติทั้งสองทิศทาง แต่มีครบสองตัวจะปลอดภัยที่สุด

## Step 0: Auto-check (รันเงียบ ๆ เอง ผู้ใช้ไม่ต้องรู้)

ก่อนเจนภาพครั้งแรกของ session ให้ Claude รันเช็คเองโดยอัตโนมัติ ผู้ใช้ไม่ต้องพิมพ์อะไรเพิ่ม และไม่ต้องเห็น output ถ้าทุกอย่างพร้อม

### ขั้น A: เช็ค `uv` ก่อน (ใช้คำสั่งที่ไม่ต้องพึ่ง uv เอง)

```bash
command -v uv          # macOS / Linux
```
```powershell
Get-Command uv -ErrorAction SilentlyContinue   # Windows
```

ถ้าคำสั่งคืนค่าว่าง แปลว่าผู้ใช้ยังไม่ได้ติดตั้ง `uv` ห้ามเรียก `uv run ...` สคริปต์ใช้แค่ Python standard library ดังนั้นถ้ามี `python3` (3.9 ขึ้นไป) ให้รัน `python3 <skill dir>/scripts/generate.py ...` แทนได้เลย ถ้าไม่มีทั้งคู่ ให้หยุดและบอกผู้ใช้ว่า:

> ต้องติดตั้ง uv ก่อนครั้งแรก ติดตั้งจาก https://docs.astral.sh/uv/
> Windows: เปิด PowerShell แล้วรัน
> `irm https://astral.sh/uv/install.ps1 | iex`

ห้ามเดาว่าผู้ใช้รู้จัก uv หรือ Python มาก่อน อธิบายแบบคนทั่วไป

### ขั้น B: รัน `doctor` เงียบ ๆ

```bash
uv run <skill dir>/scripts/generate.py doctor
```

รันจาก project root (หรือโฟลเดอร์ย่อยใดก็ได้ในโปรเจกต์) และอ้างสคริปต์ด้วย path ของโฟลเดอร์สกิล เช่น `.claude/skills/ai-image-pro/scripts/generate.py`

อ่าน output ภายใน Claude เท่านั้น ห้ามแสดงให้ผู้ใช้เห็น

### ขั้น C: กระทำตามผล

- **ถ้า `image` available และ `skill_folder_clean` กับ `env_gitignored` เป็น OK** → ไป Step 1 ได้เลย ไม่ต้องพูดอะไรกับผู้ใช้ (มี key ตัวเดียวก็พอ)
- **ถ้า `skill_folder_clean` ขึ้น LEAK** → หยุดก่อน นี่คือ key ที่วางผิดที่และกำลังเสี่ยงหลุด ย้ายไฟล์ไป `<project root>/.env` ลบตัวเดิมทิ้ง แล้วบอกผู้ใช้ว่าย้ายให้แล้วเพราะอะไร ถ้าเขาเคยส่งโฟลเดอร์สกิลให้ใครหรือ push ขึ้น git ไปแล้ว ให้แนะนำว่าควรออก key ใหม่
- **ถ้า `env_gitignored` ขึ้น missing from .gitignore** → รัน `doctor --init-env` เพื่อเติมให้ แล้วบอกผู้ใช้หนึ่งบรรทัดว่าเติม `.env` ลง `.gitignore` ให้แล้วเพราะ key อยู่ใน git repo
- **ถ้า `env_file` missing** → รัน `uv run <skill dir>/scripts/generate.py doctor --init-env` ให้ผู้ใช้เลย แล้วบอกว่า "สร้างไฟล์ `.env` ให้แล้วที่ project root ช่วยใส่ key ที่บรรทัดนี้"
- **ถ้า `image` เป็น BLOCKED** (ไม่มี key เลยสักตัว) → หยุด ห้ามเจนภาพ แล้วบอกผู้ใช้ด้วยภาษาง่าย ๆ:
  - "ขาด KIE_API_KEY (เส้นทางหลัก GPT Image 2) สมัครที่ https://kie.ai แล้วเอา key มาใส่ใน `.env`"
  - "ขาด GEMINI_API_KEY (เส้นทางสำรอง ฟรี) สมัครที่ https://aistudio.google.com/apikey แล้วเอา key มาใส่ใน `.env`"
- **ถ้ามี key แค่ตัวเดียว** → เจนภาพได้เลย ไม่ต้องหยุด แต่บอกครั้งเดียวว่ายังไม่มีเส้นทางสำรอง แล้วปล่อยผ่าน ห้ามทวงซ้ำ

### กฎสำคัญ

- ห้ามขอให้ผู้ใช้ paste key ลงในแชต
- ห้ามแสดง output `doctor` ทั้งหมดให้ผู้ใช้เห็น มันเยอะและดูน่ากลัว
- หลังจากผู้ใช้เติม key แล้ว ให้รัน `doctor` อีกครั้งเพื่อยืนยัน ถ้าผ่านค่อยเจนภาพ
- การเช็คนี้ทำครั้งเดียวต่อ session ครั้งต่อ ๆ ไปไม่ต้องเช็คซ้ำ

## Step 1: Read intent

ถอด subject และ action จากคำพูดผู้ใช้ สังเกตคำใบ้ของฉาก แล้วตั้งชื่อ working title เป็น kebab-case 3 ถึง 5 คำ (`dog-swimming-tennis-ball`) ห้ามถามชื่อ

## Step 2: Build the prompt with Prompt Autopilot

อ่าน `references/prompt-framework.md` แล้วปีน Prompt Ladder ทีละขั้น: Subject ก่อน แล้วตามด้วย Setting, Vantage, Lighting, Mood, Style

ตรวจสอบ `references/styles.md` ว่าฉากไหนเหมาะก็ดึงเข้ามาเลย ถ้าผู้ใช้พิมพ์คำที่ตรงกับ Auto-Selection Trigger ก็เลือกฉากนั้นให้อัตโนมัติโดยไม่ต้องถาม

แสดง prompt ที่ประกอบเสร็จแล้วถาม: **"Run this, or want to adjust?"** คำแก้ของผู้ใช้คือ source of truth ห้ามตีความเอง ถ้าเขาบอก "หมา" ห้ามตัดสินใจเองว่าเป็น golden retriever

## Step 3: Generate the image

```bash
uv run <skill dir>/scripts/generate.py image \
  --prompt "<AVB-6 prompt>" --title "<working-title>" \
  [--provider kie|gemini] [--model gpt-image-2|nano-banana-2-lite|nano-banana-pro] \
  [--aspect-ratio "16:9"] [--resolution 2K] [--input-image "<ref>"]...
```

ตัวเลือกเพิ่ม: `--dry-run` ดูเส้นทางที่จะใช้โดยไม่เรียก API, `--no-fallback` ห้ามสลับ provider, `--no-downloads` ไม่คัดลอกไป `~/Downloads`, `--out-dir` เปลี่ยนโฟลเดอร์ผลลัพธ์

ค่าเริ่มต้นใช้ `gpt-image-2` ผ่าน Kie และจะสลับไป Gemini อัตโนมัติถ้าล้มเหลว (สลับกลับได้ทั้งสองทิศทาง) **เวลาสลับเส้นทาง ต้องบอกผู้ใช้ว่าจริง ๆ แล้วรันผ่านเส้นทางไหน** สคริปต์ปริ้น JSON line พร้อม `image_path` และ `folder` ให้โชว์ absolute path

ภาพรันอัตโนมัติโดยไม่ต้องถาม ห้ามเจน variants ล่วงหน้า: หนึ่งคำขอ = หนึ่งภาพ

## Step 4: Repair

ถ้าภาพออกมาพลาสติก ปลอม หรือแบน ห้ามเริ่มใหม่ อ่าน `references/troubleshooting.md` หาองค์ประกอบ AVB-6 ที่ผิด แก้เฉพาะจุดนั้น แล้วบอกผู้ใช้ในหนึ่งบรรทัดว่าแก้อะไร

## Rules

1. ภาพราคาต่ำกว่า ~$0.05 รันอัตโนมัติ `gpt-image-2` หรือ `nano-banana-pro` ที่ 4K อาจเกิน ถ้าเป็นชุดใหญ่ให้ quote ราคาก่อน
2. **ห้ามพรรณนาโลโก้ สินค้า หรือใบหน้าด้วยคำพูด** ให้ส่งไฟล์จริงผ่าน `--input-image` ไฟล์อ้างอิงเก็บใน `generations/refs/`
3. **ห้ามซ่อนการสลับ provider** บอกเสมอว่ารันผ่านเส้นทางไหนและทำไม
4. หนึ่งคำขอ = หนึ่งภาพ ห้ามเจน variants ล่วงหน้า
5. Draft cheap, finish pretty: วนซ้ำที่ `nano-banana-2-lite` หรือ 1K ก่อน แล้วค่อย rerun ตัวที่ชนะที่ `gpt-image-2` 2K หรือ 4K
6. ห้าม paste API key ลงในแชต และห้ามเขียน key ลงในโฟลเดอร์สกิลไม่ว่ากรณีใด key อยู่ที่ `<project root>/.env` เท่านั้น
7. Kie result URLs หมดอายุภายในไม่กี่ชั่วโมง สคริปต์ดาวน์โหลดทันที ห้ามส่ง raw URL ให้ผู้ใช้เป็น deliverable

## Self-Update

**หมายเหตุ:** endpoint และ slug ของ Kie ใน `models.json` ยังไม่ได้ยืนยันกับเอกสารจริง (`"verified": false`) เพราะตอนสร้างเข้าถึง docs.kie.ai ไม่ได้ ครั้งแรกที่รันผ่าน Kie สำเร็จ ให้เปลี่ยนเป็น `true` ถ้าได้ 404/422 ให้เทียบกับเอกสารแล้วแก้


ถ้า model id 404 แปลว่า Kie slug เปลี่ยน: หา id ปัจจุบันที่ https://kie.ai/market แล้วอัปเดต `models.json` บอกผู้ใช้ด้วยว่าเปลี่ยนอะไร สคริปต์เตือนเมื่อ registry เก่ากว่า 30 วัน เสนอ refresh ครั้งเดียวแล้วปล่อย

## Troubleshooting

ดูตารางอาการและข้อผิดพลาดเต็มที่ `references/troubleshooting.md`
