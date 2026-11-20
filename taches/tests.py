from django.test import TestCase
from django.urls import reverse

from .forms import TacheForm
from .models import Tache


class TacheTests(TestCase):
    """Vérifie les modèles, formulaires et vues des tâches."""

    def test_creation_modele(self):
        """Vérifie les valeurs par défaut d'une tâche créée."""
        tache = Tache.objects.create(titre="Réviser Django")

        self.assertEqual(str(tache), "Réviser Django")
        self.assertEqual(tache.statut, "A_FAIRE")
        self.assertEqual(tache.priorite, 2)

    def test_liste_accessible(self):
        """Vérifie que la liste affiche une tâche existante."""
        Tache.objects.create(titre="Tâche affichée")

        response = self.client.get(reverse("liste_taches"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tâche affichée")

    def test_formulaire_valide(self):
        """Vérifie qu'un formulaire correctement rempli est valide."""
        form = TacheForm(
            data={
                "titre": "Préparer le TP",
                "description": "Écrire les tests",
                "statut": "A_FAIRE",
                "priorite": 2,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_validation_priorite(self):
        """Vérifie les priorités limites autorisées et refusées."""
        for priorite in (0, 4, 10):
            with self.subTest(priorite=priorite):
                form = TacheForm(
                    data={
                        "titre": "Priorité invalide",
                        "description": "",
                        "statut": "A_FAIRE",
                        "priorite": priorite,
                    }
                )
                self.assertFalse(form.is_valid())

        for priorite in (1, 2, 3):
            with self.subTest(priorite=priorite):
                form = TacheForm(
                    data={
                        "titre": "Priorité valide",
                        "description": "",
                        "statut": "A_FAIRE",
                        "priorite": priorite,
                    }
                )
                self.assertTrue(form.is_valid(), form.errors)

    def test_creation_via_post(self):
        """Vérifie la création d'une tâche par la vue."""
        response = self.client.post(
            reverse("creer_tache"),
            {
                "titre": "Tâche créée",
                "description": "Depuis un POST",
                "statut": "A_FAIRE",
                "priorite": 2,
            },
        )

        self.assertRedirects(response, reverse("liste_taches"))
        self.assertTrue(Tache.objects.filter(titre="Tâche créée").exists())

    def test_post_invalide_ne_cree_pas_de_tache(self):
        """Vérifie qu'une priorité invalide ne crée aucune tâche."""
        response = self.client.post(
            reverse("creer_tache"),
            {
                "titre": "Tâche invalide",
                "description": "",
                "statut": "A_FAIRE",
                "priorite": 9,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tache.objects.filter(titre="Tâche invalide").exists())

    def test_suppression_via_post(self):
        """Vérifie la suppression d'une tâche par POST."""
        tache = Tache.objects.create(titre="Tâche à supprimer")

        response = self.client.post(
            reverse("supprimer_tache", args=[tache.pk])
        )

        self.assertRedirects(response, reverse("liste_taches"))
        self.assertFalse(Tache.objects.filter(pk=tache.pk).exists())

    def test_suppression_via_get_refusee(self):
        """Vérifie qu'un GET ne supprime pas de tâche."""
        tache = Tache.objects.create(titre="Tâche conservée")

        response = self.client.get(
            reverse("supprimer_tache", args=[tache.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Tache.objects.filter(pk=tache.pk).exists())
