"""
Kariyer Planlayıcı API Servisi

Bu modül, kariyer planlama ajanlarını REST API olarak sunar.
React frontend ile entegrasyon için FastAPI kullanılır.

Yazar: Bartu
Tarih: 21 Ocak 2026
Versiyon: 1.0.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
import os
from dotenv import load_dotenv
import json
import asyncio

from agents.career_goal_agent import CareerGoalAgent
from agents.task_scheduler_agent import TaskSchedulerAgent
from tools.suggestion_tool import SuggestionTool
from memory.user_memory import UserMemory

# Çevre değişkenlerini yükle
load_dotenv()

# FastAPI uygulaması
app = FastAPI(
    title="Kariyer Gelişim Ajanı API",
    description="AI destekli kariyer planlama ve danışmanlık servisi",
    version="1.0.0"
)

# CORS ayarları - React uygulamasından erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://kariyerajani.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response modelleri
class ChatRequest(BaseModel):
    """Chat isteği modeli"""
    message: str
    user_id: Optional[str] = "default_user"


class ChatResponse(BaseModel):
    """Chat yanıtı modeli"""
    response: str
    career_plan: Optional[dict] = None
    schedule: Optional[dict] = None
    resources: Optional[list] = None


# Global değişkenler
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
goal_agent = None

if api_key:
    goal_agent = CareerGoalAgent(api_key=api_key)


@app.get("/")
async def root():
    """API ana endpoint'i"""
    return {
        "message": "Kariyer Gelişim Ajanı API'sine hoş geldiniz!",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {
        "status": "healthy",
        "api_key_configured": api_key is not None
    }


async def generate_stream_response(text: str) -> AsyncGenerator[str, None]:
    """
    Yanıtı kelime kelime stream eder.
    
    Args:
        text (str): Stream edilecek metin
        
    Yields:
        str: JSON formatında kelimeler
    """
    words = text.split()
    for i, word in enumerate(words):
        # Her kelimeyi space ile birlikte gönder (son kelime hariç)
        chunk = word + (" " if i < len(words) - 1 else "")
        yield f"data: {json.dumps({'text': chunk, 'done': False})}\n\n"
        # Doğal bir yazma hissi için kısa gecikme
        await asyncio.sleep(0.05)
    
    # Stream tamamlandı sinyali
    yield f"data: {json.dumps({'text': '', 'done': True})}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint'i - Yanıtlar kelime kelime gelir
    
    Args:
        request (ChatRequest): Kullanıcı mesajı
        
    Returns:
        StreamingResponse: SSE formatında stream yanıt
    """
    if not goal_agent:
        raise HTTPException(
            status_code=500,
            detail="API anahtarı yapılandırılmamış. Lütfen GOOGLE_GEMINI_API_KEY ayarlayın."
        )
    
    try:
        # Kullanıcı mesajından kariyer hedefini çıkar
        message = request.message.strip()
        
        # Basit bir komut analizi
        if any(keyword in message.lower() for keyword in ['merhaba', 'selam', 'hey', 'hello']):
            response_text = "👋 Merhaba! Ben Kariyer Gelişim Ajanı.\n\n✨ Size kariyer hedeflerinizde yardımcı olabilirim. Kariyer hedefinizi benimle paylaşır mısınız?"
        else:
            # Kariyer planı oluştur
            career_plan = goal_agent.ask_career_plan(message)
            
            # Yanıtı formatla
            response_text = f"🎯 Harika! '{message}' hedefi için size detaylı bir kariyer planı hazırladım!\n\n"
            response_text += "═" * 50 + "\n\n"
            
            if "adımlar" in career_plan:
                response_text += "📋 İZLENECEK ADIMLAR\n"
                response_text += "─" * 40 + "\n\n"
                for i, step in enumerate(career_plan["adımlar"][:5], 1):
                    response_text += f"  {i}️⃣ {step}\n\n"
                response_text += "\n"
            
            if "gerekli_beceriler" in career_plan:
                response_text += "💡 GEREKLİ BECERİLER\n"
                response_text += "─" * 40 + "\n\n"
                for skill in career_plan["gerekli_beceriler"][:5]:
                    response_text += f"  ✓ {skill}\n\n"
                response_text += "\n"
            
            if "önerilen_egitim" in career_plan:
                response_text += "📚 ÖNERİLEN EĞİTİMLER\n"
                response_text += "─" * 40 + "\n\n"
                for edu in career_plan["önerilen_egitim"][:3]:
                    response_text += f"  📖 {edu}\n\n"
                response_text += "\n"
            
            response_text += "═" * 50 + "\n\n"
            response_text += "💼 Başarılar dilerim! Herhangi bir sorunuz varsa sormaktan çekinmeyin."
            
            # Kullanıcı belleğine kaydet
            user_memory = UserMemory(f"memory_{request.user_id}.json")
            user_memory.update_goal(message)
            user_memory.update_memory("last_career_plan", career_plan)
        
        # Stream yanıt döndür
        return StreamingResponse(
            generate_stream_response(response_text),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Normal (non-streaming) chat endpoint'i
    
    Args:
        request (ChatRequest): Kullanıcı mesajı
        
    Returns:
        ChatResponse: Tam yanıt
    """
    if not goal_agent:
        raise HTTPException(
            status_code=500,
            detail="API anahtarı yapılandırılmamış. Lütfen GOOGLE_GEMINI_API_KEY ayarlayın."
        )
    
    try:
        message = request.message.strip()
        user_memory = UserMemory(f"memory_{request.user_id}.json")
        
        # Selamlaşma kontrolü
        if any(keyword in message.lower() for keyword in ['merhaba', 'selam', 'hey', 'hello']):
            return ChatResponse(
                response="Merhaba! Ben Kariyer Gelişim Ajanı. Size kariyer hedeflerinizde yardımcı olabilirim. Kariyer hedefinizi benimle paylaşır mısınız?"
            )
        
        # Kariyer planı oluştur
        career_plan = goal_agent.ask_career_plan(message)
        user_memory.update_goal(message)
        user_memory.update_memory("last_career_plan", career_plan)
        
        # Görev planı oluştur
        task_agent = TaskSchedulerAgent(weeks=4)
        tasks = career_plan.get("adımlar", [])
        schedule = None
        if tasks:
            schedule = task_agent.create_schedule(tasks[:10])
        
        # Kaynakları ara
        suggestion_tool = SuggestionTool()
        resources = suggestion_tool.search_resources(f"{message} için kaynaklar", max_results=5)
        
        # Yanıtı formatla
        response_text = f"Harika! '{message}' hedefi için detaylı bir kariyer planı hazırladım. "
        response_text += "Aşağıda adımları, becerileri ve önerilen eğitimleri bulabilirsiniz."
        
        return ChatResponse(
            response=response_text,
            career_plan=career_plan,
            schedule=schedule,
            resources=resources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Kariyer Gelişim Ajanı API başlatılıyor...")
    print("📍 API: http://localhost:8000")
    print("📖 Dokümantasyon: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
