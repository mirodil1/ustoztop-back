import enum


class EducationDegree(enum.Enum):
    bachelor = "bachelor"
    masters = "masters"
    doctoral = "doctoral"


class LanguageLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"
    fluent = "fluent"
