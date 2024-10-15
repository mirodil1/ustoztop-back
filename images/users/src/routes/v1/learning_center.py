from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src import schemas
from src.routes.v1 import router
from src.services.learning_center import LearningCenterService


@router.route("/get/center/<int:user_id>", methods=["GET"])
def get_center(user_id):
    learning_center = LearningCenterService.get_center_by_user_id(user_id=user_id)
    if not learning_center:
        return {"error": "Not found"}, 404

    return {
        "name": learning_center.name,
        "description": learning_center.description,
        "branches": [
            {
                "id": branch.id,
                "name": branch.name,
            } for branch in learning_center.branch
        ],
        "schedule": [
            {
                "id": schedule.id,
                "day_of_week": schedule.day_of_week.name,
                "opening_time": schedule.opening_time.strftime("%H:%M"),
                "closing_time": schedule.closing_time.strftime("%H:%M"),
                "is_closed": schedule.is_closed,
            } for schedule in learning_center.working_schedule
        ],
    }, 200


@router.route("/center/update", methods=["PUT"])
@jwt_required(fresh=True)
def update_center():
    center_data = request.json
    user_id = get_jwt_identity()

    LearningCenterService.update_center(user_id=user_id, **center_data)
    return {"error": "no error", "detail": "Learning center updated successfully"}, 200


@router.route("/center/branch/update/", methods=["PUT"])
@jwt_required(fresh=True)
def update_center_branch():
    branch_data = request.json
    user_id = get_jwt_identity()

    LearningCenterService.create_or_update_center_branch(user_id, *branch_data)
    return {"error": "no error", "detail": "Branch updated successfully"}, 200


@router.route("/center/schedule/update/", methods=["PUT"])
@jwt_required(fresh=True)
def update_center_schedule():
    schedule_data = request.json
    user_id = get_jwt_identity()

    LearningCenterService.create_or_update_center_schedule(user_id, *schedule_data)
    return {"error": "no error", "detail": "Working schedule updated successfully"}, 200
