from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src import schemas
from src.routes.v1 import router
from src.services.tutor import TutorService


@router.route("/get/tutor/<int:user_id>", methods=["GET"])
def get_tutor(user_id):
    tutor = TutorService.get_tutor_by_user_id(user_id=user_id)
    if not tutor:
        return {"error": "Not found"}, 404

    return {
            "first_name": tutor.first_name,
            "last_name": tutor.last_name,
            "gender": tutor.gender.name,
            "education": [
                {
                    "id": education.id,
                    "name": education.name,
                    "degree": education.degree.name,
                    "start_year": education.start_year,
                    "finish_year": education.finish_year,
                }
                for education in tutor.education
            ],
            "language": [
                {
                    "id": language.id,
                    "name": language.name,
                    "level": language.level.name,
                }
                for language in tutor.language
            ],
            "experience": [
                {
                    "id": experience.id,
                    "organization": experience.organization,
                    "position": experience.position,
                    "start_year": experience.start_year,
                    "finish_year": experience.finish_year,
                    "is_working": experience.is_working,
                }
                for experience in tutor.experience
            ],
        }, 200


@router.route("/tutor/update", methods=["PUT"])
@jwt_required(fresh=True)
def update_tutor():
    tutor_data = request.json
    user_id = get_jwt_identity()

    TutorService.update_tutor(user_id=user_id, **tutor_data)
    return {"error": "no error", "detail": "Tutor updated successfully"}, 200


@router.route("/tutor/language/update/", methods=["PUT"])
@jwt_required(fresh=True)
def update_tutor_language():
    language_data = request.json
    user_id = get_jwt_identity()

    TutorService.create_or_update_tutor_language(user_id, *language_data)
    return {"error": "no error", "detail": "Language updated successfully"}, 200


@router.route("/tutor/experience/update/", methods=["PUT"])
@jwt_required(fresh=True)
def update_tutor_experience():
    experience_data = request.json
    user_id = get_jwt_identity()

    TutorService.create_or_update_tutor_experience(user_id, *experience_data)
    return {"error": "no error", "detail": "Experience updated successfully"}, 200


@router.route("/tutor/education/update/", methods=["PUT"])
@jwt_required(fresh=True)
def update_tutor_education():
    education_data = request.json
    user_id = get_jwt_identity()

    TutorService.create_or_update_tutor_education(user_id, *education_data)
    return {"error": "no error", "detail": "Education updated successfully"}, 200
