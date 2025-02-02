import pytest
from django.contrib.gis.geos import Point

from qfdmo.models import (
    ActeurService,
    ActeurType,
    Action,
    EconomieCirculaireActeur,
    NomAsNaturalKeyModel,
    PropositionService,
)


class TestEconomieCirculaireNomAsNaturalKeyHeritage:
    def test_natural(self):
        assert NomAsNaturalKeyModel in EconomieCirculaireActeur.mro()


class TestEconomieCirculairePoint:
    def test_longitude_Latitude(self):
        economie_circulaire_acteur = EconomieCirculaireActeur(location=Point(1.1, 2.2))
        assert economie_circulaire_acteur.longitude == 1.1
        assert economie_circulaire_acteur.latitude == 2.2


class TestSerialize:
    @pytest.mark.django_db
    def test_serialize(self):
        acteur_type = ActeurType.objects.create(nom="Test Object", lvao_id=123)
        economie_circulaire_acteur = EconomieCirculaireActeur.objects.create(
            nom="Test Object", location=Point(0, 0), acteur_type=acteur_type
        )
        acteur_service = ActeurService.objects.create(nom="Test Object", lvao_id=123)
        action = Action.objects.create(nom="Test Object", lvao_id=123)
        proposition_service = PropositionService.objects.create(
            acteur_service=acteur_service,
            action=action,
            economie_circulaire_acteur=economie_circulaire_acteur,
        )
        assert economie_circulaire_acteur.serialize() == {
            "id": economie_circulaire_acteur.id,
            "nom": "Test Object",
            "identifiant_unique": None,
            "acteur_type": acteur_type.serialize(),
            "adresse": None,
            "adresse_complement": None,
            "code_postal": None,
            "ville": None,
            "url": None,
            "email": None,
            "telephone": None,
            "multi_base": False,
            "nom_commercial": None,
            "nom_officiel": None,
            "manuel": False,
            "label_reparacteur": False,
            "siret": None,
            "source_donnee": None,
            "identifiant_externe": None,
            "location": {"type": "Point", "coordinates": [0.0, 0.0]},
            "proposition_services": [proposition_service.serialize()],
        }
