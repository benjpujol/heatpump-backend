from graphene import ObjectType, String, Int, Schema
from graphene_django import DjangoObjectType
import graphene



from .models import CustomUser, Settings



class SettingsType(DjangoObjectType):
    class Meta:
        model = Settings
        fields = (
            "id",
            "logo",
            "company_name",
            "company_address",
            "company_city",
            "company_state",
            "company_zip",
            "company_phone",
            "company_email",
            "company_website",
            "company_identifier"
        )


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "is_staff")
    settings = graphene.Field(SettingsType)



class Query(ObjectType):
    user = graphene.Field(CustomUserType, email=String(required=True))
    settings = graphene.Field(SettingsType, user_id=Int(required=True))

    def resolve_user(root, info, email):
        return CustomUser.objects.get(email=email)

    def resolve_settings(root, info, user_id):
        return Settings.objects.get(user__id=user_id)


class Mutation(ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
