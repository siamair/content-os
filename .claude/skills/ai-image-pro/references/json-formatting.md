# Structured (JSON) Prompt

ใช้เมื่อผู้ใช้ขอ หรือฉากซับซ้อนมาก (หลายตัวละคร/หลายป้ายข้อความ) ส่ง JSON ทั้งก้อนเป็นสตริงใน `--prompt`

```json
{
  "subject": {"description": "", "pose": "", "key_features": []},
  "setting": {"location": "", "foreground": "", "background": ""},
  "vantage": {"shot": "", "angle": "", "lens": "", "aperture": ""},
  "lighting": {"source": "", "direction": "", "quality": "", "color_temp": ""},
  "mood": "",
  "style": {"medium": "", "texture": "", "palette": []},
  "text_in_image": [{"text": "", "position": "", "font": ""}],
  "negatives": [],
  "aspect_ratio": "3:4"
}
```

กฎ: ทุกฟิลด์เป็นภาษาอังกฤษ ยกเว้น `text_in_image.text` ที่คงภาษาเดิม; ลบฟิลด์ที่ว่างออก
