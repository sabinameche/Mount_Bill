from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from ...models import Customer, Expense, Product, ProductCategory


def perms_for_model(model, actions=("add", "view", "change","delete")):
    """
    Build permission codenames like add_customer/view_customer/change_customer
    and return the matching Permission queryset for that model.
    """
    ct = ContentType.objects.get_for_model(model)
    model_name = model._meta.model_name  # e.g. "customer"
    codenames = [f"{action}_{model_name}" for action in actions]
    return Permission.objects.filter(content_type=ct, codename__in=codenames)


ROLE_RULES = {
    "Partner": {
        Customer: ("add", "view", "change","delete"),
        Expense: ("add", "view", "change","delete"),
        Product: ("add", "view", "change","delete"),
        ProductCategory: ("add", "view", "change","delete"),
    },
    "Manager": {
        Customer: ("add", "view", "change"),
        Expense: ("add", "view", "change"),
        Product: ("add", "view", "change"),
        ProductCategory: ("add", "view", "change"),
    },
    "Accountant": {
        Customer: ("add", "view", "change","delete"),
        Expense: ("add", "view", "change","delete"),
        Product: ("add", "view", "change","delete"),
        ProductCategory: ("add", "view", "change","delete"),
    },
    "SalesPerson": {
        Customer: ("add", "view", "change"),
        Expense: ("add", "view"),
        Product: ("view",),
        ProductCategory: ("view")
    },
    "StockManager": {
        Product: ("add", "view", "change"),
        ProductCategory: ("view"),
    },
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for role, model_actions in ROLE_RULES.items():
            group, _ = Group.objects.get_or_create(name=role)

            perms_qs = Permission.objects.none()
            for model, actions in model_actions.items():
                perms_qs |= perms_for_model(model, actions)

            # overwrite/sync exactly what is defined in ROLE_RULES
            group.permissions.set(perms_qs.distinct())

            self.stdout.write(self.style.SUCCESS(f"Synced role: {role}"))

        self.stdout.write(self.style.SUCCESS("Roles synced successfully."))