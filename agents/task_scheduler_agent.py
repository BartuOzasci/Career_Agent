"""
Görev Zamanlama Ajanı Modülü

Bu modül, görevleri belirli bir zaman dilimi içinde planlayan ve 
bu planları JSON formatında kaydeden bir ajan sınıfı içerir.

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

import datetime
import json


class TaskSchedulerAgent:
    """
    Görev zamanlama ajanı sınıfı.
    
    Bu sınıf, verilen görevleri belirli bir zaman aralığına göre planlar
    ve bu planları JSON formatında kaydeder. Her görev, belirlenen hafta
    sayısına göre otomatik olarak tarihlere atanır.
    
    Attributes:
        weeks (int): Görevlerin planlanacağı hafta sayısı
    """
    
    def __init__(self, weeks: int = 4):
        """
        TaskSchedulerAgent sınıfının constructor fonksiyonu.
        
        Args:
            weeks (int, optional): Görevlerin planlanacağı hafta sayısı. 
                                   Varsayılan değer 4 haftadır.
        """
        self.weeks = weeks

    def create_schedule(self, tasks: list) -> dict:
        """
        Görev listesinden bir zaman çizelgesi oluşturur.
        
        Her görev, bugünden itibaren belirtilen hafta sayısı kadar sonrasına
        planlanır ve ardışık günlere dağıtılır. İlk görev belirtilen hafta
        sonunda başlar, sonraki görevler ardışık günlere atanır.
        
        Args:
            tasks (list): Planlanacak görevlerin listesi (str elemanlar)
            
        Returns:
            dict: Görev isimlerini tarihlerle eşleştiren sözlük.
                  Format: {"görev_adı": "YYYY-MM-DD", ...}
                  
        Example:
            >>> agent = TaskSchedulerAgent(weeks=2)
            >>> tasks = ["Python öğren", "Proje yap", "Portfolio hazırla"]
            >>> schedule = agent.create_schedule(tasks)
            >>> print(schedule)
            {'Python öğren': '2026-02-04', 'Proje yap': '2026-02-05', ...}
        """
        schedule = {}
        current_date = datetime.date.today()
        delta = datetime.timedelta(weeks=self.weeks)

        for task in tasks:
            due_date = current_date + delta
            schedule[task] = due_date.strftime("%Y-%m-%d")
            current_date += datetime.timedelta(days=1)

        return schedule
    
    def save_schedule(self, schedule: dict, filename: str = "schedule.json") -> None:
        """
        Oluşturulan zaman çizelgesini JSON dosyasına kaydeder.
        
        Args:
            schedule (dict): Kaydedilecek zaman çizelgesi sözlüğü
            filename (str, optional): Kaydedilecek dosyanın adı. 
                                     Varsayılan değer "schedule.json"
                                     
        Raises:
            IOError: Dosya yazma işlemi başarısız olursa
            
        Example:
            >>> agent = TaskSchedulerAgent()
            >>> schedule = {"Görev 1": "2026-02-04"}
            >>> agent.save_schedule(schedule, "my_schedule.json")
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=4, ensure_ascii=False)