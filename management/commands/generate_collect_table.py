from django.core.management.base import BaseCommand
from django.utils import timezone
from esusu_app.models import Contribution, Member


class Command(BaseCommand):
    help = 'Generates the collect table for a specific month'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        contributions = Contribution.objects.filter(
            created_at__month=now.month,
            created_at__year=now.year
        )
        members = Member.objects.all()

        collect_table = {}
        for member in members:
            collect_table[member.id] = {
                'username': member.username,
                'total_contributed': 0,
            }

        for contribution in contributions:
            collect_table[contribution.member.id]['total_contributed'] += contribution.amount

        collect_table = [
            {
                'username': data['username'],
                'total_contributed': data['total_contributed'],
            } for member_id, data in collect_table.items()
        ]

        # Save the collect_table to a file or database
        # ...

        self.stdout.write(self.style.SUCCESS('Collect table generated successfully'))
