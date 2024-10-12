from src.db import db
from src.models import Experience, Language, Tutor


class TutorService:

    @staticmethod
    def create_tutor(user_id):
        tutor = Tutor(user_id=user_id)
        db.session.add(tutor)
        db.session.commit()

    @staticmethod
    def get_tutor_by_user_id(user_id):
        tutor = Tutor.query.filter_by(user_id=user_id).first()
        if not tutor:
            return None
        return tutor

    @classmethod
    def update_tutor(cls, user_id, **tutor_new_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        if tutor:
            for key, value in tutor_new_data.items():
                if hasattr(tutor, key):
                    setattr(tutor, key, value)
            db.session.add(tutor)
            db.session.commit()
        return None

    @classmethod
    def create_or_update_tutor_language(cls, user_id, *language_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        language_mapping = {language.id: language for language in tutor.language}

        for language in language_data:
            if "id" in language:
                # Update existing language
                existing_language = language_mapping.get(language["id"])
                if existing_language:
                    existing_language.name = language["name"]
                    existing_language.level = language["level"]
            else:
                # Add new language
                new_language = Language(
                    tutor_id=tutor.id,
                    name=language["name"],
                    level=language["level"],
                )
                db.session.add(new_language)

        # Delete language
        for lang_id, lang in language_mapping.items():
            if lang_id not in [language.get("id") for language in language_data]:
                db.session.delete(lang)
        db.session.commit()

    @classmethod
    def create_or_update_tutor_experience(cls, user_id, *experience_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        experience_mapping = {
            experience.id: experience for experience in tutor.experience
        }

        for experience in experience_data:
            if "id" in experience:
                # Update existing experience
                existing_experience = experience_mapping.get(experience["id"])
                if existing_experience:
                    existing_experience.organization = experience["organization"]
                    existing_experience.position = experience["position"]
                    existing_experience.start_year = experience["start_year"]
                    existing_experience.finish_year = experience["finish_year"]
            else:
                # Add new experience
                new_language = Experience(
                    tutor_id=tutor.id,
                    organization=experience["organization"],
                    position=experience["position"],
                    start_year=experience["start_year"],
                    finish_year=experience["finish_year"],
                )
                db.session.add(new_language)

        # Delete experience
        for exp_id, exp in experience_mapping.items():
            if exp_id not in [experience.get("id") for experience in experience_data]:
                db.session.delete(exp)
        db.session.commit()
