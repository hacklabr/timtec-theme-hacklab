# -*- coding: utf-8 -*-
import json
import urllib2
import logging
from os import path
from random import random
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from activities.models import Answer
from timtec_theme_hacklab.models import AnswerNotification, UnreadNotification
from settings import *

logger = logging.getLogger(__package__)


@receiver(post_save, sender=Answer)
def answer_created_or_updated(instance, **kwargz):

    # All instructors of the corresponding course must be notified
    notifiable_users = instance.activity.unit.lesson.course.professors
    try:
        topic_id = instance.given.get('topic', None)
    except AttributeError:
        topic_id = None

    # If this answer is not relative to a Discussion Activity, this signal must not notify professors
    if topic_id is None:
        return

    # Create the New Topic notification for appropriate users
    for user in notifiable_users.all():
        try:
            notification = AnswerNotification.objects.get(
                user=user,
                topic_id=topic_id,
                activity=instance.activity
            )
        except AnswerNotification.DoesNotExist:
            notification = AnswerNotification.objects.create(
                user=user,
                topic_id=topic_id,
                activity=instance.activity
            )

        notification.action = 'new_activity'
        notification.is_read = False
        notification.save()

        # Increase the unread count for this user in 1
        # But only if the user already has a UnreadNotification instance
        try:
            unread = UnreadNotification.objects.get(user=user)
            unread.counter += 1
            unread.save()
        except UnreadNotification.DoesNotExist:
            pass


@receiver(post_save, sender=get_user_model())
def rc_create_user(sender, **kwargz):
    user = kwargz.get('instance')
    new = kwargz.get('created')

    if not new:
        return

    url = path.join(API, 'users.create')
    data = json.dumps({
        'name'    : user.get_full_name() or user.username,
        'email'   : user.email,
        'password': '%d%f' % (user.id, random()),
        'username': user.username,
        'verified': True,
    })

    headers = {'Content-Length': len(data)}
    headers.update(HEADERS)

    try:
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        logger.info('Created on RocketChat: %s' % response.read())
    except (urllib2.URLError, urllib2.HTTPError) as e:
        logger.error(e)
