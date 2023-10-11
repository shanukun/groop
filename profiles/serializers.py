from rest_framework import serializers


class FollowUnfollowReq:
    def __init__(self, leader_id):
        self.leader_id = leader_id


class FollowUnfollowReqSerializer(serializers.Serializer):
    leader_id = serializers.IntegerField()

    def create(self, validated_data):
        return FollowUnfollowReq(**validated_data)

    def update(self, instance, validated_data):
        instance.leader_id = validated_data.get("leader_id", instance.leader_id)
        return instance
