import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User, SubTheme, Question
from app.services.question_service import QuestionService
from app.schemas import QuestionCreate, AnswerOptionCreate
from app.models.enums import QuestionType, DifficultyLevel

async def seed_sample_questions():
    async with AsyncSessionLocal() as session:
        # Get admin user
        result = await session.execute(
            select(User).where(User.username == "testuser1")
        )
        admin_user = result.scalar_one_or_none()
        if not admin_user:
            print("❌ Admin user not found. Please create testuser1 first.")
            return
        
        # Get first sub-theme (Network Security)
        result = await session.execute(
            select(SubTheme).where(SubTheme.name == "Network Security")
        )
        sub_theme = result.scalar_one_or_none()
        if not sub_theme:
            print("❌ Network Security sub-theme not found")
            return
        
        # Sample questions
        questions = [
            {
                "sub_theme_id": sub_theme.id,
                "difficulty_level": DifficultyLevel.NOVICE,
                "question_type": QuestionType.SINGLE_CHOICE,
                "question_text": "What does the acronym 'VPN' stand for?",
                "rationale": "VPN stands for Virtual Private Network, a technology that creates a secure connection over the internet.",
                "answer_options": [
                    AnswerOptionCreate(option_text="Virtual Public Network", is_correct=False, display_order=1),
                    AnswerOptionCreate(option_text="Virtual Private Network", is_correct=True, display_order=2),
                    AnswerOptionCreate(option_text="Verified Private Network", is_correct=False, display_order=3),
                    AnswerOptionCreate(option_text="Virtual Protected Network", is_correct=False, display_order=4),
                ]
            },
            {
                "sub_theme_id": sub_theme.id,
                "difficulty_level": DifficultyLevel.AMATEUR,
                "question_type": QuestionType.MULTIPLE_CHOICE,
                "question_text": "Which of the following are common network security threats?",
                "rationale": "DDoS attacks, malware, and phishing are all common network security threats. Software updates are a security measure, not a threat.",
                "answer_options": [
                    AnswerOptionCreate(option_text="DDoS attacks", is_correct=True, display_order=1),
                    AnswerOptionCreate(option_text="Malware", is_correct=True, display_order=2),
                    AnswerOptionCreate(option_text="Software updates", is_correct=False, display_order=3),
                    AnswerOptionCreate(option_text="Phishing", is_correct=True, display_order=4),
                ]
            },
            {
                "sub_theme_id": sub_theme.id,
                "difficulty_level": DifficultyLevel.INITIATE,
                "question_type": QuestionType.SINGLE_CHOICE,
                "question_text": "In the OSI model, at which layer does a firewall typically operate?",
                "rationale": "Most firewalls operate at Layer 3 (Network) and Layer 4 (Transport) of the OSI model, though some advanced firewalls can operate at Layer 7 (Application).",
                "answer_options": [
                    AnswerOptionCreate(option_text="Physical Layer (Layer 1)", is_correct=False, display_order=1),
                    AnswerOptionCreate(option_text="Data Link Layer (Layer 2)", is_correct=False, display_order=2),
                    AnswerOptionCreate(option_text="Network Layer (Layer 3)", is_correct=True, display_order=3),
                    AnswerOptionCreate(option_text="Presentation Layer (Layer 6)", is_correct=False, display_order=4),
                ]
            }
        ]
        
        # Create questions
        for q_data in questions:
            question = await QuestionService.create_question(
                session,
                QuestionCreate(**q_data),
                admin_user.id
            )
            print(f"✅ Created question: {question.question_text[:50]}...")
            print(f"   - Difficulty: {question.difficulty_level.value}")
            print(f"   - Type: {question.question_type.value}")
            print(f"   - Points: {question.points}")

if __name__ == "__main__":
    asyncio.run(seed_sample_questions())