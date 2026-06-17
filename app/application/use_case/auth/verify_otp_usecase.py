from dataclasses import dataclass


class VerifyOtpUseCase:
    async def execute(self, email: str | None, phone: str | None, otp: str) -> str:
        # Tạm thời: luôn thành công nếu OTP = "4444" 
        if otp == "4444":
            return "OTP verified"
        raise ValueError("Invalid OTP")