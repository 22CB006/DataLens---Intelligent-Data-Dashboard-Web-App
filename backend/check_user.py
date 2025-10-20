"""
Diagnostic script to check user credentials and password hashing
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services import user_service
from app.core.security import verify_password, get_password_hash

async def check_user():
    """Check if user exists and test password verification"""
    
    # Get database session
    async for db in get_db():
        try:
            email = "aryalakshmi2910@gmail.com"
            
            # Check if user exists
            print(f"\n🔍 Checking user: {email}")
            user = await user_service.get_user_by_email(db, email)
            
            if not user:
                print("❌ User NOT found in database!")
                print("\n💡 You need to register this user first.")
                print("   Go to: http://localhost:5173/register")
                return
            
            print(f"✅ User found!")
            print(f"   - Username: {user.username}")
            print(f"   - Email: {user.email}")
            print(f"   - Full Name: {user.full_name}")
            print(f"   - Is Active: {user.is_active}")
            print(f"   - Is Superuser: {user.is_superuser}")
            print(f"   - Hashed Password: {user.hashed_password[:50]}...")
            
            # Test password verification
            print("\n🔐 Testing password verification:")
            test_passwords = ["password123", "Password123", "test123", "admin123"]
            
            for pwd in test_passwords:
                is_valid = verify_password(pwd, user.hashed_password)
                status = "✅ MATCH" if is_valid else "❌ NO MATCH"
                print(f"   {status}: '{pwd}'")
            
            # Test authentication
            print("\n🔑 Testing authentication function:")
            for pwd in test_passwords:
                auth_user = await user_service.authenticate_user(db, email, pwd)
                if auth_user:
                    print(f"   ✅ Authentication SUCCESS with password: '{pwd}'")
                    break
            else:
                print(f"   ❌ Authentication FAILED with all test passwords")
                print(f"\n💡 Try these steps:")
                print(f"   1. Register a new account at: http://localhost:5173/register")
                print(f"   2. Or reset the password for this user")
            
        finally:
            await db.close()
            break

if __name__ == "__main__":
    asyncio.run(check_user())
