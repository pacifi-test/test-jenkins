import csv, io
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
# one parameter named request
from apps.persona.models.departamento import Departamento
from apps.persona.models.distrito import Distrito
from apps.persona.models.provincia import Provincia


def departamento_upload(request):
    "https://medium.com/@simathapa111/how-to-upload-a-csv-file-in-django-3a0d6295f624"
    # declaring template
    template = "persona/csv/departamento.html"
    data = Departamento.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'profiles': data
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        # _, created = Departamento.objects.update_or_create(
        #     codigo=column[0],
        #     nombre=column[3],
        # )
        departamento = Departamento.objects.get(codigo=column[0])

        if column[1] != '00' and column[2] != '00':
            provincia = Provincia.objects.get(codigo=column[1], departamento=departamento)
            Distrito.objects.create(codigo=column[2], nombre=column[3], provincia=provincia)

    context = {}
    return render(request, template, context)
