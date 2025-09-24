import os
from typing import Optional

from django.core.exceptions import MultipleObjectsReturned
import numpy as np
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from apps.pages.models import Category


class Command(BaseCommand):
    """
    Custom Django script to initialize DB based ready-made Categories.
    """

    help = "Custom Django script to refresh the data entries in Task model based on CSV file."

    def add_arguments(self, parser) -> None:
        return parser.add_argument(
            "--commit",
            "-c",
            action="store_true",
            default=False,
            help="Confirm to populate Category data.",
        )

    @transaction.atomic
    def handle(self, **options) -> str | None:
        savepoint = transaction.savepoint()

        categories = [
            "Food",
            "Transportation",
            "Health",
            "Entertainment",
            "Social Life",
            "Household",
            "Education",
            "Insurance",
            "Investment",
            "Other",
        ]

        for category in categories:
            try:
                obj, _ = Category.objects.get_or_create(name=category)
            except (IntegrityError, MultipleObjectsReturned) as ex:
                self.stdout.write(
                    self.style.WARNING(f"Skipped {category}, encountered: {ex}")
                )
                continue
            else:
                self.stdout.write(
                    self.style.WARNING(f"Created new Category object in DB: {obj.name}")
                )

        if options["commit"]:
            self.stdout.write(
                self.style.SUCCESS("Successfully initialized Category in DB.")
            )
            transaction.savepoint_commit(savepoint)
        else:
            self.stdout.write(
                self.style.WARNING("Ran command without committing to DB (dry run).")
            )
            transaction.savepoint_rollback(savepoint)
