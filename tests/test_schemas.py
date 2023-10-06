import pytest
from graphene_django.utils.testing import GraphQLTestCase

from plant_care_tracker.models import Plant, CareEvent
from plant_care_tracker.schemas.main import schema


class PlantCareTrackerGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @pytest.mark.django_db
    def test_query_all_plants(self):
        Plant.objects.create(name="Rose", species="Rosa")
        response = self.query(
            """
            {
                allPlants {
                    id
                    name
                    species
                }
            }
        """
        )
        content = response.json()
        self.assertResponseNoErrors(response)
        assert len(content["data"]["allPlants"]) == 1
        assert content["data"]["allPlants"][0]["name"] == "Rose"
        assert content["data"]["allPlants"][0]["species"] == "Rosa"

    @pytest.mark.django_db
    def test_query_single_plant(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        response = self.query(
            f"""
            {{
                plant(id: {plant.id}) {{
                    name
                    species
                }}
            }}
        """
        )
        content = response.json()
        self.assertResponseNoErrors(response)
        assert content["data"]["plant"]["name"] == "Rose"
        assert content["data"]["plant"]["species"] == "Rosa"

    @pytest.mark.django_db
    def test_add_plant_mutation(self):
        response = self.query(
            """
            mutation {
                addPlant(name: "Rose", species: "Rosa") {
                    plant {
                        id
                        name
                        species
                    }
                }
            }
        """
        )
        content = response.json()
        assert content["data"]["addPlant"]["plant"]["name"] == "Rose"
        assert content["data"]["addPlant"]["plant"]["species"] == "Rosa"
        assert Plant.objects.count() == 1

    @pytest.mark.django_db
    def test_update_plant_mutation(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        response = self.query(
            f"""
            mutation {{
                updatePlant(id: {plant.id}, name: "Lily", species: "Lilium") {{
                    plant {{
                        id
                        name
                        species
                    }}
                }}
            }}
        """
        )
        content = response.json()
        assert content["data"]["updatePlant"]["plant"]["name"] == "Lily"
        assert content["data"]["updatePlant"]["plant"]["species"] == "Lilium"
        updated_plant = Plant.objects.get(id=plant.id)
        assert updated_plant.name == "Lily"
        assert updated_plant.species == "Lilium"

    @pytest.mark.django_db
    def test_delete_plant_mutation(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        response = self.query(
            f"""
            mutation {{
                deletePlant(id: {plant.id}) {{
                    success
                }}
            }}
        """
        )
        self.assertEquals(response.status_code, 200)


class CareEventGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @pytest.mark.django_db
    def test_create_care_event(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        response = self.query(
            f"""
            mutation {{
                addCareEvent(plantId: {plant.id}, eventType: "water", date: "2023-01-01") {{
                    careEvent {{
                        id
                        eventType
                        date
                    }}
                }}
            }}
            """
        )
        content = response.json()
        assert content["data"]["addCareEvent"]["careEvent"]["eventType"] == "WATER"

    @pytest.mark.django_db
    def test_update_care_event(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        care_event = CareEvent.objects.create(
            plant=plant, event_type="water", date="2023-01-01"
        )
        response = self.query(
            f"""
            mutation {{
                updateCareEvent(id: {care_event.id}, eventType: "fertilize") {{
                    careEvent {{
                        id
                        eventType
                    }}
                }}
            }}
            """
        )
        content = response.json()
        assert (
            content["data"]["updateCareEvent"]["careEvent"]["eventType"] == "FERTILIZE"
        )

    @pytest.mark.django_db
    def test_delete_care_event(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        care_event = CareEvent.objects.create(
            plant=plant, event_type="Watering", date="2023-01-01"
        )
        response = self.query(
            f"""
            mutation {{
                deleteCareEvent(id: {care_event.id}) {{
                    success
                }}
            }}
            """
        )
        content = response.json()
        assert content["data"]["deleteCareEvent"]["success"]
        assert CareEvent.objects.count() == 0

    @pytest.mark.django_db
    def test_all_care_events(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        CareEvent.objects.create(plant=plant, event_type="Watering", date="2023-01-01")
        CareEvent.objects.create(plant=plant, event_type="Pruning", date="2023-01-02")
        response = self.query(
            """
            {
                allCareEvents {
                    id
                    eventType
                }
            }
            """
        )
        content = response.json()
        assert len(content["data"]["allCareEvents"]) == 2

    @pytest.mark.django_db
    def test_query_care_event_by_id(self):
        plant = Plant.objects.create(name="Rose", species="Rosa")
        care_event = CareEvent.objects.create(
            plant=plant, event_type="water", date="2023-01-01"
        )
        response = self.query(
            f"""
            {{
                careEvent(id: {care_event.id}) {{
                    id
                    eventType
                }}
            }}
            """
        )
        content = response.json()
        assert content["data"]["careEvent"]["id"] == str(care_event.id)
        assert content["data"]["careEvent"]["eventType"] == "WATER"
