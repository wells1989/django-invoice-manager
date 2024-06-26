# Generated by Django 5.0.4 on 2024-05-10 10:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0006_invoice_client_address_invoice_client_contact_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="freelancer",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="invoice.freelancer",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="history",
            name="invoice",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="invoice.invoice",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="invoice",
            name="been_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="invoice",
            name="client",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="invoice.client",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="invoice",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="invoice",
            name="freelancer",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="invoice.freelancer",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="invoice",
            name="month_ending",
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name="invoice",
            name="recurring",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="invoice",
            name="services",
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="total_charge",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="total_hours",
            field=models.IntegerField(null=True),
        ),
    ]
