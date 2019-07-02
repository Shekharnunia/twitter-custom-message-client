# Generated by Django 2.2.2 on 2019-07-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_auto_20190702_1338'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FollowerDetail',
        ),
        migrations.AlterModelOptions(
            name='followers',
            options={'verbose_name': 'Follower', 'verbose_name_plural': 'Followers'},
        ),
        migrations.AddField(
            model_name='searchkeywords',
            name='since_id',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
