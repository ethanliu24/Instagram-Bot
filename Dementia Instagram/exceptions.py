""" exceptions.py
Creators: Ethan Liu
Date Created: 2024-06-05
Last Modified: 2024-06-05

This file has the potential errors that could be made when sending url
requests. Keep in mind they are only general errors, no detailed errors are
provided.

I've chosen to do it this way because I don't know how to do it better.
"""


class ContainerCreationError(Exception):
    """ Something went wrong while creating media container """
    def __str__(self) -> str:
        return "Something went wrong while creating media container"


class PublishError(Exception):
    """ Something went wrong while publishing media post """
    def __str__(self) -> str:
        return "Something went wrong while publishing media post"


class UserLongTokenError(Exception):
    """ Something went wrong when generating USER long token """
    def __str__(self) -> str:
        return "Something went wrong when generating USER long token error"


class PageLongTokenError(Exception):
    """ Something went wrong when generating PAGE long token """
    def __str__(self) -> str:
        return "Something went wrong when generating PAGE long token error"
