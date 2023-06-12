import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class DatabaseService:
    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance
    
    def setup_database(self):
        CRED = "./website/api/key.json"
        DATABASE_URL = "https://bmi-calculating-device-default-rtdb.asia-southeast1.firebasedatabase.app/"

        cred = credentials.Certificate(CRED)

        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })

        self.db = db

    def get_data_with_lrn(self, lrn):
        user_info = {}
        primary_ref = self.db.reference("").get()

        for primary_key in primary_ref.keys():
            secondary_ref = self.db.reference(primary_key).get()
            for secondary_key in secondary_ref.keys():
                tertiary_ref = self.db.reference(
                    f"/{primary_key}/{secondary_key}").get()
                for tertiary_key in tertiary_ref.keys():
                    fourth_ref = self.db.reference(
                        f"/{primary_key}/{secondary_key}/{tertiary_key}").get()
                    for _lrn in fourth_ref.keys():
                        if _lrn == lrn:
                            user_ref = self.db.reference(
                                f"/{primary_key}/{secondary_key}/{tertiary_key}/{lrn}").get()
                            user_info[primary_key] = user_ref

        return user_info

    # for development only
    def delete_all(self):
        _ref = self.db.reference("/")
        _ref.delete()


if __name__ == "__main__":
    service = DatabaseService()
    service.setup_database()
    service.get_data_with_lrn("4021020150721")
