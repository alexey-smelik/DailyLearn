from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )


class LearningCardNotFound(HTTPException):
    def __init__(self, card_id: object) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LearningCard {card_id} not found",
        )


class NewsletterNotFound(HTTPException):
    def __init__(self, newsletter_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Newsletter {newsletter_id} not found",
        )


class GroupNotFound(HTTPException):
    def __init__(self, group_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group {group_id} not found",
        )
