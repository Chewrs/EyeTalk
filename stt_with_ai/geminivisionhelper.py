
from google.genai import types
from google import genai

class GeminiVisionHelper:
    def __init__(self):
        self.client = genai.Client()

    def describe_image(
        self,
        model="gemini-2.5-flash",
        image_path="Images/image.jpg",
        prompt = None
        ):


        if prompt and prompt.strip():
            prompt = f'''คุณคือผู้หญิง คุณเป็นผู้ช่วยผู้คนตาบอด คุณจะตอบสั้นๆ ไม่เกิน 3 ประโยคเสมอ 
            คุณจะตอบเป็นประโยคข้อความเสมอโดยไม่มีการใช้ย่อหน้าหรือ * 
            ห้าใช้คำว่าในรูปนี้ หรือในภาพนี้ และบางครั้งผู้ใช้อาจจะพูดผิดให้ทำความเข้าใจด้วย
            สิ่งที่คนตาบอดต้องการรู้คือ "{prompt}"'''
        else:
            prompt =  ''' คุณคือผู้หญิง ผู้ช่วยคนตาบอด
                        คุณจะตอบเป็นข้อความสั้นๆ ไม่เกิน 2 ประโยคเสมอ ห้ามขึ้นย่อหน้าใหม่ ห้ามใช้ * หรืออักขระพิเศษใดๆ
                        คุณได้รับภาพจากกล้องของผู้ใช้
                        บรรยายสิ่งตรงหน้าเป็นภาษาไทย 3 ประโยคสั้นๆ ใช้คำง่ายๆ ไม่ใช้คำว่า “ในภาพ” หรือ “รูปนี้”
                        พูดเหมือนอยู่ตรงนั้นกับผู้ใช้ บอกว่าใครอยู่ที่ไหน กำลังทำอะไร สี ท่าทาง และอารมณ์โดยรอบ
                        ตัวอย่าง: “คุณอยู่ในร้านกาแฟ มีผู้หญิงยืนอยู่หน้า เธอถือแก้วกาแฟ บรรยากาศอบอุ่น”'''



        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        response = self.client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ]
        )

        result = response.text
        return result


