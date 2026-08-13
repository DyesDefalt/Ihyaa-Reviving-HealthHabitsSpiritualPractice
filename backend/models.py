from datetime import date, datetime, timezone
from typing import Annotated, Any

from bson import ObjectId
from pydantic import (BaseModel, BeforeValidator, ConfigDict, EmailStr, Field,
                      field_validator)


def _to_str_id(v: Any) -> Any:
    if isinstance(v, ObjectId):
        return str(v)
    return v


PyObjectId = Annotated[str, BeforeValidator(_to_str_id)]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BaseDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: PyObjectId | None = Field(default=None, alias="_id")

    def to_mongo(self) -> dict:
        data = self.model_dump(by_alias=True, exclude_none=True)
        if data.get("_id") is not None:
            data["_id"] = ObjectId(data["_id"])
        else:
            data.pop("_id", None)
        return data

    @classmethod
    def from_mongo(cls, doc: dict | None):
        if doc is None:
            return None
        return cls.model_validate(doc)


# ---------- Preferences ----------

class Preferences(BaseModel):
    fitness_level: str = "beginner"           # beginner | intermediate | advanced
    health_goals: list[str] = Field(default_factory=list)
    dietary_preferences: list[str] = Field(default_factory=list)
    sleep_habit: str = "moderate"             # early_bird | moderate | night_owl
    spiritual_level: str = "beginner"         # beginner | practicing | devoted
    preferred_challenge: str = "30_days"      # 30_days | 100_days | 1_year
    reminders_enabled: bool = True


class User(BaseDocument):
    email: str
    name: str = ""
    password_hash: str | None = None
    auth_provider: str = "password"           # password | google
    picture: str | None = None
    role: str = "user"
    language: str = "en"                      # en | ar | id
    theme: str = "light"
    timezone: str = "UTC"
    onboarding_completed: bool = False
    is_pro: bool = False
    pro_until: str | None = None
    points_balance: int = 0
    lifetime_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_checkin_date: str | None = None
    prefs: Preferences = Field(default_factory=Preferences)
    created_at: datetime = Field(default_factory=utcnow)


class PublicUser(BaseModel):
    id: str
    email: str
    name: str
    picture: str | None = None
    role: str
    language: str
    theme: str
    timezone: str
    onboarding_completed: bool
    is_pro: bool
    pro_until: str | None = None
    points_balance: int
    lifetime_points: int
    current_streak: int
    longest_streak: int
    last_checkin_date: str | None = None
    prefs: Preferences

    @classmethod
    def of(cls, user: User) -> "PublicUser":
        return cls(
            id=str(user.id),
            email=user.email,
            name=user.name,
            picture=user.picture,
            role=user.role,
            language=user.language,
            theme=user.theme,
            timezone=user.timezone,
            onboarding_completed=user.onboarding_completed,
            is_pro=user.is_pro,
            pro_until=user.pro_until,
            points_balance=user.points_balance,
            lifetime_points=user.lifetime_points,
            current_streak=user.current_streak,
            longest_streak=user.longest_streak,
            last_checkin_date=user.last_checkin_date,
            prefs=user.prefs,
        )


class Challenge(BaseDocument):
    user_id: PyObjectId
    challenge_type: str = "30_days"
    status: str = "active"                    # active | paused | completed | abandoned
    start_date: str = ""
    end_date: str = ""
    total_days: int = 30
    created_at: datetime = Field(default_factory=utcnow)


class DailyTask(BaseDocument):
    user_id: PyObjectId
    challenge_id: PyObjectId
    template_key: str
    pillar: str
    day_number: int
    scheduled_date: str
    scheduled_time: str = "07:00"
    anchor: str = "anytime"
    duration_minutes: int = 5
    difficulty: int = 1
    points_reward: int = 10
    completed: bool = False
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=utcnow)


class Checkin(BaseDocument):
    user_id: PyObjectId
    challenge_id: PyObjectId | None = None
    checkin_date: str
    mood_rating: int = 3
    energy_rating: int = 3
    gratitude_note: str = ""
    reflection_note: str = ""
    tasks_completed: int = 0
    tasks_total: int = 0
    points_earned: int = 0
    created_at: datetime = Field(default_factory=utcnow)


class PointTransaction(BaseDocument):
    user_id: PyObjectId
    amount: int
    type: str = "earned"                      # earned | redeemed
    source: str = "task_complete"
    description: str = ""
    created_at: datetime = Field(default_factory=utcnow)


class CoachMessage(BaseDocument):
    user_id: PyObjectId
    role: str                                 # user | assistant
    content: str
    created_at: datetime = Field(default_factory=utcnow)


# ---------- Request bodies ----------

class RegisterBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = ""
    language: str = "en"


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class ForgotBody(BaseModel):
    email: EmailStr


class ResetBody(BaseModel):
    token: str
    password: str = Field(min_length=6)


class ProfileUpdate(BaseModel):
    name: str | None = None
    language: str | None = None
    theme: str | None = None
    timezone: str | None = None
    prefs: Preferences | None = None


class OnboardingBody(BaseModel):
    name: str | None = None
    language: str | None = None
    timezone: str | None = None
    prefs: Preferences
    start_challenge: bool = True


class StartChallengeBody(BaseModel):
    challenge_type: str = Field(default="30_days", pattern=r"^(30_days|100_days|1_year)$")
    start_date: str | None = None

    @field_validator("start_date")
    @classmethod
    def _valid_date(cls, v: str | None) -> str | None:
        if v in (None, ""):
            return None
        date.fromisoformat(v)
        return v


class CompleteTaskBody(BaseModel):
    completed: bool = True


class TaskTimeBody(BaseModel):
    scheduled_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")


class CheckinBody(BaseModel):
    mood_rating: int = Field(ge=1, le=5)
    energy_rating: int = Field(ge=1, le=5)
    gratitude_note: str = ""
    reflection_note: str = ""


class CoachBody(BaseModel):
    message: str
