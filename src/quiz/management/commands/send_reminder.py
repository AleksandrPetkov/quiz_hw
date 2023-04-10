from datetime import datetime, time, timedelta

from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from prettytable import PrettyTable

from quiz.models import Result


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = make_aware(datetime.combine(timezone.now() - timedelta(7), time()))
        end = make_aware(datetime.combine(timezone.now() + timedelta(1), time()))
        results = Result.objects.filter(create_timestamp__range=(start, end), state=0).order_by('user')

        if results:
            tab_fields = ['Test', 'Start Date']
            user_results = {}
            for result in results:
                if user_results.get(result.user) is None:
                    user_results[result.user] = []
                user_results[result.user].append(
                    [result.exam.title, result.create_timestamp.strftime('%Y-%m-%d %H:%M')])

            for user, results_ in user_results.items():
                tab = PrettyTable()
                tab.field_names = tab_fields
                tab.add_rows(results_)

                subject = 'Some of your exams not finished.'
                body = f'{tab.get_string()}'
                user.email_user(subject, body)
            self.stdout.write('>>> Reminder was sent. <<<')
        else:
            self.stdout.write('>>> Nothing to send. <<<')
