import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional


class ProfileManager(ttk.Frame):
    """
    Composant pour la gestion des profils
    """

    def __init__(
        self,
        master: tk.Tk,
        on_profiles_updated: Optional[Callable[[List[str]], None]] = None,
    ):
        """
        Initialise le gestionnaire de profils

        :param master: Widget parent
        :param on_profiles_updated: Fonction de callback lors de la mise à jour des profils
        """
        super().__init__(master, style="TFrame")

        self.on_profiles_updated = on_profiles_updated
        self.available_profiles: List[str] = []
        self.selected_profiles: List[str] = []

        # Créer les widgets
        self._create_widgets()

    def _create_widgets(self):
        """
        Crée les widgets du gestionnaire de profils
        """
        # Frame pour l'ajout manuel de profils
        manual_frame = ttk.Frame(self)
        manual_frame.pack(fill=tk.X, pady=5)

        # Étiquette et champ de saisie pour l'ajout manuel
        ttk.Label(manual_frame, text="Ajouter un profil:").pack(side=tk.LEFT, padx=5)
        self.profile_entry = ttk.Entry(manual_frame, width=20)
        self.profile_entry.pack(side=tk.LEFT, padx=5)

        # Bouton d'ajout
        ttk.Button(
            manual_frame, text="+", command=self._add_manual_profile, width=3
        ).pack(side=tk.LEFT)

        # Frame pour la liste des profils
        list_frame = ttk.LabelFrame(self, text="Profils disponibles")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Liste des profils disponibles
        self.profile_list = tk.Listbox(
            list_frame, selectmode=tk.MULTIPLE, exportselection=False
        )
        self.profile_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.profile_list.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.profile_list.config(yscrollcommand=scrollbar.set)

        # Événement de sélection
        self.profile_list.bind("<<ListboxSelect>>", self._on_profile_selection)

    def set_available_profiles(self, profiles: List[str]):
        """
        Définit les profils disponibles

        :param profiles: Liste des profils disponibles
        """
        # Vider la liste actuelle
        self.profile_list.delete(0, tk.END)

        # Trier les profils
        profiles.sort()

        # Ajouter les nouveaux profils
        self.available_profiles = profiles
        for profile in profiles:
            self.profile_list.insert(tk.END, profile)

    def _add_manual_profile(self):
        """
        Ajoute un profil manuellement
        """
        profile = self.profile_entry.get().strip()

        if not profile:
            messagebox.showwarning("Attention", "Veuillez entrer un nom de profil.")
            return

        if profile in self.available_profiles:
            messagebox.showwarning("Attention", f"Le profil '{profile}' existe déjà.")
            return

        # Ajouter le profil
        self.available_profiles.append(profile)
        self.set_available_profiles(self.available_profiles)

        # Effacer le champ de saisie
        self.profile_entry.delete(0, tk.END)

    def _on_profile_selection(self, event):
        """
        Gère la sélection des profils

        :param event: Événement de sélection
        """
        # Récupérer les indices des profils sélectionnés
        selected_indices = self.profile_list.curselection()

        # Mettre à jour la liste des profils sélectionnés
        self.selected_profiles = [
            self.profile_list.get(idx) for idx in selected_indices
        ]

        # Appeler le callback si défini
        if self.on_profiles_updated:
            self.on_profiles_updated(self.selected_profiles)
