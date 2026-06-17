from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: str
    country: str
    city: str
    password: str


class UserResponse(BaseModel):
    access_token: int        
    accessToken: str         
    name: str
    email: str
    password: str
    phone: str
    country: str
    city: str


class ForgotPasswordRequest(BaseModel):
    email: str | None = None
    phone: str | None = None


class VerifyOtpRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    otp: str


class ResetPasswordRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    new_password: str