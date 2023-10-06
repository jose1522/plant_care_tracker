import pytest
from plant_care_tracker.models import Plant, CareEvent


@pytest.mark.django_db
def test_create_plant():
    plant = Plant.objects.create(name="Rose", species="Rosa")
    assert Plant.objects.count() == 1
    assert plant.name == "Rose"
    assert plant.species == "Rosa"


@pytest.mark.django_db
def test_create_care_event():
    plant = Plant.objects.create(name="Rose", species="Rosa")
    event = CareEvent.objects.create(
        plant=plant,
        event_type="Watering",
        date="2022-10-06",
        notes="Watered thoroughly",
    )

    assert CareEvent.objects.count() == 1
    assert event.event_type == "Watering"
    assert str(event.date) == "2022-10-06"
    assert event.notes == "Watered thoroughly"
