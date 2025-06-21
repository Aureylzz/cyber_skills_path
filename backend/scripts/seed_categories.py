import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal
from app.models import Category, SubTheme
from app.services.category_service import CategoryService
from app.services.sub_theme_service import SubThemeService
from app.schemas import CategoryCreate, SubThemeCreate

async def seed_categories():
    async with AsyncSessionLocal() as session:
        # Check if categories already exist
        count = await CategoryService.get_category_count(session)
        if count > 0:
            print(f"Categories already seeded ({count} categories exist)")
            return
        
        # Define categories and their sub-themes
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
                "name": "Application & API Security",
                "display_order": 3,
                "sub_themes": [
                    "Application Security",
                    "Secure Coding",
                    "API Security",
                    "Software Architecture"
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
            print(f"✅ Created category: {category.name}")
            
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

if __name__ == "__main__":
    asyncio.run(seed_categories())