import graphene

from plant_care_tracker.models import Plant, CareEvent
from plant_care_tracker.schemas.plant import (
    PlantType,
    AddPlant,
    UpdatePlant,
    DeletePlant,
)
from plant_care_tracker.schemas.event import (
    CareEventType,
    AddCareEvent,
    UpdateCareEvent,
    DeleteCareEvent,
)


class Query(graphene.ObjectType):
    all_plants = graphene.List(PlantType)
    all_care_events = graphene.List(CareEventType)
    plant = graphene.Field(PlantType, id=graphene.Int())
    care_event = graphene.Field(CareEventType, id=graphene.Int())

    def resolve_all_plants(self, info, **kwargs):
        return Plant.objects.all()

    def resolve_plant(self, info, id):
        return Plant.objects.get(pk=id)

    def resolve_all_care_events(self, info, **kwargs):
        return CareEvent.objects.all()

    def resolve_care_event(self, info, id):
        return CareEvent.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    add_plant = AddPlant.Field()
    update_plant = UpdatePlant.Field()
    delete_plant = DeletePlant.Field()

    add_care_event = AddCareEvent.Field()
    update_care_event = UpdateCareEvent.Field()
    delete_care_event = DeleteCareEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
