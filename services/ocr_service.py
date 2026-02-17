from paddleocr import PaddleOCR


class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True, lang="ch", use_gpu=False, show_log=False
        )

    def extract_text(self, image_path):
        try:
            result = self.ocr.ocr(image_path, cls=True)

            if not result or not result[0]:
                return []

            extracted_texts = []
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                extracted_texts.append({"text": text, "confidence": confidence})

            return extracted_texts
        except Exception as e:
            raise Exception(f"OCR extraction failed: {str(e)})")


def get_ocr_service():
    return OCRService()
