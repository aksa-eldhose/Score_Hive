import datetime
import logging
import os
import re

import jwt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from group.validations import CustomException
from scorehive_server.common import custom_errors
from team.models import Team
from team_players.models import TeamPlayers

from .models import User
from .serializers import UserDetailsUpdateSerializer, UserRegisterSerializer

# Create your views here.

load_dotenv()
logger = logging.getLogger(__name__)


class RegisterUser(APIView):
    authentication_classes = []

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        validator = EmailValidator()
        if "email" not in request.data:
            logger.error({"message": "Email is required"})
            return Response(
                {"error_code": 1002, "message": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.data["email"]
        try:
            User.objects.get(email=email)
            logger.error({"message": "User with this email already exist"})
            return Response(custom_errors.USER_ALREADY_EXISTS, status=409)
        except ObjectDoesNotExist:
            if len(email) > 100:
                logger.error(
                    {
                        "error_code": 1003,
                        "message": "Maximum length of email should be 100 characters",
                    }
                )
                return Response(
                    {
                        "error_code": 1003,
                        "message": "Maximum length of email should be 100 characters",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                validator(email)
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
                    "iat": datetime.datetime.now(),
                    "purpose": "email_verification_token",
                }
                token = jwt.encode(
                    payload,
                    os.environ.get("EMAIL_VERIFICATION_SECRET"),
                    algorithm="HS256",
                )
                link = (
                    os.environ.get("UI_BASE_URL")
                    + "/register-email-response/"
                    + token
                    + "/"
                )
                context = {"verification_link": link}
                template = "email_verification_mail_template.html"
                email_content = render_to_string(template, context)
                email = EmailMessage("Register your email", email_content, to=[email])
                email.content_subtype = "html"
                try:
                    if os.environ.get("EMAIL_SERVICES_ACTIVE") == "True":
                        email.send()
                    logger.info({"message": "Verification link sent"})
                    return Response(
                        {"message": "Verification link sent"}, status=status.HTTP_200_OK
                    )
                except Exception as e:
                    logger.error({"message": "Verification link sending failed"})
                    logger.exception(e)
                    return Response(
                        {
                            "error_code": 3001,
                            "message": "Verification link sending failed",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except ValidationError:
                logger.info({"message": "Enter a valid email"})
                return Response(
                    {"error_code": 1004, "message": "Enter a valid email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class EmailVerify(APIView):
    authentication_classes = []

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        if "token" not in request.data:
            logger.error({"message": "Token is needed to pass in request body"})
            return Response(
                {
                    "error_code": 1005,
                    "message": "Token is needed to pass in request body",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = request.data["token"]
        try:
            payload = jwt.decode(
                token, os.environ.get("EMAIL_VERIFICATION_SECRET"), algorithms=["HS256"]
            )
            if payload["purpose"] != "email_verification_token":
                return Response(
                    {"message": "Verification link invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            payload["purpose"] = "email_verification_response_token"
            token = jwt.encode(
                payload, os.environ.get("EMAIL_VERIFICATION_SECRET"), algorithm="HS256"
            )
            logger.info({"message": "Success"})
            return Response({"email_token": token}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as es:
            logger.exception(es)
            return Response(
                {"error_code": 1007, "message": "Verification link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.exception(e)
            return Response(
                {"error_code": 1006, "message": "Verification link invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class UserRegister(APIView):
    authentication_classes = []
    serializer_class = UserRegisterSerializer
    required_keys = ["token", "name", "phone_number", "password", "confirm_password"]

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        team_id = None
        try:
            email_verified_token = request.data["token"]
            try:
                payload = jwt.decode(
                    email_verified_token,
                    os.environ.get("EMAIL_VERIFICATION_SECRET"),
                    algorithms=["HS256"],
                )
                if payload["purpose"] != "email_verification_response_token":
                    logger.error(custom_errors.ERR_1008)
                    return Response(
                        custom_errors.ERR_1008,
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
                request.data.pop("token")
                request.data["email"] = payload["email"]
                team_id = payload.get("team_id", None)
            except Exception:
                logger.error(custom_errors.ERR_1008)
                return Response(
                    custom_errors.ERR_1008,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            user = User.objects.get(email=payload["email"])
            logger.error({"message": "User with this email already exist"})
            return Response(custom_errors.USER_ALREADY_EXISTS, status=409)
        except Exception:
            serialized_data = self.serializer_class(data=request.data)
            return self.process_valid_data(request, serialized_data, team_id)

    def process_valid_data(self, request, serialized_data, team_id):
        if serialized_data.is_valid():
            if (
                serialized_data.validated_data["password"]
                != request.data["confirm_password"]
            ):
                logger.error(
                    {
                        "message": {
                            "confirm_password": "Password and Confirm password should match"
                        }
                    }
                )
                return Response(
                    {
                        "error_code": 1008,
                        "message": {
                            "confirm_password": "Password and Confirm password should match"
                        },
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            serialized_data.validated_data["password"] = make_password(
                serialized_data.validated_data["password"]
            )
            if team_id is None:
                serialized_data.save()
                logger.info({"message": "User registration success"})
                return Response(
                    {"message": "User registration success"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return self.add_to_team(request, serialized_data, team_id)
        else:
            logger.error({"message": serialized_data.errors})
            return Response(
                {"error_code": 1008, "message": serialized_data.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def add_to_team(self, request, serialized_data, team_id):
        try:
            team = Team.objects.get(id=team_id)
            user = serialized_data.save()
            try:
                TeamPlayers.objects.get(team_id=team.id, player_id=user.id, status=1)
                logger.error({"message": "User is already member of the team"})
                return Response(
                    {
                        "error_code": 1027,
                        "message": "User is already member of the team",
                    },
                    status=409,
                )
            except ObjectDoesNotExist:
                try:
                    deleted_player = TeamPlayers.objects.get_deleted_row(
                        team_id=team_id, player_id=request.user.pk, status=0
                    )
                    deleted_player.status = 1
                    deleted_player.save()
                except ObjectDoesNotExist:
                    new_team_player = TeamPlayers(team_id=team, player_id=user)
                    new_team_player.save()
                logger.info(
                    {"message": "Player registration success and  player added to team"}
                )
                return Response(
                    {
                        "message": "Player registration success and  player added to team"
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except ObjectDoesNotExist:
            logger.error({"message": "Team not found"})
            return Response(
                {"error_code": 4012, "message": "Team not found"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class Login(APIView):
    required_keys = ["email", "password"]
    authentication_classes = []

    def post(self, request):
        logger.info(request)
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=request.data["email"], status=1, is_active=1)
            print(user.id)
            if check_password(request.data["password"], user.password):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "Refresh_Token": str(refresh),
                        "Access_Token": str(refresh.access_token),
                        "name": user.name,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                logger.error(custom_errors.ERR_1009)
                return Response(
                    custom_errors.ERR_1009,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ObjectDoesNotExist:
            logger.error(custom_errors.ERR_1009)
            return Response(
                custom_errors.ERR_1009,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAccountPasswordReset(APIView):
    authentication_classes = []

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        if "email" not in request.data:
            logger.error({"message": "Email is needed to pass in request body"})
            return Response(
                {
                    "error_code": 1010,
                    "message": "Email is needed to pass in request body",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=request.data["email"], status=1, is_active=1)
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = (
                os.environ.get("UI_BASE_URL")
                + "/verify_ResetPassword/"
                + uidb64
                + "/"
                + token
                + "/"
            )
            context = {"reset_link": link}
            template = "password_reset_mail_template.html"
            email_content = render_to_string(template, context)
            email = EmailMessage(
                "Reset Password", email_content, to=[request.data["email"]]
            )
            email.content_subtype = "html"
            if os.environ.get("EMAIL_SERVICES_ACTIVE") == "True":
                email.send()
            logger.info({"message": "Password reset link sent"})
            return Response(
                {"message": "Password reset link sent"}, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            logger.error(
                {"message": "No user account found associated with the given mail"}
            )
            return Response(
                custom_errors.USER_DOESNOT_EXISTS, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(e)
            logger.error({"message": "Password reset link sending failed"})
            return Response(
                {"error_code": 3001, "message": "Password reset link sending failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetTokenVerification(APIView):
    authentication_classes = []

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        if "user_id" not in request.data or "token" not in request.data:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data["user_id"].isspace():
            logger.error({"message": "Invalid User id"})
            return Response(
                {"error_code": 1011, "message": "Invalid User id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(request.data["user_id"]) == 0:
            logger.error({"message": "User id is required"})
            return Response(
                {"error_code": 1012, "message": "User id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user_id = force_str(urlsafe_base64_decode(request.data["user_id"]))
            token = request.data["token"]
            user = User.objects.get(pk=user_id)
            if user and PasswordResetTokenGenerator().check_token(user, token):
                return Response({"email": user.email}, status=status.HTTP_200_OK)
            else:
                logger.error(
                    {"message": "Invalid/Expired/Already used password reset token"}
                )
                return Response(
                    {
                        "error_code": 1013,
                        "message": "Invalid/Expired/Already used password reset token",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.exception(e)
            logger.error({"message": "Invalid password reset token"})
            return Response(
                {"error_code": 1014, "message": "Invalid password reset token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordUpdate(APIView):
    required_keys = ["email", "password", "confirm_password"]
    authentication_classes = []
    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if request.data["email"] == "":
            logger.error({"message": "Please verify your email first"})
            return Response(
                {"error_code": 1015, "message": "Please verify your email first"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        try:
            user = User.objects.get(email=request.data["email"], status=1, is_active=1)
            password = request.data["password"]
            pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]).{8,20}$"
            if re.match(pattern, password):
                if request.data["password"] == request.data["confirm_password"]:
                    user.password = make_password(request.data["password"])
                    user.save()
                    return Response(
                        {"message": "Password updated successfully"},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    logger.error(
                        {"message": "Password and confirm password should match"}
                    )
                    return Response(
                        {
                            "error_code": 1017,
                            "message": "Password and confirm password should match",
                        },
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
            else:
                logger.error({"message": "Invalid password"})
                return Response(
                    {"error_code": 1016, "message": "Invalid password"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except Exception:
            logger.error({"message": "User with the given email doesn't exist"})
            return Response(
                custom_errors.USER_DOESNOT_EXISTS,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class EditProfile(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer = UserDetailsUpdateSerializer

    def get(self, request):
        logger.info(request)
        logger.info(request.data)
        try:
            return Response(
                {"Name": request.user.name, "Phone_Number": request.user.phone_number},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        logger.info(request)
        logger.info(request.data)
        if not bool(request.data):
            logger.error({"message": "No data provided to update"})
            return Response(
                {"error_code": 1018, "message": "No data provided to update"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            serialized_data = self.serializer(
                request.user, data=request.data, partial=True
            )
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(
                    {"message": "User details updated"}, status=status.HTTP_200_OK
                )
            else:
                logger.error({"message": serialized_data.errors})
                return Response(
                    {"error_code": 1019, "message": serialized_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.exception(e)
            logger.error({"message": "Update failed"})
            return Response(
                {"error_code": 1028, "message": "Update failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePassword(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["current_password", "new_password", "confirm_password"]

    def patch(self, request):
        logger.info(request)
        logger.info(request.data)
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if check_password(request.data["current_password"], request.user.password):
                new_password = request.data["new_password"]
                if check_password(new_password, request.user.password):
                    return Response(
                        {
                            "error_code": 1021,
                            "message": "Current password and new password are same. Please give a different password",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]).{8,20}$"
                if re.match(pattern, new_password):
                    if request.data["new_password"] == request.data["confirm_password"]:
                        request.user.password = make_password(
                            request.data["new_password"]
                        )
                        request.user.save()
                        return Response(
                            {"message": "Password updated successfully"},
                            status=status.HTTP_200_OK,
                        )
                    else:
                        logger.error(
                            {
                                "message": "New password and confirm passwords should match"
                            }
                        )
                        return Response(
                            {
                                "error_code": 1017,
                                "message": "New password and confirm passwords should match",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    logger.error({"message": "New password entered is not strong"})
                    return Response(
                        {
                            "error_code": 1022,
                            "message": "New password entered is not strong",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                logger.error({"message": "Current password incorrect"})
                return Response(
                    {"error_code": 1020, "message": "Current password incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.exception(e)
            logger.error({"message": "Password updation failed"})
            return Response(
                {"error_code": 1024, "message": "Password updation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckCurrentPassword(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        if (
            "current_password" not in request.data
            or request.data["current_password"] == ""
        ):
            return Response(
                {"error_code": 1029, "message": "current_password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if check_password(request.data["current_password"], request.user.password):
            return Response(
                {"message": "current_password is correct"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error_code": 1030, "message": "current_password incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
