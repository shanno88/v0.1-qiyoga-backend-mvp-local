# Temporarily disabled for Railway deployment
# from rapidocr_onnxruntime import RapidOCR


class OCRService:
    def __init__(self):
        pass

    def recognize_image(self, image_path):
        raise NotImplementedError(
            "OCR temporarily disabled - will use cloud OCR API later"
        )

    def recognize_images(self, image_paths):
        raise NotImplementedError(
            "OCR temporarily disabled - will use cloud OCR API later"
        )


def get_ocr_service():
    return OCRService()
