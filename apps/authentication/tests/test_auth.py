import factory
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")


class UserAuthTestCase(TestCase):
    def test_account_page__when_user_is_not_authorized__should_return_302(self):
        response = self.client.get(reverse_lazy("movie:home"))
        self.assertEqual(response.status_code, 302)

    def test_account_page__when_user_is_authorized__should_return_200(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("movie:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user, response.context["user"])
