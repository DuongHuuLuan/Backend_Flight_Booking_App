from fastapi import APIRouter, Depends
from app.core.exceptions import UnauthorizedException, ConflictException
from app.core.security import create_access_token, create_refresh_token
from app.shared.dependencies import (
    get_login_usecase,
    get_register_usecase,
    get_logout_usecase,
    get_forgot_password_usecase,
    get_verify_otp_usecase,
    get_reset_password_usecase,
    get_refresh_token_usecase,
    get_me_usecase,
    get_current_user_id,
)
from app.application.use_case.auth.login_user_usecase import LoginUserUseCase, LoginUserInput
from app.application.use_case.auth.register_user_usecase import RegisterUserUseCase, RegisterUserInput
from app.application.use_case.auth.logout_user_usecase import LogoutUserUseCase
from app.application.use_case.auth.forgot_password_usecase import ForgotPasswordUseCase
from app.application.use_case.auth.verify_otp_usecase import VerifyOtpUseCase
from app.application.use_case.auth.reset_password_usecase import ResetPasswordUseCase
from app.application.use_case.auth.refresh_token_usecase import RefreshTokenUseCase
from app.application.use_case.auth.get_me_usecase import GetMeUseCase
from app.application.dto.common import BaseResponse
from app.application.dto.auth_dto import (
    LoginRequest,
    RegisterRequest,
    UserResponse,
    ForgotPasswordRequest,
    VerifyOtpRequest,
    ResetPasswordRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserMeResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    body: LoginRequest,
    uc: LoginUserUseCase = Depends(get_login_usecase),
):
    user = await uc.execute(LoginUserInput(email=body.email, password=body.password))
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(subject=user.id)
    return BaseResponse(
        data=UserResponse(
            access_token=user.id,
            accessToken=access_token,
            refresh_token=refresh_token,
            name=user.name,
            email=user.email,
            password="",
            phone=user.phone,
            country=user.country,
            city=user.city,
        ),
        message="Login successful",
        status=200,
        success=True,
    )


@router.post("/register")
async def register(
    body: RegisterRequest,
    uc: RegisterUserUseCase = Depends(get_register_usecase),
):
    try:
        user = await uc.execute(RegisterUserInput(**body.model_dump()))
    except ValueError as e:
        raise ConflictException(str(e))
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(subject=user.id)
    return BaseResponse(
        data=UserResponse(
            access_token=user.id,
            accessToken=access_token,
            refresh_token=refresh_token,
            name=user.name,
            email=user.email,
            password="",
            phone=user.phone,
            country=user.country,
            city=user.city,
        ),
        message="Registration successful",
        status=200,
        success=True,
    )


@router.post("/refresh")
async def refresh_token(
    body: RefreshTokenRequest,
    uc: RefreshTokenUseCase = Depends(get_refresh_token_usecase),
):
    user = await uc.execute(body.refresh_token)
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(subject=user.id)
    return BaseResponse(
        data=TokenResponse(
            access_token=new_access_token,
            accessToken=new_access_token,
            refresh_token=new_refresh_token,
        ),
        message="Token refreshed",
        status=200,
        success=True,
    )


@router.get("/me")
async def get_me(
    user_id: int = Depends(get_current_user_id),
    uc: GetMeUseCase = Depends(get_me_usecase),
):
    user = await uc.execute(user_id)
    return BaseResponse(
        data=UserMeResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            country=user.country,
            city=user.city,
            avatar=user.avatar,
        ),
        message="Success",
        status=200,
        success=True,
    )


@router.post("/forgot-password/sms")
async def forgot_password_sms(
    body: ForgotPasswordRequest,
    uc: ForgotPasswordUseCase = Depends(get_forgot_password_usecase),
):
    msg = await uc.execute_by_sms(body.phone or "")
    return BaseResponse(
        data={"message": msg, "nextStep": "otp", "contact": body.phone}, success=True
    )


@router.post("/forgot-password/email")
async def forgot_password_email(
    body: ForgotPasswordRequest,
    uc: ForgotPasswordUseCase = Depends(get_forgot_password_usecase),
):
    msg = await uc.execute_by_email(body.email or "")
    return BaseResponse(
        data={"message": msg, "nextStep": "otp", "contact": body.email}, success=True
    )


@router.post("/verify-otp")
async def verify_otp(
    body: VerifyOtpRequest,
    uc: VerifyOtpUseCase = Depends(get_verify_otp_usecase),
):
    msg = await uc.execute(body.email, body.phone, body.otp)
    return BaseResponse(data={"message": msg}, success=True)


@router.post("/resetPassword/sms")
async def reset_password_sms(
    body: ResetPasswordRequest,
    uc: ResetPasswordUseCase = Depends(get_reset_password_usecase),
):
    msg = await uc.execute_by_sms(body.phone or "", body.new_password)
    return BaseResponse(
        data={"message": msg, "userId": None}, success=True
    )


@router.post("/resetPassword/email")
async def reset_password_email(
    body: ResetPasswordRequest,
    uc: ResetPasswordUseCase = Depends(get_reset_password_usecase),
):
    msg = await uc.execute_by_email(body.email or "", body.new_password)
    return BaseResponse(
        data={"message": msg, "userId": None}, success=True
    )