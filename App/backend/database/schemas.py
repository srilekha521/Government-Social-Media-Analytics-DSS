from pydantic import BaseModel


class SocialMediaInput(BaseModel):
    platform: str
    post_text: str
    department: str | None = None
    location: str | None = None