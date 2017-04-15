"""
    Useful game utility functions for common actions
"""

from api.models import Game, PlayerInstance, StealAttempt
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


def get_valid_game(game_id: int) -> Game:
    game = Game.objects.filter(id=game_id).all()
    if len(game) == 0:
        raise ValidationError('Invalid game_id')
    return game[0]


def get_valid_game_with_status(game_id: int, status: Game.Status) -> Game:
    game = Game.objects.filter(id=game_id, status=status).all()
    if len(game) == 0:
        raise ValidationError('Invalid game_id')
    return game[0]


def get_valid_player_instance(
        game: Game, player_instance_id: int, error_message='Invalid player_instance_id'
) -> PlayerInstance:
    pi = PlayerInstance.objects.filter(game=game, id=player_instance_id).all()
    if len(pi) == 0:
        raise ValidationError(error_message)
    return pi[0]


def get_valid_player_instance_from_user(
        game: Game, user: User, error_message='Invalid player'
) -> PlayerInstance:
    pi = PlayerInstance.objects.filter(game=game, player__user=user).all()
    if len(pi) == 0:
        raise ValidationError(error_message)
    return pi[0]


def get_valid_steal_attempt(
        steal_attempt_id: int, status: StealAttempt.Status, error_message='Invalid player'
) -> StealAttempt:
    attempt = StealAttempt.objects.filter(id=steal_attempt_id, status=status).all()
    if len(attempt) == 0:
        raise ValidationError(error_message)
    return attempt[0]


def finalize_steal_attempt(attempt: StealAttempt):
    attempt.status = StealAttempt.Status.COMPLETE
    attempt.completed_at = timezone.now()

    successful_steal = attempt.coins_stolen > 0

    if successful_steal:
        # Exchange coins
        attempt.thief.coins += attempt.coins_stolen
        attempt.thief.save()
        attempt.victim.coins -= attempt.coins_stolen
        attempt.victim.save()

    # TODO send notification to players with result
