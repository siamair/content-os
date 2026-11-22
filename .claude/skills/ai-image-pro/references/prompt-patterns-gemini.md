# Prompt Patterns: Gemini (Nano Banana / Gemini Image)

- Gemini เข้าใจ **ประโยคเล่าเรื่องเป็นธรรมชาติ** ดีกว่ารายการคีย์เวิร์ด เขียนเป็นย่อหน้าบรรยายฉาก
- เริ่มด้วยคำสั่งชัด ๆ: "Generate a photorealistic image of ..." เพื่อให้คืนภาพ ไม่ใช่ข้อความ
- **แก้ภาพจากภาพอ้างอิง**: ใส่ภาพก่อนข้อความ แล้วพูดแบบสั่งงาน "Using the attached photo of this cat, show the same cat as a 2-year-old adult. Keep its coat pattern and facial markings exactly."
- หลายภาพอ้างอิง: ระบุบทบาท "Image 1 is the character, Image 2 is the background"
- อธิบาย "ทำไม" ช่วยได้: "for a cozy Instagram post" ทำให้เลือกองค์ประกอบเหมาะ
- Aspect ratio และ resolution ส่งผ่าน `imageConfig` (สคริปต์จัดการให้) ไม่ต้องเขียนใน prompt
- ข้อห้ามให้เขียนเชิงบวก: "an empty, quiet street" ดีกว่า "no cars"
