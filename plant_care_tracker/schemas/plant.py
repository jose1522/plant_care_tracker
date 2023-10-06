import graphene
from graphene_django.types import DjangoObjectType

from plant_care_tracker.models import Plant


class PlantType(DjangoObjectType):
    class Meta:
        model = Plant


class AddPlant(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        species = graphene.String()

    plant = graphene.Field(PlantType)

    def mutate(self, info, name, species):
        plant = Plant.objects.create(name=name, species=species)
        return AddPlant(plant=plant)


class UpdatePlant(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        species = graphene.String()

    plant = graphene.Field(PlantType)

    def mutate(self, info, id, name=None, species=None):
        plant = Plant.objects.get(pk=id)
        if name:
            plant.name = name
        if species:
            plant.species = species
        plant.save()
        return UpdatePlant(plant=plant)


class DeletePlant(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            plant = Plant.objects.get(pk=id)
            plant.delete()
            return DeletePlant(success=True)
        except Plant.DoesNotExist:
            return DeletePlant(success=False)
