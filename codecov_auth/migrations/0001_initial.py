# Generated by Django 3.1.6 on 2021-04-08 19:21

import datetime
import uuid

import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
import django.db.models.deletion
from django.conf import settings  # noqa: F401
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models

import core.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        CITextExtension(),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("email", django.contrib.postgres.fields.citext.CITextField(null=True)),
                ("name", models.TextField(null=True)),
                ("is_staff", models.BooleanField(default=False, null=True)),
                ("is_superuser", models.BooleanField(default=False, null=True)),
                (
                    "external_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Owner",
            fields=[
                ("ownerid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "service",
                    models.TextField(
                        choices=[
                            ("github", "Github"),
                            ("gitlab", "Gitlab"),
                            ("bitbucket", "Bitbucket"),
                            ("github_enterprise", "Github Enterprise"),
                            ("gitlab_enterprise", "Gitlab Enterprise"),
                            ("bitbucket_server", "Bitbucket Server"),
                        ]
                    ),
                ),
                (
                    "username",
                    django.contrib.postgres.fields.citext.CITextField(
                        null=True, unique=True
                    ),
                ),
                ("email", models.TextField(null=True)),
                ("name", models.TextField(null=True)),
                ("oauth_token", models.TextField(null=True)),
                ("stripe_customer_id", models.TextField(null=True)),
                ("stripe_subscription_id", models.TextField(null=True)),
                ("createstamp", models.DateTimeField(null=True)),
                ("service_id", models.TextField()),
                ("parent_service_id", models.TextField(null=True)),
                ("root_parent_service_id", models.TextField(null=True)),
                ("private_access", models.BooleanField(null=True)),
                ("staff", models.BooleanField(default=False, null=True)),
                ("cache", models.JSONField(null=True)),
                ("plan", models.TextField(default="users-free", null=True)),
                ("plan_provider", models.TextField(null=True)),
                ("plan_user_count", models.SmallIntegerField(default=5, null=True)),
                ("plan_auto_activate", models.BooleanField(default=True, null=True)),
                (
                    "plan_activated_users",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), null=True, size=None
                    ),
                ),
                ("did_trial", models.BooleanField(null=True)),
                ("free", models.SmallIntegerField(default=0)),
                ("invoice_details", models.TextField(null=True)),
                ("delinquent", models.BooleanField(null=True)),
                ("yaml", models.JSONField(null=True)),
                (
                    "updatestamp",
                    core.models.DateTimeWithoutTZField(default=datetime.datetime.now),
                ),
                (
                    "organizations",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), null=True, size=None
                    ),
                ),
                (
                    "admins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), null=True, size=None
                    ),
                ),
                ("integration_id", models.IntegerField(null=True)),
                (
                    "permission",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), null=True, size=None
                    ),
                ),
                ("student", models.BooleanField(default=False)),
                ("student_created_at", core.models.DateTimeWithoutTZField(null=True)),
                ("student_updated_at", core.models.DateTimeWithoutTZField(null=True)),
                (
                    "bot",
                    models.ForeignKey(
                        db_column="bot",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="codecov_auth.owner",
                    ),
                ),
            ],
            options={"db_table": "owners", "ordering": ["ownerid"]},
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("sessionid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "token",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.TextField(null=True)),
                ("useragent", models.TextField(null=True)),
                ("ip", models.TextField(null=True)),
                ("lastseen", models.DateTimeField(null=True)),
                (
                    "type",
                    models.TextField(choices=[("api", "Api"), ("login", "Login")]),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        db_column="ownerid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="codecov_auth.owner",
                    ),
                ),
            ],
            options={"db_table": "sessions", "ordering": ["-lastseen"]},
        ),
        migrations.AddConstraint(
            model_name="owner",
            constraint=models.UniqueConstraint(
                fields=("service", "username"), name="owner_service_username"
            ),
        ),
        migrations.AddConstraint(
            model_name="owner",
            constraint=models.UniqueConstraint(
                fields=("service", "service_id"), name="owner_service_ids"
            ),
        ),
    ]
