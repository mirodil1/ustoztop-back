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
            "gender": tutor.gender,
            "education": tutor.education,
            "language": tutor.language,
            "experience": tutor.experience,
        }, 200


@router.route("/tutor/update", methods=["PUT"])
@jwt_required(fresh=True)
def update_tutor():
    tutor_data = request.json
    user_id = get_jwt_identity()
    TutorService.update_tutor(user_id=user_id, **tutor_data,)
    return {"error": "no error", "detail": "Tutor updated successfully"}, 200
