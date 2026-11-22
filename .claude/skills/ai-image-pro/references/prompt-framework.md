# AVB-6 Prompt Framework (Prompt Ladder)

เขียน prompt โดยปีนบันได 6 ขั้นตามลำดับ แต่ละขั้นตอบหนึ่งคำถาม ห้ามข้ามขั้น ถ้าผู้ใช้ไม่ได้ระบุ ให้เติมค่าเริ่มต้นที่สมเหตุสมผลและไม่ขัดกับคำของผู้ใช้

| ขั้น | องค์ประกอบ | คำถาม | ตัวอย่าง |
|---|---|---|---|
| 1 | **Subject** | อะไร/ใคร กำลังทำอะไร ลักษณะเด่นที่ต้องเห็น | an adult long-haired tortoiseshell cat sitting upright |
| 2 | **Setting** | อยู่ที่ไหน มีอะไรรอบตัว | on a wooden office desk, monitor blurred behind |
| 3 | **Vantage** | มุมกล้อง เลนส์ ระยะ | eye-level, 85mm, f/2.0, shallow depth of field |
| 4 | **Lighting** | แหล่งแสง ทิศ คุณภาพ สี | soft window light from the left, warm bounce |
| 5 | **Mood** | ความรู้สึก อารมณ์ จังหวะ | calm, warm, quietly regal |
| 6 | **Style** | สื่อ/สไตล์ ความสมจริง พื้นผิว | photorealistic pet photography, natural color, film grain |

## โครงประโยค

```
<Subject>. <Setting>. <Vantage>. <Lighting>. <Mood>. <Style>. <Constraints / negatives>.
```

- เรียง Subject ไว้ก่อนเสมอ โมเดลให้น้ำหนักคำแรก ๆ มากที่สุด
- ใช้คำที่เห็นภาพได้ (concrete) แทนคำคุณศัพท์ลอย ๆ: "fine individual fur strands catching light" ดีกว่า "beautiful fur"
- ปิดท้ายด้วยข้อห้ามสั้น ๆ: no text, no watermark, no extra limbs, no CGI look
- ถ้ามีภาพอ้างอิง ให้เริ่มด้วยประโยคบอกบทบาทภาพ: "Use the attached photo as the identity reference for this exact cat; keep its markings."
- ภาษาอังกฤษให้ผลเสถียรกว่า ให้แปลคำขอภาษาไทยเป็นอังกฤษ แต่ข้อความที่ต้องปรากฏในภาพให้คงภาษาเดิมไว้ในเครื่องหมายคำพูด

## Checklist ก่อนรัน

- [ ] ทุกคำของผู้ใช้อยู่ใน prompt ครบ ไม่ตีความเพิ่มเกินที่เขาพูด
- [ ] มีครบ 6 องค์ประกอบ
- [ ] ไม่พรรณนาโลโก้/ใบหน้า/สินค้าจริงด้วยคำพูด ใช้ `--input-image` แทน
- [ ] เลือก aspect ratio ตามการใช้งาน (โซเชียลแนวตั้ง 4:5 หรือ 9:16, ปก 16:9, ภาพสัตว์เลี้ยง 3:4)
