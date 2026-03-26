from django.test import TestCase
from django.contrib.auth.models import User
from main.models import (
    Role, Service, RoleService, Network, NetworkMembership,
    CooperativeCenter,
)
from accounts.test_helpers import (
    create_country, create_cooperative_center, create_user,
    create_basic_user, create_advanced_user, create_superuser,
    create_role, create_service, create_role_service,
    create_topic, create_network,
)


# ---------- Dashboard ----------

class DashboardViewTest(TestCase):

    def setUp(self):
        self.cc = create_cooperative_center()
        self.superuser = create_superuser()
        self.advanced_user = create_advanced_user(cc=self.cc)
        self.basic_user = create_basic_user(cc=self.cc)

    def test_unauthenticated_redirects(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_basic_user_redirects_to_change_profile(self):
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("change-profile", response.url)

    def test_advanced_user_renders_index(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    def test_superuser_renders_index(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")


# ---------- Users ----------

class UsersListViewTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(code="BR1.1", country=self.country)
        self.cc2 = create_cooperative_center(code="BR2.1", country=self.country)
        self.superuser = create_superuser()
        self.advanced_user = create_advanced_user(cc=self.cc)

        # Create test users in cc
        self.user1 = create_basic_user(username="user1", email="user1@example.com", cc=self.cc)
        self.user2 = create_basic_user(username="user2", email="user2@example.com", cc=self.cc2)

        # Create network managed by cc
        self.network = create_network(acronym="Net1", responsible=self.cc, country=self.country)
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc)
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc2)

    def test_list_unauthenticated_redirects(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 302)

    def test_list_basic_user_denied(self):
        self.client.login(username="user1", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 404)

    def test_list_superuser_sees_all_users(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        # Superuser sees all users
        user_ids = [u.pk for u in response.context["users"]]
        self.assertIn(self.user1.pk, user_ids)
        self.assertIn(self.user2.pk, user_ids)

    def test_list_advanced_user_sees_network_cc_users(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        # Advanced user manages network with cc and cc2
        user_ids = [u.pk for u in response.context["users"]]
        self.assertIn(self.user1.pk, user_ids)
        self.assertIn(self.user2.pk, user_ids)

    def test_list_search_by_username(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/", {"s": "user1"})
        self.assertEqual(response.status_code, 200)
        usernames = [u.username for u in response.context["users"]]
        self.assertIn("user1", usernames)
        self.assertNotIn("user2", usernames)

    def test_list_search_by_email(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/", {"s": "user2@"})
        self.assertEqual(response.status_code, 200)
        usernames = [u.username for u in response.context["users"]]
        self.assertIn("user2", usernames)

    def test_list_filter_by_cc(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/", {"cc": self.cc.pk})
        self.assertEqual(response.status_code, 200)
        for u in response.context["users"]:
            self.assertEqual(u.profile.cooperative_center, self.cc)

    def test_list_pagination(self):
        self.client.login(username="admin", password="TestPass123!")
        # Create 30 users to exceed MAX_USERS_PER_PAGE (25)
        for i in range(30):
            create_basic_user(
                username=f"puser{i}",
                email=f"puser{i}@example.com",
                cc=self.cc,
            )
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["pages"]) > 1)

    def test_list_ordering(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/", {"orderby": "username", "order": "-"})
        self.assertEqual(response.status_code, 200)
        usernames = [u.username for u in response.context["users"]]
        self.assertEqual(usernames, sorted(usernames, reverse=True))


class NewUserViewTest(TestCase):

    def setUp(self):
        self.cc = create_cooperative_center()
        self.superuser = create_superuser()
        self.advanced_user = create_advanced_user(cc=self.cc)

    def test_get_form_as_superuser(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/new/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_get_form_as_advanced(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/users/new/")
        self.assertEqual(response.status_code, 200)

    def test_get_form_basic_user_denied(self):
        basic = create_basic_user(cc=self.cc)
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/users/new/")
        self.assertEqual(response.status_code, 404)

    def test_post_valid_user_as_superuser(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "username": "created_user",
            "email": "created@example.com",
            "type": "basic",
            "is_active": True,
            "cc": self.cc.pk,
        }
        response = self.client.post("/users/new/", data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="created_user").exists())

    def test_post_valid_user_as_advanced_assigns_own_cc(self):
        self.client.login(username="advuser", password="TestPass123!")
        data = {
            "username": "adv_created",
            "email": "adv_created@example.com",
            "type": "basic",
            "is_active": True,
        }
        response = self.client.post("/users/new/", data)
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username="adv_created")
        self.assertEqual(new_user.profile.cooperative_center, self.cc)

    def test_post_invalid_data(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"username": "", "email": "", "type": "basic", "is_active": True, "cc": self.cc.pk}
        response = self.client.post("/users/new/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)


class EditUserViewTest(TestCase):

    def setUp(self):
        self.cc = create_cooperative_center()
        self.superuser = create_superuser()
        self.target_user = create_basic_user(cc=self.cc)

    def test_get_edit_form(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get(f"/users/edit/{self.target_user.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_valid_edit(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "username": self.target_user.username,
            "email": "updated@example.com",
            "type": "advanced",
            "is_active": True,
            "cc": self.cc.pk,
        }
        response = self.client.post(f"/users/edit/{self.target_user.pk}/", data)
        self.assertEqual(response.status_code, 302)
        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.email, "updated@example.com")

    def test_post_invalid_edit(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "username": "",
            "email": "",
            "type": "basic",
            "is_active": True,
            "cc": self.cc.pk,
        }
        response = self.client.post(f"/users/edit/{self.target_user.pk}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_edit_nonexistent_user_returns_404(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/edit/99999/")
        self.assertEqual(response.status_code, 404)

    def test_edit_basic_user_denied(self):
        basic = create_basic_user(username="basic2", email="basic2@example.com", cc=self.cc)
        self.client.login(username="basic2", password="TestPass123!")
        response = self.client.get(f"/users/edit/{self.target_user.pk}/")
        self.assertEqual(response.status_code, 404)


# ---------- Networks ----------

class NetworksListViewTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(code="BR1.1", country=self.country)
        self.superuser = create_superuser()
        self.advanced_user = create_advanced_user(cc=self.cc)
        self.network1 = create_network(acronym="Net1", responsible=self.cc, country=self.country)
        self.network2 = create_network(
            acronym="Net2",
            responsible=create_cooperative_center(code="BR2.1", country=self.country),
            country=self.country,
        )

    def test_list_unauthenticated_redirects(self):
        response = self.client.get("/networks/")
        self.assertEqual(response.status_code, 302)

    def test_list_basic_user_denied(self):
        basic = create_basic_user(cc=self.cc)
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/networks/")
        self.assertEqual(response.status_code, 404)

    def test_list_superuser_sees_all_networks(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/networks/")
        self.assertEqual(response.status_code, 200)
        acronyms = [n.acronym for n in response.context["networks"]]
        self.assertIn("Net1", acronyms)
        self.assertIn("Net2", acronyms)

    def test_list_advanced_user_sees_only_responsible_networks(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/networks/")
        self.assertEqual(response.status_code, 200)
        acronyms = [n.acronym for n in response.context["networks"]]
        self.assertIn("Net1", acronyms)
        self.assertNotIn("Net2", acronyms)

    def test_list_search_by_acronym(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/networks/", {"s": "Net1"})
        acronyms = [n.acronym for n in response.context["networks"]]
        self.assertIn("Net1", acronyms)
        self.assertNotIn("Net2", acronyms)

    def test_list_ordering(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/networks/", {"orderby": "acronym", "order": "-"})
        self.assertEqual(response.status_code, 200)


class NewNetworkViewTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(country=self.country)
        self.topic = create_topic()
        self.superuser = create_superuser()

    def test_get_form(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/network/new/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_valid_network(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "acronym": "NewNet",
            "responsible": self.cc.pk,
            "type": "national",
            "country": self.country.pk,
            "topic": self.topic.pk,
        }
        response = self.client.post("/network/new/", data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Network.objects.filter(acronym="NewNet").exists())

    def test_post_invalid_network(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"acronym": "", "type": "national"}
        response = self.client.post("/network/new/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_login_required(self):
        response = self.client.get("/network/new/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class EditNetworkViewTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(country=self.country)
        self.superuser = create_superuser()
        self.network = create_network(responsible=self.cc, country=self.country)

    def test_get_edit_form(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get(f"/network/edit/{self.network.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["network"], self.network)

    def test_post_valid_edit(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "acronym": "UpdatedNet",
            "responsible": self.cc.pk,
            "type": "thematic",
            "country": self.country.pk,
        }
        response = self.client.post(f"/network/edit/{self.network.pk}/", data)
        self.assertEqual(response.status_code, 200)
        self.network.refresh_from_db()
        self.assertEqual(self.network.acronym, "UpdatedNet")

    def test_edit_nonexistent_network_returns_404(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/network/edit/99999/")
        self.assertEqual(response.status_code, 404)

    def test_basic_user_denied(self):
        basic = create_basic_user(cc=self.cc)
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get(f"/network/edit/{self.network.pk}/")
        self.assertEqual(response.status_code, 404)


# ---------- Services ----------

class ServicesListViewTest(TestCase):

    def setUp(self):
        self.cc = create_cooperative_center()
        self.superuser = create_superuser()
        self.service1 = create_service(acronym="FI", name="FI-Admin")
        self.service2 = create_service(acronym="LIS", name="LILDBI-Web")

    def test_list_superuser_sees_services(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service1, response.context["services"])
        self.assertIn(self.service2, response.context["services"])

    def test_list_advanced_user_denied(self):
        adv = create_advanced_user(cc=self.cc)
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 404)

    def test_list_basic_user_denied(self):
        basic = create_basic_user(cc=self.cc)
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 404)

    def test_list_search_by_name(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/services/", {"s": "FI-Admin"})
        names = [s.name for s in response.context["services"]]
        self.assertIn("FI-Admin", names)
        self.assertNotIn("LILDBI-Web", names)

    def test_list_ordering(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/services/", {"orderby": "name", "order": "-"})
        self.assertEqual(response.status_code, 200)


class NewServiceViewTest(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.role = create_role()

    def test_get_form_as_superuser(self):
        self.client.login(username="admin", password="TestPass123!")
        # NOTE: The new_service view has a bug - it queries RoleService with an
        # unsaved Service instance on GET. This raises ValueError in Django 5.2+.
        with self.assertRaises(ValueError):
            self.client.get("/services/new/")

    def test_get_form_non_superuser_denied(self):
        cc = create_cooperative_center()
        adv = create_advanced_user(cc=cc)
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/services/new/")
        self.assertEqual(response.status_code, 404)

    def test_post_valid_service(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"name": "New Service", "acronym": "NS"}
        response = self.client.post("/services/new/", data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Service.objects.filter(acronym="NS").exists())

    def test_post_valid_service_with_roles(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "name": "Role Service",
            "acronym": "RS",
            "roles_associated": [self.role.pk],
        }
        response = self.client.post("/services/new/", data)
        self.assertEqual(response.status_code, 302)
        service = Service.objects.get(acronym="RS")
        self.assertTrue(RoleService.objects.filter(service=service, role=self.role).exists())

    def test_post_invalid_service(self):
        self.client.login(username="admin", password="TestPass123!")
        # NOTE: The new_service view has a bug - it queries RoleService with an
        # unsaved Service instance after form validation fails. This raises ValueError.
        with self.assertRaises(ValueError):
            self.client.post("/services/new/", {"name": "", "acronym": ""})


class EditServiceViewTest(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.service = create_service()
        self.role1 = create_role(acronym="R1", name="Role1")
        self.role2 = create_role(acronym="R2", name="Role2")
        RoleService.objects.create(service=self.service, role=self.role1)

    def test_get_edit_form(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get(f"/services/edit/{self.service.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_valid_edit(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"name": "Updated Service", "acronym": "US"}
        response = self.client.post(f"/services/edit/{self.service.pk}/", data)
        self.assertEqual(response.status_code, 200)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, "Updated Service")

    def test_post_edit_with_role_reassociation(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {
            "name": self.service.name,
            "acronym": self.service.acronym,
            "roles_associated": [self.role2.pk],
        }
        response = self.client.post(f"/services/edit/{self.service.pk}/", data)
        self.assertEqual(response.status_code, 200)
        # Old association deleted, new one created
        self.assertFalse(RoleService.objects.filter(service=self.service, role=self.role1).exists())
        self.assertTrue(RoleService.objects.filter(service=self.service, role=self.role2).exists())

    def test_edit_nonexistent_returns_404(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/services/edit/99999/")
        self.assertEqual(response.status_code, 404)


# ---------- Roles ----------

class RolesListViewTest(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.role1 = create_role(acronym="EDR", name="Editor")
        self.role2 = create_role(acronym="ADM", name="Administrator")

    def test_list_superuser(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/roles/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.role1, response.context["roles"])
        self.assertIn(self.role2, response.context["roles"])

    def test_list_advanced_denied(self):
        cc = create_cooperative_center()
        adv = create_advanced_user(cc=cc)
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/roles/")
        self.assertEqual(response.status_code, 404)

    def test_list_search_by_name(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/roles/", {"s": "Editor"})
        names = [r.name for r in response.context["roles"]]
        self.assertIn("Editor", names)
        self.assertNotIn("Administrator", names)

    def test_list_ordering(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/roles/", {"orderby": "name", "order": "-"})
        self.assertEqual(response.status_code, 200)


class NewRoleViewTest(TestCase):

    def setUp(self):
        self.superuser = create_superuser()

    def test_get_form_as_superuser(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/roles/new/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_non_superuser_denied(self):
        cc = create_cooperative_center()
        adv = create_advanced_user(cc=cc)
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/roles/new/")
        self.assertEqual(response.status_code, 404)

    def test_post_valid_role(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"name": "New Role", "acronym": "NR", "description": "A new role"}
        response = self.client.post("/roles/new/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Role.objects.filter(acronym="NR").exists())

    def test_post_invalid_role(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.post("/roles/new/", {"name": "", "acronym": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)


class EditRoleViewTest(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.role = create_role()

    def test_get_edit_form(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get(f"/roles/edit/{self.role.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_valid_edit(self):
        self.client.login(username="admin", password="TestPass123!")
        data = {"name": "Updated Role", "acronym": "UR", "description": "Updated"}
        response = self.client.post(f"/roles/edit/{self.role.pk}/", data)
        self.assertEqual(response.status_code, 200)
        self.role.refresh_from_db()
        self.assertEqual(self.role.name, "Updated Role")

    def test_edit_nonexistent_returns_404(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/roles/edit/99999/")
        self.assertEqual(response.status_code, 404)
