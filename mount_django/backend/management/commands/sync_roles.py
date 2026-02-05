from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from ...models import (
    Company,
    CompanyRole,
    Customer,
    Expense,
    Product,
    ProductCategory,
)


def perms_for_model(model, actions=("add", "view", "change", "delete")):
    """
    Build permission codenames like:
    add_customer, view_customer, change_customer, delete_customer
    and return the matching Permission queryset.
    """
    content_type = ContentType.objects.get_for_model(model)
    model_name = model._meta.model_name

    codenames = [f"{action}_{model_name}" for action in actions]

    return Permission.objects.filter(
        content_type=content_type,
        codename__in=codenames
    )


ROLE_RULES = {
    "Partner": {
        Customer: ("add", "view", "change", "delete"),
        Expense: ("add", "view", "change", "delete"),
        Product: ("add", "view", "change", "delete"),
        ProductCategory: ("add", "view", "change", "delete"),
    },
    "Manager": {
        Customer: ("add", "view", "change"),
        Expense: ("add", "view", "change"),
        Product: ("add", "view", "change"),
        ProductCategory: ("add", "view", "change"),
    },
    "Accountant": {
        Customer: ("add", "view", "change", "delete"),
        Expense: ("add", "view", "change", "delete"),
        Product: ("add", "view", "change", "delete"),
        ProductCategory: ("add", "view", "change", "delete"),
    },
    "SalesPerson": {
        Customer: ("add", "view", "change"),
        Expense: ("add", "view"),
        Product: ("view",),
        ProductCategory: ("view",),
    },
    "StockManager": {
        Product: ("add", "view", "change"),
        ProductCategory: ("view",),
    },
}


class Command(BaseCommand):
    help = "Sync company roles and permissions for all companies"

    def handle(self, *args, **options):
        companies = Company.objects.all()

        if not companies.exists():
            self.stdout.write(
                self.style.WARNING("No companies found. Nothing to sync.")
            )
            return

        for company in companies:
            self.stdout.write(
                self.style.NOTICE(f"Syncing roles for company: {company.name}")
            )

            for role_name, model_actions in ROLE_RULES.items():
                role, _ = CompanyRole.objects.get_or_create(
                    company=company,
                    name=role_name
                )

                permissions = Permission.objects.none()

                for model, actions in model_actions.items():
                    permissions |= perms_for_model(model, actions)

                role.permissions.set(permissions.distinct())

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✔ {role_name} synced"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("✅ All company roles synced successfully.")
        )
