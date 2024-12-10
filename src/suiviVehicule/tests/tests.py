import pytest
from suiviVehicule.models import Recordcomment
from datetime import datetime, time

@pytest.mark.django_db
def test_trip_cancellation():
    # Étape 1 : Créer un trajet
    record = Recordcomment.objects.create(
        id_trip=101,
        comment="Trajet annulé en raison d'un problème mécanique.",
        vehicleno="MH12345",
        driver_oname="Jean Dupont",
        FromPlace="Paris",
        ToPlace="Lyon",
        trip_start_date="2024-11-28",
        pick_up_time=time(10, 30),
        datetime=datetime(2024, 11, 28, 10, 0),
        etat=1,
        driver_mobile_number="0612345678",
        current="At pick-up location",
        difftimestart=15.0,
        difftimepickup=5.0,
        speed=50.5,
        speedMeasure="kph",
        odometer=1500.25,
        ignition="ON",
        engineTime=120.5,
        engineStatus="Idle",
        catno=2
    )

    # Étape 2 : Appeler la méthode d'annulation avec un reason_id
    reason_id = 1
    record.status = "cancelled"
    record.reason = reason_id
    record.save()

    # Étape 3 : Vérifier que la mise à jour est effectuée dans la base de données
    record.refresh_from_db()
    assert record.status == "cancelled"
    assert record.reason == reason_id
