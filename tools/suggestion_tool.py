"""
Kaynak Önerisi Aracı Modülü

Bu modül, DuckDuckGo arama motorunu kullanarak web'den kariyer ve eğitim
ile ilgili kaynakları arayan bir araç sınıfı içerir.

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

from ddgs import DDGS
from typing import List, Dict, Any


class SuggestionTool:
    """
    Kaynak önerisi aracı sınıfı.
    
    Bu sınıf, DuckDuckGo arama motoru API'sini kullanarak belirtilen
    sorguya göre web'den ilgili kaynakları arar ve döndürür. Kariyer
    planlaması, eğitim materyalleri ve diğer konularda kaynak bulmak
    için kullanılır.
    
    Attributes:
        ddgs (DDGS): DuckDuckGo arama motoru instance'ı
    """
    
    def __init__(self):
        """
        SuggestionTool sınıfının constructor fonksiyonu.
        
        DuckDuckGo arama motoru nesnesini başlatır.
        """
        self.ddgs = DDGS()

    def search_resources(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Verilen sorgu için web'den kaynakları arar.
        
        DuckDuckGo arama motorunu kullanarak belirtilen sorguya göre
        en alakalı sonuçları döndürür. Her sonuç başlık, URL ve kısa
        açıklama içerir.
        
        Args:
            query (str): Aranacak sorgu metni
            max_results (int, optional): Döndürülecek maksimum sonuç sayısı.
                                         Varsayılan değer 5
                                         
        Returns:
            List[Dict[str, Any]]: Arama sonuçlarının listesi. Her sonuç bir sözlük
                                  olup başlık, URL ve açıklama içerir.
                                  
        Example:
            >>> tool = SuggestionTool()
            >>> results = tool.search_resources("Python programlama kursu", max_results=3)
            >>> for result in results:
            ...     print(result['title'], result['url'])
            
        Note:
            İnternet bağlantısı gerektirir. Arama motoru API'sinin limitlerine tabidir.
        """
        results = []
        try:
            # DDGS kütüphanesinde text() metodu kullanılır
            search_results = self.ddgs.text(query, max_results=max_results)
            for result in search_results:
                results.append(result)
        except Exception as e:
            print(f"⚠ Arama sırasında hata oluştu: {str(e)}")
        return results
    

