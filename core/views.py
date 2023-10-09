# myapp/views.py
# core/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from django.shortcuts import render
from .models import UploadFile  # Importez le modèle

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

import os
import json
import csv
from zipfile import ZipFile
import zipfile
import tempfile

#exemple de base 
# class FileFieldFormView(FormView):
#     form_class = UploadFileForm
#     template_name = "upload.html"
#     success_url = reverse_lazy("success_view_name")

#     def form_valid(self, form):
#         files = form.cleaned_data['file_field']
#         for file in files:
#             instance = UploadFile(file=file)  # Utilisez votre modèle ici
#             instance.save()  # Enregistre le fichier en base de données
#         return super().form_valid(form)
  
# exemple de processingdiffrent en fonction de lextension

# class FileFieldFormView(FormView):
#     form_class = UploadFileForm
#     template_name = "upload.html"
#     success_url = reverse_lazy("success_view_name")

#     def form_valid(self, form):
#         files = form.cleaned_data['file_field']
#         for file in files:
#             instance = UploadFile(file=file)
#             instance.save()
            
#             file_name, file_extension = os.path.splitext(file.name)

#             if file_extension == '.json':
#                 self.convert_json_to_csv(file)

#             elif file_extension == '.txt':
#                 self.compress_txt(file)

#         return super().form_valid(form)

#     def convert_json_to_csv(self, json_file):
#         json_file.seek(0)  # Réinitialiser le curseur
#         json_data = json.load(json_file)

#         if not json_data:
#             print("Le fichier JSON est vide")
#             return

#         people_data = json_data.get("people", [])

#         if not people_data or not isinstance(people_data, list):
#             print("Le fichier JSON doit contenir une liste d'objets sous la clé 'people'")
#             return

#         try:
#             with open(f"{json_file.name}.csv", "w", newline="") as csv_file:
#                 csv_writer = csv.writer(csv_file)
#                 # Écrire les en-têtes
#                 csv_writer.writerow(people_data[0].keys())
#                 # Écrire les données
#                 for item in people_data:
#                     csv_writer.writerow(item.values())
#         except KeyError as e:
#             print(f"Clé non trouvée : {e}")


#     def compress_txt(self, txt_file):
#         with ZipFile(f"{txt_file.name}.zip", "w") as zipf:
#             zipf.writestr(txt_file.name, txt_file.read().decode())


#metre en bdd les format transformés 


# class FileFieldFormView(FormView):
#     form_class = UploadFileForm
#     template_name = "upload.html"
#     success_url = reverse_lazy("success_view_name")

#     def form_valid(self, form):
#         files = form.cleaned_data['file_field']
#         for file in files:
#             # instance = UploadFile(file=file)  # <--- Supprimé
#             # instance.save()  # <--- Supprimé
            
#             file_name, file_extension = os.path.splitext(file.name)

#             if file_extension == '.json':
#                 self.convert_json_to_csv(file)

#             elif file_extension == '.txt':
#                 self.compress_txt(file)

#         return super().form_valid(form)

#     def convert_json_to_csv(self, json_file):
#         json_file.seek(0)  # Réinitialiser le curseur
#         json_data = json.load(json_file)

#         if not json_data:
#             print("Le fichier JSON est vide")
#             return

#         people_data = json_data.get("people", [])

#         if not people_data or not isinstance(people_data, list):
#             print("Le fichier JSON doit contenir une liste d'objets sous la clé 'people'")
#             return

#         try:
#             csv_file_path = f"{json_file.name}.csv"
#             with open(csv_file_path, "w", newline="") as csv_file:
#                 csv_writer = csv.writer(csv_file)
#                 # Écrire les en-têtes
#                 csv_writer.writerow(people_data[0].keys())
#                 # Écrire les données
#                 for item in people_data:
#                     csv_writer.writerow(item.values())
                    
#             # Pour sauvegarder le fichier CSV en base de données
#             csv_buffer = BytesIO()
#             with open(csv_file_path, "rb") as f:
#                 csv_buffer.write(f.read())
#             csv_file = InMemoryUploadedFile(
#                 csv_buffer, None, f"{json_file.name}.csv", 'text/csv', csv_buffer.tell(), None
#             )
#             instance = UploadFile(file=csv_file)
#             instance.save()
            
#         except KeyError as e:
#             print(f"Clé non trouvée : {e}")


#     def compress_txt(self, txt_file):
#         zip_file_path = f"{txt_file.name}.zip"
#         with ZipFile(zip_file_path, "w") as zipf:
#             zipf.writestr(txt_file.name, txt_file.read().decode())

#         # Pour sauvegarder le fichier ZIP en base de données
#         zip_buffer = BytesIO()
#         with open(zip_file_path, "rb") as f:
#             zip_buffer.write(f.read())
            
#         zip_file = InMemoryUploadedFile(
#             zip_buffer, None, f"{txt_file.name}.zip", 'application/zip', zip_buffer.tell(), None
#         )
#         instance = UploadFile(file=zip_file)
#         instance.save()



#en bdd avec fichier temporaire pour eviter de poluer la racibe du projet 

class FileFieldFormView(FormView):
    form_class = UploadFileForm
    template_name = "upload.html"
    success_url = reverse_lazy("success_view_name")

    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        for file in files:
            # instance = UploadFile(file=file)  # <--- Supprimé
            # instance.save()  # <--- Supprimé
            
            file_name, file_extension = os.path.splitext(file.name)

            if file_extension == '.json':
                self.convert_json_to_csv(file)

            elif file_extension == '.txt':
                self.compress_txt(file)

        return super().form_valid(form)

    def convert_json_to_csv(self, json_file):
        json_file.seek(0)  # Réinitialiser le curseur
        json_data = json.load(json_file)

        if not json_data:
            print("Le fichier JSON est vide")
            return

        people_data = json_data.get("people", [])

        if not people_data or not isinstance(people_data, list):
            print("Le fichier JSON doit contenir une liste d'objets sous la clé 'people'")
            return

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(people_data[0].keys())
                for item in people_data:
                    csv_writer.writerow(item.values())
            
            csv_file_path = csv_file.name

            # Pour sauvegarder le fichier CSV en base de données
            csv_buffer = BytesIO()
            with open(csv_file_path, "rb") as f:
                csv_buffer.write(f.read())
            csv_file = InMemoryUploadedFile(
                csv_buffer, None, f"{json_file.name}.csv", 'text/csv', csv_buffer.tell(), None
            )
            instance = UploadFile(file=csv_file)
            instance.save()
            
            os.remove(csv_file_path)  # Supprimer le fichier temporaire
            
        except KeyError as e:
            print(f"Clé non trouvée : {e}")


    def compress_txt(self, txt_file):
        # Créer un fichier temporaire pour le fichier zip
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as zip_temp:
            with ZipFile(zip_temp, "w") as zipf:
                zipf.writestr(txt_file.name, txt_file.read().decode())
            
            zip_file_path = zip_temp.name

        # Pour sauvegarder le fichier ZIP en base de données
        zip_buffer = BytesIO()
        with open(zip_file_path, "rb") as f:
            zip_buffer.write(f.read())
            
        zip_file = InMemoryUploadedFile(
            zip_buffer, None, f"{txt_file.name}.zip", 'application/zip', zip_buffer.tell(), None
        )
        instance = UploadFile(file=zip_file)
        instance.save()

        os.remove(zip_file_path)  # Supprimer le fichier temporaire
    


def success(request):
    return render(request, 'success.html')