from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation
import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

BAD_MARKS = [2, 3]
MAX_MARK = 5
COMMENDATION_TEXTS = ['Хвалю!', 'Молодец!', 'Так держать!', 'Талантливо!', 'Ты меня приятно удивил!']


def get_schoolkid(schoolkid_full_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    except ObjectDoesNotExist:
        print('There is less than one student with this name')
    except MultipleObjectsReturned:
        print('There is more than one student with this name')


def fix_marks(schoolkid_full_name):
    schoolkid = get_schoolkid(schoolkid_full_name)
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__in=BAD_MARKS).update(points=MAX_MARK)


def remove_chastisements(schoolkid_full_name):
    schoolkid = get_schoolkid(schoolkid_full_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_full_name, subject_title):
    schoolkid = get_schoolkid(schoolkid_full_name)
    if not schoolkid:
        return

    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title,
    )

    lesson = random.choice(lessons)
    if not lesson:
        print('There is no lessons with this student')
        return

    Commendation.objects.create(
        text=random.choice(COMMENDATION_TEXTS),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
