import graphene
from graphene_django.types import DjangoObjectType

from plant_care_tracker.models import CareEvent, Plant


class CareEventType(DjangoObjectType):
    class Meta:
        model = CareEvent


class AddCareEvent(graphene.Mutation):
    class Arguments:
        plant_id = graphene.Int()
        event_type = graphene.String()
        date = graphene.Date()
        notes = graphene.String()

    care_event = graphene.Field(CareEventType)

    def mutate(self, info, plant_id, event_type, date, notes=""):
        plant = Plant.objects.get(pk=plant_id)
        care_event = CareEvent.objects.create(
            plant=plant, event_type=event_type, date=date, notes=notes
        )
        return AddCareEvent(care_event=care_event)


class UpdateCareEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        plant_id = graphene.Int()
        event_type = graphene.String()
        date = graphene.Date()
        notes = graphene.String()

    care_event = graphene.Field(CareEventType)

    def mutate(self, info, id, plant_id=None, event_type=None, date=None, notes=None):
        care_event = CareEvent.objects.get(pk=id)
        if plant_id:
            care_event.plant = Plant.objects.get(pk=plant_id)
        if event_type:
            care_event.event_type = event_type
        if date:
            care_event.date = date
        if notes:
            care_event.notes = notes
        care_event.save()
        return UpdateCareEvent(care_event=care_event)


class DeleteCareEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            care_event = CareEvent.objects.get(pk=id)
            care_event.delete()
            return DeleteCareEvent(success=True)
        except CareEvent.DoesNotExist:
            return DeleteCareEvent(success=False)
