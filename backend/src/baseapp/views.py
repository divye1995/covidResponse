import os
from django.shortcuts import render
import json
from django.views.generic import View
from django.db.models import Func, F, Sum, Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework as filters
from rest_framework import mixins, generics, permissions
from baseapp.models import ( Covid, Entity, Feedback, EntityBulkEdit,
                            BulkOperation, EntityHistory, Location, Request,
                            Pledge)
from user.mixins import HttpResponseMixin
from .serializers import (CovidSerializer,ItemSerializer1, EntitySerializer,
                          EntityPublicSerializer, FeedbackSerializer,
                          EntityBulkEditSerializer, BulkOperationSerializer,
                          EntityListSerializer, SmallEntitySerializer,
                          EntityHistorySerializer, StateSerializer,
                          DistrictSerializer, LocationSerializer,
                          RequestSerializer, PledgeSerializer
                         )
from user.permissions import IsStaffReadWriteOrAuthReadOnly, IsStaffReadWriteOrReadOnly, UserViewPermission
from user.utils import is_json
from baseapp.permissions import EntityPermissions
import git

# Create your views here.
def get_id_from_request(request):
    """Small function to retrieve the Id from request
    It can either take id from get parameters
    or it can retrieve id from the input Json data
    """
    url_id = request.GET.get('id', None)
    input_json_id = None
    if is_json(request.body):
        input_json_data = json.loads(request.body)
        input_json_id = input_json_data.get("id", None)
    input_id = url_id or input_json_id or None
    return input_id


class CovidFilter(filters.FilterSet):
 #   min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
 #   max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Covid
        #fields = ('number_of_rooms', 'floor_area_size',
        #          'price_per_month', 'is_available')
        fields = {
                    'id': ['gte', 'lte'],
                    'latitude' : ['gte', 'lte'],
                    'longitude' : ['gte', 'lte']
                }
    @property
    def qs(self):
        parent_qs = super(CovidFilter, self).qs
        return parent_qs
       #if 'finyear' in self.request.query_params:
       #    return parent_qs
       #else:
       #    return parent_qs.filter(finyear='NA')




class CovidAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [IsStaffReadWriteOrAuthReadOnly]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = CovidSerializer
    passed_id = None
    input_id = None
    search_fields = ('name',)
    ordering_fields = ('name', 'id', 'created', 'updated')
    filterset_class = CovidFilter
    queryset = Covid.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return Covid.objects.all()
       return Covid.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post method would create a apartment object"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """put method will update the apartment object. All fields need to be
        present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Will delete the retrieved object"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)

class CovidBulkDeleteView(GenericAPIView):
    throttle_classes = ()
    permission_classes = [IsStaffReadWriteOrAuthReadOnly]
    serializer_class = ItemSerializer1

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ids = serializer.data['user_ids']
        if (len(user_ids) == 1) and (user_ids[0] == 'all'):
            Covid.objects.all().delete()
        else:
            Covid.objects.filter(id__in=user_ids).delete()
        return Response({'status': 'OK'})



class CreateEntityView(generics.CreateAPIView):
    """This will create a new Entity. This view does not require
    authentication. The Entities created with this view, will have is_active
    field set to false."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = EntityPublicSerializer

class EntityFilter(filters.FilterSet):
 #   min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
 #   max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Entity
        #fields = ('number_of_rooms', 'floor_area_size',
        #          'price_per_month', 'is_available')
        fields = {
                    'id': ['gte', 'lte'],
                    'latitude' : ['gte', 'lte'],
                    'longitude' : ['gte', 'lte'],
                    'record_type' : ['exact'],
                    'status' : ['exact'],
                    'urgency' : ['exact'],
                    'state' : ['exact'],
                    'district' : ['exact'],
                    'assigned_to_user' : ['isnull'],
                    'assigned_to_user__name' : ['contains', 'icontains'],
                    'assigned_to_user__id' : ['exact'],
                    'assigned_to_group' : ['isnull'],
                    'assigned_to_group__name' : ['contains', 'icontains'],
                    'assigned_to_group__id' : ['exact'],
                    'assigned_to_group__organization__id' : ['exact'],
                    'user__email' : ['exact'],
                    'formio_usergroup' : ['exact'],
                    'what_help' : ['contains', 'icontains'],
                }
    @property
    def qs(self):
        parent_qs = super(EntityFilter, self).qs
        queryset = parent_qs
        for key in self.request.query_params:
            if "extra_fields__" in key:
                value = self.request.query_params[key]
                queryset = queryset.filter(**{ key: value })
            if "what_help" in key:
                value = self.request.query_params[key].lstrip(",").rstrip(",")
                for item in value:
                    queryset = queryset.filter(what_help__icontains=item)
                
                
        return queryset
       #if "volunteer" in self.request.query_params:
       #    volunteer = self.request.query_params['volunteer']
       #    queryset = parent_qs.filter(extra_fields__volunteer = volunteer)
       #    return queryset
       #return parent_qs
       #if 'finyear' in self.request.query_params:
       #    return parent_qs
       #else:
       #    return parent_qs.filter(finyear='NA')




class EntityBulkEditAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity Bulk Edit table"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntityBulkEditSerializer
    passed_id = None
    input_id = None
    search_fields = ('id')
    ordering_fields = ('id', "created")
    queryset = EntityBulkEdit.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return EntityBulkEdit.objects.all()
       return EntityBulkEdit.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get Entity request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """This would create an Entity Bulk Edit  object in database"""
        print("I am in post")
        return self.create(request, *args, **kwargs)

class EntitySmallAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = SmallEntitySerializer
    passed_id = None
    input_id = None
    search_fields = ('keywords', 'name', 'description', 'id')
    ordering_fields = ('name', 'id', 'created', 'updated')
    filterset_class = EntityFilter
    queryset = Entity.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return Entity.objects.all()
       return Entity.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class EntityHistoryAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntityHistorySerializer
    passed_id = None
    input_id = None
    search_fields = ('id')
    ordering_fields = ('title', 'id', 'created', 'updated')
    filter_fields=("id", "entity__id")
    
    queryset = EntityHistory.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return EntityHistory.objects.all()
       return EntityHistory.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class DistrictAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = DistrictSerializer
    passed_id = None
    input_id = None
    search_fields = ('keywords', 'name', 'description')
    ordering_fields = ('district', 'id', 'created', 'updated')
    queryset = Entity.objects.all().values("district").annotate(count=Count('id'))
    def get_queryset(self, *args, **kwargs):
       return self.queryset
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class StateAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = StateSerializer
    passed_id = None
    input_id = None
    search_fields = ('keywords', 'name', 'description')
    ordering_fields = ('state', 'id', 'created', 'updated')
    queryset = Entity.objects.all().values("state").annotate(count=Count('id'))
    def get_queryset(self, *args, **kwargs):
       return self.queryset
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class EntityListAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntityListSerializer
    passed_id = None
    input_id = None
    search_fields = ('id', 'keywords', 'name', 'description')
    ordering_fields = ('name', 'id', 'created', 'updated')
    filterset_class = EntityFilter
    queryset = Entity.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return Entity.objects.all()
       return Entity.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class EntityAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntitySerializer
    passed_id = None
    input_id = None
    search_fields = ('id', 'keywords', 'name', 'description')
    ordering_fields = ('name', 'id', 'created', 'updated')
    filterset_class = EntityFilter
    queryset = Entity.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return Entity.objects.all()
       return Entity.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """This would create an entity object in database. Name, description,
        latitute and longitude are mandatory fields. This method is only
        allowed for users with staff (user manager) permissions"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """This method would update the entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. All fields will be updated."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """This method would patch the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. Only the fields passed on in the data will be updated"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """This method would delete the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)


class FeedbackAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [IsStaffReadWriteOrReadOnly]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackSerializer
    passed_id = None
    input_id = None
    search_fields = ('id')
    ordering_fields = ('id', 'created', 'updated')
    queryset = Feedback.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return Feedback.objects.all()
       return Feedback.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post method would create a apartment object"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """put method will update the apartment object. All fields need to be
        present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Will delete the retrieved object"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)

class BulkOperationAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [UserViewPermission]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = BulkOperationSerializer
    passed_id = None
    input_id = None
    search_fields = ('id')
    ordering_fields = ('id', 'created', 'updated')
    queryset = BulkOperation.objects.all()
    def get_queryset(self, *args, **kwargs):
       if self.request.user.is_staff:
           return BulkOperation.objects.all()
       return BulkOperation.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post method would create a apartment object"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """put method will update the apartment object. All fields need to be
        present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Will delete the retrieved object"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)

class EntityExportAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
     def get(self, request):
         url = "https://coast-india.s3.ap-south-1.amazonaws.com/export/data.csv"
         data = json.dumps({"url":url})
         return self.render_to_response(data, status="200")

class VersionAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     def get(self, request):
         try:
             BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
             REPO_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
             repo = git.Repo(path=REPO_DIR)
             sha = repo.head.object.hexsha
             commit_url = f'https://github.com/rajesh241/covidResponse/commit/{sha}'
             version = { 'sha': sha, 'commit_url': commit_url, 'hash': sha[:7] }
             data = json.dumps(version)
             status_code = 200
         except Exception as e:
             data = json.dumps({'message':f"Errored: {e}"})
             status_code = 404
         return self.render_to_response(data, status=status_code)



class LocationAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LocationSerializer
    passed_id = None
    input_id = None
    search_fields = ('code', 'name')
    ordering_fields = ('id', 'code', 'name')
    filter_fields=("id", "name", "location_type", "code")
    queryset = Location.objects.all()
    def get_queryset(self, *args, **kwargs):
       return Location.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class RequestFilter(filters.FilterSet):
 #   min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
 #   max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Request
        #fields = ('number_of_rooms', 'floor_area_size',
        #          'price_per_month', 'is_available')
        fields = {
                    'id': ['gte', 'lte'],
                    'user__id' : ['exact'],
                    'user__organization__id' : ['exact'],
                    'amount_pending' : ['gt']
                }
    @property
    def qs(self):
        parent_qs = super(RequestFilter, self).qs
        queryset = parent_qs
        return queryset
 
class RequestAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestSerializer
    filterset_class = RequestFilter
    passed_id = None
    input_id = None
    search_fields = ('id', 'title')
    ordering_fields = ('id')
    queryset = Request.objects.all()
    def get_queryset(self, *args, **kwargs):
       return Request.objects.all().order_by("-updated")
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """This would create an entity object in database. Name, description,
        latitute and longitude are mandatory fields. This method is only
        allowed for users with staff (user manager) permissions"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """This method would update the entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. All fields will be updated."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """This method would patch the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. Only the fields passed on in the data will be updated"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """This method would delete the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)


class PledgeFilter(filters.FilterSet):
 #   min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
 #   max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Pledge
        #fields = ('number_of_rooms', 'floor_area_size',
        #          'price_per_month', 'is_available')
        fields = {
                    'id': ['gte', 'lte'],
                    'user__id' : ['exact'],
                    'user__organization__id' : ['exact'],
                }
    @property
    def qs(self):
        parent_qs = super(PledgeFilter, self).qs
        queryset = parent_qs
        return queryset
 
class PledgeAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """Primary view of Entity table. GET Methods do not require authentication,
    Other methods are allowed only for users with permissions of user manager"""
    permission_classes = [EntityPermissions]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = PledgeSerializer
    filterset_class = PledgeFilter
    passed_id = None
    input_id = None
    search_fields = ('id', 'request__organization__name', 'user__name')
    ordering_fields = ('id')
    queryset = Pledge.objects.all()
    def get_queryset(self, *args, **kwargs):
       return Pledge.objects.all().order_by("-updated")
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        """This method will return the list of the Entity items based on the
        filter values specified. The number of items can be controlled by the
        limit parameter. 
        ordering field can be set to either of (name, id, created, updated). It
        will sort the returned results based on that. For example
        entity/?ordering=updated or entity/?ordering=-name (Sort by name
        descending)
        If id of the Entity is appended to the url for example /entity/1, then
        it would return only one entity corresponding to the id mentioned. 
        """
        print(f"I am in get request {request.user}")
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """This would create an entity object in database. Name, description,
        latitute and longitude are mandatory fields. This method is only
        allowed for users with staff (user manager) permissions"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """This method would update the entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. All fields will be updated."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """This method would patch the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'. Only the fields passed on in the data will be updated"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """This method would delete the existing entity object, based on the id as
        supplied in the data. ID can also be specified in the url for example,
        'entity/id'."""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)


