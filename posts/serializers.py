from rest_framework import serializers


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
