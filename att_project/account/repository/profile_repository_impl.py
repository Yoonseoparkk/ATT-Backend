from account.entity.profile import Profile
from account.repository.profile_repository import ProfileRepository


class ProfileRepositoryImpl(ProfileRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def findByEmail(self, email):
        try:
            profile = Profile.objects.get(email=email)
            return profile
        except Profile.DoesNotExist:
            print(f"email로 profile을 찾을 수 없습니다.: {email}")
            return None
        except Exception as e:
            print(f"error occurred during email duplicate check: {e}")
            return None

