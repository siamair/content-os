# Troubleshooting: แมปอาการ → องค์ประกอบที่ผิด

ซ่อมเฉพาะจุด ห้ามเขียน prompt ใหม่ทั้งหมด แก้ทีละองค์ประกอบ แล้วบอกผู้ใช้หนึ่งบรรทัดว่าแก้อะไร

## อาการของภาพ

| อาการ | องค์ประกอบผิด | วิธีแก้ |
|---|---|---|
| ผิว/ขนดูพลาสติก เรียบเกิน | Style + Lighting | ดู `de-plasticize-checklist.md`; เพิ่ม "natural texture, film grain", เปลี่ยนเป็นแสงทิศทางเดียว |
| ภาพแบน ไม่มีมิติ | Lighting + Vantage | เพิ่ม side light, rim light, ชั้น foreground/background, f/2.0 |
| ตัวแบบไม่เหมือนภาพอ้างอิง | Subject | ใส่ `--input-image` และประโยค "keep the exact identity/markings from the reference"; ลด adjectives ที่ขัดกับภาพ |
| องค์ประกอบในภาพผิด/เกิน | Setting | ระบุสิ่งที่ต้องมีให้ชัด และใส่ "no ..." สำหรับสิ่งที่เกิน |
| มุมกล้องไม่ตรงใจ | Vantage | ระบุมุม + เลนส์ + ระยะ เป็นคำศัพท์จาก `camera-movements.md` |
| สีจัดเกิน ดูเป็น AI | Style + Mood | "natural color grading, muted tones, no oversaturation" |
| อารมณ์ไม่ใช่ | Mood | เปลี่ยนคำ Mood และปรับ Lighting ให้สอดคล้อง |
| ตัวอักษรในภาพเพี้ยน | Style | ใช้ `gpt-image-2`, ข้อความสั้น ใส่ในเครื่องหมายคำพูด |
| มือ/ขา/นิ้วเกิน | Subject | ระบุท่าทางให้ชัด, เพิ่ม "anatomically correct, four legs" |
| สไตล์หลุด (สมจริง↔การ์ตูน) | Style | วาง Style ไว้ทั้งต้นและท้าย prompt |

## ข้อผิดพลาดของสคริปต์

| ข้อความ | สาเหตุ | แก้ |
|---|---|---|
| `image: BLOCKED` | ไม่มี key เลย | ใส่ `KIE_API_KEY` หรือ `GEMINI_API_KEY` ใน `<project root>/.env` |
| HTTP 401 / 403 | key ผิดหรือหมดอายุ | ออก key ใหม่ |
| HTTP 404 model | slug โมเดลเปลี่ยน | อัปเดต `models.json` (ดู https://kie.ai/market หรือ https://ai.google.dev/gemini-api/docs/models) |
| HTTP 429 | เกินโควตา | รอ หรือสลับ provider |
| `blocked by network` / proxy 403 | เครือข่ายของ environment บล็อก host | อนุญาต host นั้นใน network policy หรือใช้อีก provider |
| Gemini คืนข้อความแต่ไม่มีภาพ | prompt ถูก safety filter หรือโมเดลตอบเป็นข้อความ | ปรับถ้อยคำ, ระบุ "Generate an image" ชัด ๆ |
| Kie task `fail` | prompt ถูกปฏิเสธหรือ input ผิด | ดู `failMsg` ใน output |
| `.env` ในโฟลเดอร์สกิล | วาง key ผิดที่ | ย้ายไป project root แล้วลบตัวเดิม |
