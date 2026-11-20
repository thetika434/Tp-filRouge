from django.test import TestCase
from django.urls import reverse
from .models import Tache
from .forms import TacheForm


class TacheTests(TestCase):
    def test_creation_modele(self):
        tache = Tache.objects.create(titre="Réviser Django")
        self.assertEqual(str(tache), "Réviser Django")

    def test_liste_accessible(self):
        response = self.client.get(reverse("liste_taches"))
        self.assertEqual(response.status_code, 200)

    # ---- TP 2 : qualité logicielle ----

    def test_creation_valide_modele(self):
        """Une tâche créée avec uniquement un titre reçoit les valeurs par défaut."""
        tache = Tache.objects.create(titre="Écrire les tests")
        self.assertEqual(tache.statut, "A_FAIRE")
        self.assertEqual(tache.priorite, 2)
        self.assertEqual(Tache.objects.count(), 1)

    def test_formulaire_valide(self):
        form = TacheForm(data={
            "titre": "Tâche valide",
            "description": "",
            "statut": "A_FAIRE",
            "priorite": 2,
        })
        self.assertTrue(form.is_valid())

    def test_validation_priorite_hors_limites(self):
        """La priorité doit être comprise entre 1 et 3 (cas limites inclus)."""
        for priorite in (0, 4, 10):
            with self.subTest(priorite=priorite):
                form = TacheForm(data={
                    "titre": "Tâche invalide",
                    "description": "",
                    "statut": "A_FAIRE",
                    "priorite": priorite,
                })
                self.assertFalse(form.is_valid())
                self.assertIn("priorite", form.errors)

    def test_validation_priorite_bornes_valides(self):
        for priorite in (1, 2, 3):
            with self.subTest(priorite=priorite):
                form = TacheForm(data={
                    "titre": "Tâche",
                    "description": "",
                    "statut": "A_FAIRE",
                    "priorite": priorite,
                })
                self.assertTrue(form.is_valid())

    def test_liste_affiche_les_taches(self):
        Tache.objects.create(titre="Tâche visible")
        response = self.client.get(reverse("liste_taches"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tâche visible")

    def test_creation_via_post(self):
        response = self.client.post(reverse("creer_tache"), {
            "titre": "Créée par POST",
            "description": "Via le formulaire",
            "statut": "EN_COURS",
            "priorite": 1,
        })
        self.assertRedirects(response, reverse("liste_taches"))
        self.assertEqual(Tache.objects.count(), 1)
        tache = Tache.objects.get()
        self.assertEqual(tache.titre, "Créée par POST")
        self.assertEqual(tache.statut, "EN_COURS")

    def test_creation_via_post_invalide_ne_cree_rien(self):
        response = self.client.post(reverse("creer_tache"), {
            "titre": "Priorité invalide",
            "description": "",
            "statut": "A_FAIRE",
            "priorite": 9,
        })
        self.assertEqual(response.status_code, 200)  # le formulaire est réaffiché
        self.assertEqual(Tache.objects.count(), 0)

    def test_suppression_via_post(self):
        tache = Tache.objects.create(titre="À supprimer")
        response = self.client.post(reverse("supprimer_tache", args=[tache.pk]))
        self.assertRedirects(response, reverse("liste_taches"))
        self.assertFalse(Tache.objects.filter(pk=tache.pk).exists())

    def test_suppression_refuse_get(self):
        """La suppression est réservée au POST : un GET renvoie 405 et ne supprime rien."""
        tache = Tache.objects.create(titre="Doit rester")
        response = self.client.get(reverse("supprimer_tache", args=[tache.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Tache.objects.filter(pk=tache.pk).exists())
