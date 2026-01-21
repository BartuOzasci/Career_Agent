"""
Kariyer Planlayıcı Ana Modül

Bu modül, kariyer hedeflerine göre detaylı kariyer planları oluşturmak,
görev zaman çizelgeleri hazırlamak ve ilgili kaynakları önermek için
çeşitli ajanlar ve araçlar kullanır.

Ana İşlevler:
    - Kullanıcıdan kariyer hedefini alır
    - Google Gemini AI ile kariyer planı oluşturur
    - Görev zaman çizelgesi hazırlar
    - İlgili web kaynaklarını önerir
    - Tüm bilgileri kullanıcı belleğinde saklar

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

from agents.task_scheduler_agent import TaskSchedulerAgent
from agents.career_goal_agent import CareerGoalAgent
from tools.suggestion_tool import SuggestionTool
from memory.user_memory import UserMemory
from dotenv import load_dotenv
import json
import os

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()


def main() -> None:
    """
    Ana uygulama fonksiyonu.
    
    Bu fonksiyon, kariyer planlama sürecinin tüm adımlarını koordine eder:
    1. Kullanıcı belleğini başlatır
    2. Kullanıcıdan kariyer hedefini alır
    3. AI ile kariyer planı oluşturur
    4. Görev zaman çizelgesi hazırlar
    5. İlgili kaynakları arar ve önerir
    6. Tüm verileri kaydeder
    
    Raises:
        ValueError: Geçersiz API anahtarı veya yanıt formatı
        IOError: Dosya okuma/yazma hatası
        
    Example:
        Program çalıştırıldığında:
        $ python main.py
        Kariyer hedefinizi girin: Veri Bilimci
        [Kariyer planı oluşturulur ve kaydedilir]
    """
    print("=" * 60)
    print("Kariyer Planlayıcı Ajan Başlatıldı.")
    print("=" * 60)
    
    # Kullanıcı belleğini başlat
    user_memory = UserMemory()

    # Kullanıcıdan kariyer hedefini al
    goal = input("\nKariyer hedefinizi girin: ")
    user_memory.update_goal(goal)

    # API anahtarını çevre değişkeninden al
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        print("HATA: GOOGLE_GEMINI_API_KEY çevre değişkeni bulunamadı.")
        print("Lütfen .env dosyasında API anahtarınızı ayarlayın.")
        return

    # Kariyer planı oluştur
    print("\n[1/3] Kariyer planı oluşturuluyor...")
    goal_agent = CareerGoalAgent(api_key=api_key)
    career_plan = goal_agent.ask_career_plan(goal)

    print("\n✓ Oluşturulan Kariyer Planı:")
    print("-" * 60)
    print(json.dumps(career_plan, indent=4, ensure_ascii=False))
    print("-" * 60)

    # Görev zaman çizelgesi oluştur
    print("\n[2/3] Görev zaman çizelgesi hazırlanıyor...")
    task_agent = TaskSchedulerAgent(weeks=4)
    tasks = career_plan.get("adımlar", [])
    
    if tasks:
        schedule = task_agent.create_schedule(tasks)
        task_agent.save_schedule(schedule, "career_schedule.json")
        print("✓ Görev zaman çizelgesi 'career_schedule.json' dosyasına kaydedildi.")
    else:
        print("⚠ Kariyer planında adım bulunamadı.")

    # İlgili kaynakları ara ve öner
    print("\n[3/3] İlgili kaynaklar aranıyor...")
    suggestion_tool = SuggestionTool()
    resources = suggestion_tool.search_resources(f"{goal} için kaynaklar", max_results=5)
    
    print("\n✓ Önerilen Kaynaklar:")
    print("-" * 60)
    for idx, resource in enumerate(resources, 1):
        print(f"{idx}. {resource}")
    print("-" * 60)
    
    user_memory.update_memory("recommended_resources", resources)

    print("\n" + "=" * 60)
    print("✓ Kariyer planlama süreci başarıyla tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Railway deployment için API app'ini export et
try:
    from api import app
except ImportError:
    app = None
