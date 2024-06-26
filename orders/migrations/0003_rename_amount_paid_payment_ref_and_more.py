# Generated by Django 5.0.2 on 2024-04-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_rename_oder_number_order_order_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="amount_paid",
            new_name="ref",
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="created_at",
            new_name="timestamp",
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="payment_id",
            new_name="verified",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="payment_method",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="status",
        ),
        migrations.AddField(
            model_name="payment",
            name="amount",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="payment",
            name="email",
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
