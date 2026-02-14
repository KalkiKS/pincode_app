from app.models.pincode_model import PincodeModel


class ValidateLocation:

    @staticmethod
    def validate_state(query: str):
        """ Validate if the provided state exists in the database."""
        result = PincodeModel.collection().find_one({"state": query})

        if not result:
            return False
        return True

    @staticmethod
    def validate_district(query: str):
        """ Validate if the provided district exists in the database."""
        result = PincodeModel.collection().find_one({"district": query})

        if not result:
            return False
        return True

    @staticmethod
    def validate_postoffice(query: str):
        """ Validate if the provided post office exists in the database."""
        result = PincodeModel.collection().find({"postoffices.name": query})

        if not result:
            return False
        return True