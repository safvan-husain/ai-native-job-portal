import asyncio
import os
from database import init_db
from models import Candidate

async def seed_data():
    # Initialize database
    await init_db()

    # Clear existing candidates
    await Candidate.find_all().delete()
    print("Cleared existing candidates.")

    # 10 Developer candidates with varying/overlapping skillsets
    candidates = [
        Candidate(
            name="Alice Johnson",
            keywords=["Python", "FastAPI", "MongoDB", "AI", "Machine Learning"],
            description="Deep learning specialist with experience in building high-performance AI backends using Python and FastAPI."
        ),
        Candidate(
            name="Bob Smith",
            keywords=["React", "Node.js", "TypeScript", "Web Development", "MongoDB"],
            description="Full-stack web developer focused on building scalable frontend applications with React and robust backends."
        ),
        Candidate(
            name="Charlie Davis",
            keywords=["Flutter", "Dart", "Mobile App Development", "Firebase", "iOS", "Android"],
            description="Cross-platform mobile expert specializing in Flutter and high-quality UI/UX for both iOS and Android."
        ),
        Candidate(
            name="Diana Prince",
            keywords=["Unity", "C#", "Game Development", "VR", "AR", "3D Modeling"],
            description="Game developer with 5 years of experience in Unity, focusing on immersive VR/AR experiences and real-time rendering."
        ),
        Candidate(
            name="Ethan Hunt",
            keywords=["Python", "PyTorch", "AI", "Natural Language Processing", "Machine Learning"],
            description="AI Researcher with a focus on NLP and Large Language Models. Experienced in PyTorch and model optimization."
        ),
        Candidate(
            name="Fiona Gallagher",
            keywords=["Vue.js", "JavaScript", "Web Development", "CSS", "Tailwind"],
            description="Frontend engineer with a passion for modern JavaScript frameworks and creating beautiful, responsive web interfaces."
        ),
        Candidate(
            name="George Miller",
            keywords=["React Native", "JavaScript", "Mobile App Development", "Redux"],
            description="Mobile developer specialized in React Native, bridging the gap between web and mobile for rapid deployment."
        ),
        Candidate(
            name="Hannah Abbott",
            keywords=["C++", "Unreal Engine", "Game Development", "Physics Engines"],
            description="Expert game programmer focused on core engine development and physics simulation in Unreal Engine."
        ),
        Candidate(
            name="Ian Wright",
            keywords=["Python", "Django", "Web Development", "PostgreSQL", "AI"],
            description="Backend developer with a strong foundation in Django and a growing interest in integrating AI features into web apps."
        ),
        Candidate(
            name="Julia Roberts",
            keywords=["Swift", "iOS", "Mobile App Development", "SwiftUI", "Combine"],
            description="Dedicated iOS developer with a deep understanding of Swift and the Apple ecosystem, building premium native apps."
        )
    ]

    # Insert candidates
    for candidate in candidates:
        await candidate.insert()
    
    count = await Candidate.count()
    print(f"Successfully seeded {count} candidates into the database.")

if __name__ == "__main__":
    asyncio.run(seed_data())
