import uuid
from datetime import datetime, timedelta
from peewee import (
    CharField,
    DateTimeField,
    IntegerField,
    Model,
    UUIDField,
)
from playhouse import db_url
from itsdangerous import BadData, URLSafeSerializer
from . import settings


class TokenField:

    def __init__(self, field: UUIDField):
        self.field = field
        self.serializer = URLSafeSerializer(settings.SECRET_KEY)

    def __eq__(self, token):
        try:
            key = self.serializer.loads(token)
        except BadData:
            return False
        return self.field == key

    def __get__(self, instance, owner):
        if instance:
            return self.serializer.dumps(getattr(instance, self.field.name).hex)
        return self


class Secret(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    data = CharField()
    expiration = DateTimeField()
    reads = IntegerField()
    token = TokenField(id)

    def serialize(self):
        return {
            'data': self.data,
            'expiration': (self.expiration - datetime.now()).seconds // 3600,
            'reads': self.reads,
        }

    @classmethod
    def deserialize(cls, data):
        secret = Secret(
            data=data.get('data'),
            expiration=datetime.now() + timedelta(hours=int(data.get('expiration'))),
            reads=data.get('reads'),
        )
        secret.validate()
        return secret

    def validate(self):
        if not all((
            0 < len(self.data) <= settings.MAX_DATA_LENGTH,
            self.expiration <= datetime.now() + timedelta(hours=settings.MAX_EXPIRATION),
            0 < int(self.reads) <= settings.MAX_READS,
        )):
            raise ValueError()

    class Meta:
        database = db_url.connect(settings.DATABASE_URL)


Secret._meta.database.create_tables([Secret])
