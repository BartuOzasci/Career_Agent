"""
Kariyer Planlama Ajanı Modülü

Bu modül, kullanıcıların kariyer hedeflerine göre detaylı kariyer planları 
oluşturmak için Google Gemini AI modelini kullanan bir ajan sınıfı içerir.

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import json


class CareerGoalAgent:
    """
    Kariyer planlama ajanı sınıfı.
    
    Bu sınıf, Google Gemini AI modelini kullanarak kullanıcıların kariyer 
    hedeflerine göre özelleştirilmiş kariyer planları oluşturur.
    
    Attributes:
        chat_model (ChatGoogleGenerativeAI): Google Gemini AI chat modeli instance'ı
    """
    
    def __init__(self, api_key: str):
        """
        CareerGoalAgent sınıfının constructor fonksiyonu.
        
        Args:
            api_key (str): Google Gemini API anahtarı
        """
        self.chat_model = ChatGoogleGenerativeAI(
            api_key=api_key, 
            model="gemini-2.5-flash",
            temperature=0.5
        )

    def ask_career_plan(self, career_goal: str) -> dict:
        """
        Kullanıcıdan gelen hedefe göre kariyer planı oluşturma fonksiyonu.
        
        Bu fonksiyon, kullanıcının kariyer hedefini alır ve AI modelinden
        detaylı bir kariyer planı talep eder. Plan; gerekli beceriler,
        önerilen eğitimler, deneyim gereksinimleri ve izlenecek adımları içerir.
        
        Args:
            career_goal (str): Kullanıcının kariyer hedefi
            
        Returns:
            dict: Kariyer planı bilgilerini içeren JSON formatında sözlük
                - adımlar: İzlenecek adımların listesi
                - gerekli_beceriler: Gerekli becerilerin listesi
                - önerilen_egitim: Önerilen eğitimlerin listesi
                - deneyim: Deneyim gereksinimlerinin listesi
                
        Raises:
            ValueError: AI yanıtı JSON formatında değilse
        """
        messages = [
            SystemMessage(content = (
                "Sen bir kariyer planlama asistanısın. Kullanıcının kariyer hedeflerine göre detaylı bir kariyer planı oluşturmalısın."
                "Kariyer planı; gerekli beceriler, eğitim, deneyim ve önerilen adımları içermelidir."
                "Hedef kullanıcının kariyer hedefi doğrultusunda özelleştirilmelidir."
                "Sonuçlar *sadece* aşağıdaki JSON formatında olmalıdır:\n"
                "{\n \"adımlar\": [\"...\"],\n \"gerekli_beceriler\": [\"...\"],\n \"önerilen_egitim\": [\"...\"],\n \"deneyim\": [\"...\"]\n}\n"
                
            )),
            HumanMessage(content = f"Kariyer hedefim: {career_goal}. Bana bu hedefe ulaşmak için ayrıntılı bir kariyer planı oluşturur musun?")
        ]

        response = self.chat_model.invoke(messages)

        # yanıtın içeriği parse edilip JSON formatında döndürülüyor
        return self.parse_response(response.content)
    
    def parse_response(self, response_content: str) -> dict:
        """
        AI modelinden gelen yanıtı JSON formatına dönüştürür.
        
        AI modeli yanıtı markdown kod blokları içinde döndürebilir (```json ... ```).
        Bu metod, bu tür işaretleri temizleyerek saf JSON içeriğini çıkarır.
        
        Args:
            response_content (str): AI modelinden gelen ham yanıt metni
            
        Returns:
            dict: Parse edilmiş JSON objesi
            
        Raises:
            ValueError: Yanıt JSON formatında değilse veya parse edilemezse
        """
        # Markdown kod bloklarını temizle
        content = response_content.strip()
        
        # ```json ve ``` işaretlerini kaldır
        if content.startswith('```json'):
            content = content[7:]  # ```json kısmını kaldır
        elif content.startswith('```'):
            content = content[3:]  # ``` kısmını kaldır
            
        if content.endswith('```'):
            content = content[:-3]  # Son ``` kısmını kaldır
            
        content = content.strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Yanıt JSON formatına dönüştürülemedi. Hata: {str(e)}\n"
                f"İçerik: {content[:200]}..."
            )


        