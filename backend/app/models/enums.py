import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

class DifficultyLevel(str, enum.Enum):
    NOVICE = "novice"
    AMATEUR = "amateur"
    INITIATE = "initiate"
    PROFESSIONAL = "professional"
    EXPERT = "expert"
    
    @property
    def points(self):
        points_map = {
            DifficultyLevel.NOVICE: 0.5,
            DifficultyLevel.AMATEUR: 1.0,
            DifficultyLevel.INITIATE: 2.0,
            DifficultyLevel.PROFESSIONAL: 3.5,
            DifficultyLevel.EXPERT: 5.5
        }
        return points_map[self]

class AssessmentStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class ReportType(str, enum.Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    CERTIFICATE = "certificate"
