from graphene import ObjectType, String, Int, Schema
from graphene_django import DjangoObjectType
import graphene



from .models import CustomUser, Settings
from mainapp.models import Customer
from file_storage.models import Logo


class LogoType(DjangoObjectType):
    class Meta:
        model = Logo
        

class SettingsType(DjangoObjectType):
    class Meta:
        model = Settings
        fields = (
            "id",
            "company_name",
            "company_address",
            "company_city",
            "company_state",
            "company_zip",
            "company_phone",
            "company_email",
            "company_website",
            "company_identifier",
            "company_description",
            "logo"
        )
        


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "is_staff", "customer_set")
    settings = graphene.Field(SettingsType)
    


class SettingsUpdateInput(graphene.InputObjectType):
    company_name = graphene.String()
    company_address = graphene.String()
    company_city = graphene.String()
    company_state = graphene.String()
    company_zip = graphene.String()
    company_phone = graphene.String()
    company_email = graphene.String()
    company_website = graphene.String()
    company_identifier = graphene.String()
    company_description = graphene.String()
    user_id = graphene.Int()

class UpdateSettings(graphene.Mutation):
    class Arguments:
        input = SettingsUpdateInput(required=True)

    settings = graphene.Field(SettingsType)

    @staticmethod
    def mutate(self, info, input=None):
        print("input settings",input)
        settings = Settings.objects.get(user__id=input.user_id)
        if settings :
            if "company_name" in input:
                settings.company_name = input.company_name
            if "company_address" in input:
                settings.company_address = input.company_address
            if "company_city" in input:
                settings.company_city = input.company_city
            if "company_state" in input:
                settings.company_state = input.company_state
            if "company_zip" in input:
                settings.company_zip = input.company_zip
            if "company_phone" in input:
                settings.company_phone = input.company_phone
            if "company_email" in input:
                settings.company_email = input.company_email
            if "company_website" in input:
                settings.company_website = input.company_website
            if "company_identifier" in input:
                settings.company_identifier = input.company_identifier
            if "company_description" in input:
                settings.company_description = input.company_description
            settings.save()
            return UpdateSettings(settings=settings)
        else:
            return UpdateSettings(settings=None)
        




class Query(ObjectType):
    user = graphene.Field(CustomUserType, email=String(required=True))
    settings = graphene.Field(SettingsType, user_id=Int(required=True))

    def resolve_user(root, info, email):
        return CustomUser.objects.get(email=email)

    def resolve_settings(root, info, user_id):
        return Settings.objects.get(user__id=user_id)
    
    def resolve_customer_set(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Customer.objects.all()
        else:
            return Customer.objects.none()


class Mutation(ObjectType):
    update_settings = UpdateSettings.Field()



schema = Schema(query=Query, mutation=Mutation)
