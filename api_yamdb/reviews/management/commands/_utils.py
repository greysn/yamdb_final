from ...models import (
    Category, Genre, Title, TitlesGenre, Review, User,
    Comment)


def loading(model, row):
    if model == Category:
        return Category(id=row['id'], name=row['name'], slug=row['slug'])
    if model == Genre:
        return Genre(id=row['id'], name=row['name'], slug=row['slug'])
    if model == Title:
        return Title(id=row['id'], name=row['name'], year=row['year'],
                     category_id=row['category'])
    if model == TitlesGenre:
        return TitlesGenre(id=row['id'], titles_id=row['title_id'],
                           genre_id=row['genre_id'])
    if model == Review:
        return Review(id=row['id'], title_id=row['title_id'], text=row['text'],
                      author_id=row['author'], score=row['score'],
                      pub_date=row['pub_date'])
    if model == User:
        return User(id=row['id'], username=row['username'], email=row['email'],
                    role=row['role'], bio=row['bio'],
                    first_name=row['first_name'], last_name=row['last_name'],)
    if model == Comment:
        return Comment(id=row['id'], review_id=row['review_id'],
                       text=row['text'], author_id=row['author'],
                       pub_date=row['pub_date'])
    return 'Error'
