from src.db import db
from src.models import Branch, LearningCenter, WorkingSchedule


class LearningCenterService:

    @staticmethod
    def create_center(user_id):
        learning_center = LearningCenter(user_id=user_id)
        db.session.add(learning_center)
        db.session.commit()

    @staticmethod
    def get_center_by_user_id(user_id):
        learning_center = LearningCenter.query.filter_by(user_id=user_id).first()
        if not learning_center:
            return None
        return learning_center

    @classmethod
    def update_center(cls, user_id, **learning_center_new_data):
        learning_center = cls.get_center_by_user_id(user_id=user_id)
        if not learning_center:
            return
        for key, value in learning_center_new_data.items():
            if hasattr(learning_center, key):
                setattr(learning_center, key, value)
        db.session.add(learning_center)
        db.session.commit()

    @classmethod
    def create_or_update_center_branch(cls, user_id, *branch_data):
        return cls.create_or_update_center_items(user_id, "branch", *branch_data)

    @classmethod
    def create_or_update_center_schedule(cls, user_id, *schedule_data):
        return cls.create_or_update_center_items(user_id, "working_schedule", *schedule_data)

    @classmethod
    def create_or_update_center_items(cls, user_id, item_type, *item_data):
        learning_center = cls.get_center_by_user_id(user_id=user_id)
        item_mapping = {item.id: item for item in getattr(learning_center, item_type)}

        for item in item_data:
            if "id" in item:
                # Update existing item
                existing_item = item_mapping.get(item["id"])
                if existing_item:
                    for key, value in item.items():
                        if hasattr(existing_item, key):
                            setattr(existing_item, key, value)
            else:
                # Add new item
                new_item = None
                if item_type == "branch":
                    new_item = Branch(learning_center_id=learning_center.id, **item)
                elif item_type == "working_schedule":
                    new_item = WorkingSchedule(
                        learning_center_id=learning_center.id,
                        **item,
                    )

                if new_item:
                    db.session.add(new_item)

        # Delete items
        for item_id, item in item_mapping.items():
            if item_id not in [item.get("id") for item in item_data]:
                db.session.delete(item)

        db.session.commit()
