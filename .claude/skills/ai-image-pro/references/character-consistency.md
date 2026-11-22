# Character Consistency (ตัวละครเดียวกันหลายช็อต)

1. **สร้างภาพหลัก (anchor) หนึ่งภาพ** ที่หน้าตรง แสงเรียบ เห็นลักษณะเด่นครบ เก็บไว้ที่ `generations/refs/<name>-anchor.png`
2. **ทุกช็อตต่อไปส่ง anchor ผ่าน `--input-image`** และขึ้นต้น prompt ว่า "Same character as the reference image: keep face, markings, colors, proportions identical."
3. **เขียน character sheet สั้น ๆ** (3-5 ลักษณะที่ห้ามเปลี่ยน) แล้ววางซ้ำทุก prompt เช่น "tortoiseshell long coat, cream chin, cream-tipped left forepaw, amber eyes, ear tufts"
4. เปลี่ยนเฉพาะ Setting / Vantage / Lighting / Mood ระหว่างช็อต อย่าเปลี่ยน Subject
5. ใช้โมเดลเดิมตลอดชุด `nano-banana-pro` รักษาตัวตนดีที่สุด
6. ถ้าเพี้ยน ให้ใส่ทั้ง anchor และช็อตที่ดีที่สุดก่อนหน้าเป็นภาพอ้างอิงสองภาพ
