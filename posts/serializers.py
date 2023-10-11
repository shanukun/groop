from rest_framework import serializers


class PostAction:
    def __init__(self, post_id):
        self.post_id = post_id


class PostActionSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    def create(self, validated_data):
        return PostAction(**validated_data)

    def update(self, instance, validated_data):
        instance.post_id = validated_data.get("post_id", instance.post_id)
        return instance


class Post:
    def __init__(self, body, image):
        self.body = body
        self.image = image


class PostSerializer(serializers.Serializer):
    body = serializers.CharField(allow_null=True)
    image = serializers.ImageField(allow_null=True)

    def create(self, validated_data):
        return Post(**validated_data)


class Comment:
    def __init__(self, body, post_id):
        self.body = body
        self.post_id = post_id


class CommentSerializer(serializers.Serializer):
    body = serializers.CharField()
    post_id = serializers.IntegerField()

    def create(self, validated_data):
        return Comment(**validated_data)


class CommentAction:
    def __init__(self, comment_id):
        self.comment_id = comment_id


class CommentActionSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()

    def create(self, validated_data):
        return CommentAction(**validated_data)

    def update(self, instance, validated_data):
        instance.comment_id = validated_data.get("comment_id", instance.comment_id)
        return instance
