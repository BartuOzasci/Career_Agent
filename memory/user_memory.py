"""
Kullanıcı Belleği Modülü

Bu modül, kullanıcının kariyer hedeflerini ve planlarını kalıcı olarak 
saklamak için bir bellek yönetim sistemi sağlar. Veriler JSON formatında 
saklanır ve yönetilir.

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

import json
import os
from typing import Any, Optional


class UserMemory:
    """
    Kullanıcı belleği yönetim sınıfı.
    
    Bu sınıf, kullanıcının kariyer hedeflerini, planlarını ve diğer ilgili
    bilgileri JSON dosyasında saklar ve yönetir. Bellek verileri anahtar-değer
    çiftleri şeklinde tutulur ve kalıcı depolama sağlar.
    
    Attributes:
        file_path (str): Bellek verilerinin saklanacağı JSON dosyasının yolu
        memory (dict): Bellekteki mevcut veri sözlüğü
    """
    
    def __init__(self, file_path: str = "user_memory.json"):
        """
        UserMemory sınıfının constructor fonksiyonu.
        
        Belirtilen dosya yolunda bir JSON dosyası oluşturur veya mevcut olanı
        yükler. Dosya yoksa boş bir JSON dosyası oluşturulur.
        
        Args:
            file_path (str, optional): Bellek dosyasının yolu. 
                                       Varsayılan değer "user_memory.json"
        """
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        self.memory = self.load_memory()

    def load_memory(self) -> dict:
        """
        Bellekteki verileri JSON dosyasından yükler.
        
        Returns:
            dict: Bellekte saklanan tüm veriler
            
        Raises:
            json.JSONDecodeError: JSON dosyası geçersiz formatta ise
            IOError: Dosya okuma hatası oluşursa
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def save_memory(self) -> None:
        """
        Mevcut bellek verilerini JSON dosyasına kaydeder.
        
        Bellekteki tüm değişiklikler bu metod çağrıldığında dosyaya yazılır.
        Türkçe karakterler korunarak kaydedilir.
        
        Raises:
            IOError: Dosya yazma hatası oluşursa
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def update_goal(self, goal: str) -> None:
        """
        Kullanıcının kariyer hedefini günceller.
        
        Bu metod, kullanıcının kariyer hedefini 'career_goal' anahtarı
        altında saklar ve değişiklikleri dosyaya kaydeder.
        
        Args:
            goal (str): Kullanıcının yeni kariyer hedefi
            
        Example:
            >>> memory = UserMemory()
            >>> memory.update_goal("Yazılım Mühendisi olmak")
        """
        self.memory['career_goal'] = goal
        self.save_memory()

    def update_memory(self, key: str, value: Any) -> None:
        """
        Bellekte herhangi bir anahtar-değer çiftini günceller veya ekler.
        
        Bu genel amaçlı metod, bellekte herhangi bir veriyi saklamak için
        kullanılabilir. Değişiklikler otomatik olarak dosyaya kaydedilir.
        
        Args:
            key (str): Saklanacak verinin anahtarı
            value (Any): Saklanacak veri (herhangi bir JSON serileştirilebilir tip)
            
        Example:
            >>> memory = UserMemory()
            >>> memory.update_memory("completed_tasks", ["Görev 1", "Görev 2"])
            >>> memory.update_memory("progress", 75.5)
        """
        self.memory[key] = value
        self.save_memory()

    def get_memory(self, key: str) -> Optional[Any]:
        """
        Bellekten belirtilen anahtara sahip veriyi getirir.
        
        Args:
            key (str): Getirilecek verinin anahtarı
            
        Returns:
            Optional[Any]: Anahtara karşılık gelen değer. Anahtar yoksa None döner.
            
        Example:
            >>> memory = UserMemory()
            >>> goal = memory.get_memory("career_goal")
            >>> print(goal)  # "Yazılım Mühendisi olmak" veya None
        """
        return self.memory.get(key, None)
