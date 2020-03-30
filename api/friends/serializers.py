from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from friends.models import Friend

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    '''
    This serializer should only be used for actions taken by the internal program of the server.
    Do NOT pass the user's data DIRECTLY into this serializer, since this serializer has neither 
    read_only_fields nor any advanced validator.
    '''
    class Meta:
        model = Friend
        fields = ('id', 'followee_id', 'followee_host', 'followee_name', 'followee_url', 'follower_id', 
                  'follower_host', 'follower_name', 'follower_url', 'mutual', 'not_read')

        validators = [
            UniqueTogetherValidator(
                queryset=Friend.objects.all(),
                fields=['followee_id', 'follower_id']
            )
        ]

    def validate(self, data):
        """
        If "followee" and "follower" fields are provided (may not be provided if action is update), 
        enforce followee field and follower field have different values.
        """
        if 'followee_id' in data.keys() and 'follower_id' in data.keys() and data['followee_id'] == data['follower_id']:
            raise serializers.ValidationError("followee and follower should not be same")
        return data

    # def create(self, validated_data):
    #     print(validated_data)
    #     return Friend(**validated_data)

class FriendReadOnlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'followee_id', 'followee_host', 'followee_name', 'followee_url', 'follower_id', 
                  'follower_host', 'follower_name', 'follower_url', 'mutual', 'not_read')
        read_only_fields = ('followee_id', 'followee_host', 'followee_name', 'followee_url', 'follower_id', 
                            'follower_host', 'followee_name', 'followee_url', 'mutual', 'not_read')

class FriendfollowerSerializer(serializers.HyperlinkedModelSerializer):
    '''
    This serializer should only be used to create a new friendship event by the follower.
    Do NOT use this serializer for update.
    '''
    class Meta:
        model = Friend
        fields = ('id', 'followee_id', 'followee_host', 'followee_name', 'followee_url', 'follower_id', 
                  'follower_host', 'follower_name', 'follower_url', 'mutual', 'not_read')
        read_only_fields = ('mutual', 'not_read')

        validators = [
            UniqueTogetherValidator(
                queryset=Friend.objects.all(),
                fields=['followee_id', 'follower_id']
            )
        ]

    def validate(self, data):
        """
        enforce followee field and follower field have different values
        """
        if data['followee_id'] == data['follower_id']:
            raise serializers.ValidationError("followee and follower should not be same")
        return data

class FriendURLSerializer(serializers.HyperlinkedModelSerializer):
    # followee_url = serializers.SerializerMethodField()
    # follower_url = serializers.SerializerMethodField()
    class Meta:
        model = Friend
        fields = ('followee_url', "follower_url")

    # def get_followee_url(self, obj):
    #     firend_url = f"{obj.host}author/{obj.followee_id}"
    #     return 

    # def get_follower_url(self, obj):
    #     firend_url = f"{obj.host}author/{obj.follower_id}"
    #     return 

# class FriendCreateResponseSerializer(serializers.HyperlinkedModelSerializer):
#     id = serializers.SerializerMethodField()
#     host = serializers.SerializerMethodField()
#     displayName = serializers.SerializerMethodField()

#     class Meta:
#         model = Friend
#         fields = ('followee_url', "follower_url")