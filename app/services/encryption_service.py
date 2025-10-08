from cryptography.fernet import Fernet
from app.config import settings
import json

class EncryptionService:
    def __init__(self):
        # .env에서 ENCRYPTION_KEY 가져오기
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt_json(self, data: dict) -> bytes:
        """딕셔너리를 JSON으로 변환 후 암호화"""
        json_str = json.dumps(data, ensure_ascii=False)
        return self.cipher.encrypt(json_str.encode('utf-8'))
    
    def decrypt_json(self, encrypted_data: bytes) -> dict:
        """암호화된 데이터를 복호화 후 딕셔너리로 변환"""
        if not encrypted_data:
            return None
        decrypted = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted.decode('utf-8'))

# 싱글톤 인스턴스
encryption_service = EncryptionService()