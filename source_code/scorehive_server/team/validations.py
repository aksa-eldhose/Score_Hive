from .models import City


class TeamValidations:
    def validate_query_param(self, request):
        if request.query_params:
            if len(request.query_params) == 1 and "page" in request.query_params:
                return
            else:
                raise CustomException(
                    "Invalid query parameter. Only 'page' is allowed.", 4011
                )

    def team_data_validation(self, request):
        if request.data.get("city"):
            try:
                if not request.data.get("city").isdigit():
                    raise CustomException("city must be an Integer", 4005)
                City.objects.get(id=request.data.get("city"))
            except City.DoesNotExist:
                raise CustomException("City with this id is not available", 4007)

        if "logo_url" in request.data:
            logo_file = request.data["logo_url"]
            self.validate_logo_url(logo_file)

    def team_id_param(self, request):
        if "id" not in request.query_params or not request.query_params["id"]:
            raise CustomException("query param id is required with a value", 4008)
        elif not request.query_params.get("id").isdigit():
            raise CustomException("query param id must be an integer", 4009)

    def validate_logo_url(self, value):
        logo_file = value
        if not logo_file:
            raise CustomException("Please insert an image", 4006)
        if type(logo_file) == str:
            if logo_file == "1":
                return
            else:
                raise CustomException("invalid value for logo_url", 4006)
        allowed = ["image/jpeg", "image/png"]
        if logo_file.content_type not in allowed:
            raise CustomException("This file type is not allowed", 4017)

        if logo_file.size > 2 * 1024 * 1024:
            raise CustomException("File size should not exceed 2 MB", 4018)


class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def to_dict(self):
        return {"status_code": self.error_code, "message": self.message}
