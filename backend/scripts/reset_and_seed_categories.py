import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import AsyncSessionLocal
from app.models import Category, SubTheme
from app.services.category_service import CategoryService
from app.services.sub_theme_service import SubThemeService
from app.schemas import CategoryCreate, SubThemeCreate

async def reset_and_seed_categories():
    async with AsyncSessionLocal() as session:
        # Clear existing data in correct order (due to foreign keys)
        await session.execute(text("DELETE FROM sub_themes"))
        await session.execute(text("DELETE FROM categories"))
        await session.commit()
        print("✅ Cleared existing categories and sub-themes")
        
        # Define all categories and their sub-themes
        categories_data = [
            {
                "name": "Network & Infrastructure Security",
                "display_order": 1,
                "sub_themes": [
                    "Network Security",
                    "DNS",
                    "VPN", 
                    "Proxies",
                    "Linux Administration"
                ]
            },
            {
                "name": "Cloud & Container Security",
                "display_order": 2,
                "sub_themes": [
                    "Cloud Security (IaaS/PaaS/SaaS)",
                    "Container/Kubernetes Security",
                    "DevSecOps",
                    "Identity and Access Management (IAM)"
                ]
            },
            {
                "name": "Endpoint & IoT Security",
                "display_order": 3,
                "sub_themes": [
                    "Endpoint Security",
                    "Mobile Security",
                    "IoT Security",
                    "OT/ICS Security",
                    "Medical Device Security"
                ]
            },
            {
                "name": "Application & API Security",
                "display_order": 4,
                "sub_themes": [
                    "Application Security",
                    "Secure Coding",
                    "API Security",
                    "OOP (secure design patterns)",
                    "Software Architecture"
                ]
            },
            {
                "name": "Cryptography & Emerging Tech",
                "display_order": 5,
                "sub_themes": [
                    "Cryptography",
                    "Quantum-Safe Cryptography",
                    "Blockchain/Cryptocurrency Security",
                    "AI/ML Security",
                    "Privacy Engineering"
                ]
            },
            {
                "name": "Security Operations (SecOps)",
                "display_order": 6,
                "sub_themes": [
                    "Security Operations Center (SOC)",
                    "Incident Response",
                    "Digital Forensics",
                    "Vulnerability Management",
                    "Penetration Testing",
                    "Cyber Threat Hunting"
                ]
            },
            {
                "name": "Risk & Compliance",
                "display_order": 7,
                "sub_themes": [
                    "Risk Management",
                    "Compliance (GDPR/HIPAA/PCI-DSS)",
                    "Third-Party Risk Management",
                    "Supply Chain Security",
                    "Security Policy Management"
                ]
            },
            {
                "name": "Access Control & Trust",
                "display_order": 8,
                "sub_themes": [
                    "Zero Trust Architecture",
                    "Insider Threat Management",
                    "Social Engineering Defense",
                    "Security Culture Development"
                ]
            },
            {
                "name": "Low-Level & Exploit Analysis",
                "display_order": 9,
                "sub_themes": [
                    "Low-level Programming",
                    "Reverse Engineering",
                    "Memory Safety",
                    "Automotive Security"
                ]
            },
            {
                "name": "Specialized & Industry-Specific Security",
                "display_order": 10,
                "sub_themes": [
                    "Aeronautical Security",
                    "Critical Infrastructure Protection",
                    "Cyber Warfare and Defense",
                    "Security Architecture"
                ]
            }
        ]
        
        # Create categories and sub-themes
        for cat_data in categories_data:
            # Create category
            category = await CategoryService.create_category(
                session,
                CategoryCreate(
                    name=cat_data["name"],
                    display_order=cat_data["display_order"]
                )
            )
            print(f"\n✅ Created category: {category.name}")
            
            # Create sub-themes
            for idx, sub_theme_name in enumerate(cat_data["sub_themes"]):
                sub_theme = await SubThemeService.create_sub_theme(
                    session,
                    SubThemeCreate(
                        name=sub_theme_name,
                        category_id=category.id,
                        display_order=idx + 1
                    )
                )
                print(f"   - Added sub-theme: {sub_theme.name}")
        
        print(f"\n✅ Successfully seeded {len(categories_data)} categories!")

if __name__ == "__main__":
    asyncio.run(reset_and_seed_categories())
