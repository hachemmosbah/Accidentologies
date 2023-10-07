from django.shortcuts import redirect, render 
import pandas as pd
from Acc_route.data_vis import *
from Acc_route.models import *
# from django.urls import reverse


def index(request):
    return render(request, 'Acc_route/index.html')

def dep_data():
    # treatment of dataframe and query
    names=['code_departement', 'nom_departement', 'code_region', 'nom_region']
    df = pd.read_csv('Acc_route/data/departements-france.csv',
                      header=None, skiprows=[0], names=names)
    list_code_departement = df.code_departement.tolist()
    list_nom_departement = df.nom_departement.tolist()

    list_code_departement1 = []
    list_code_departement2 = [971,972,973,974,976]

    for i in range(1, len(list_code_departement)-5):
        i = i*10
        list_code_departement1.append(i)
        
    list_code_departement = list_code_departement1 + list_code_departement2
    list_code_departement.insert(29, 201)
    list_code_departement.insert(30, 202)
    list_code_departement.remove(200)
    departement = zip(list_code_departement1, list_nom_departement)
    return departement


def data(request):
    departement = dep_data()
    context = {
        'departement': departement
    }
    return render(request, 'Acc_route/data.html', context)


def form_data(request):
    
    year = request.POST.get('year')
    age1 = request.POST.get('age1')
    age2 = request.POST.get('age2')
    unhurt = request.POST.get('unhurt')
    dead = request.POST.get('dead')
    hospitalized = request.POST.get('hospitalized')
    hurt_light = request.POST.get('hurt_light')
    men = request.POST.get('men')
    women = request.POST.get('women')
    # gravity = request.POST.get('gravity')
    # gender = request.POST.get('gender')
    departement = request.POST.get('departement')
    return year, departement, age1, age2, unhurt, dead, hospitalized, hurt_light, men, women #gravity, gender


def graphique(year, departement,age1, age2):

    age1 = int(age1)
    age2 = int(age2)
    
    plot1 = plot(year, departement,1, 1 ,age1, age2, 'INDEMNS', 'rgba(230, 36, 36, 0.5)')
    plot2 = plot(year, departement,1,  2,age1, age2, 'DÉCÉDES', 'rgba(4, 0, 247, 0.5)')
    plot3 = plot(year, departement,1,  3,age1, age2, 'BLESSÉES HOSPITALISÉES', 'rgba(54, 214, 71, 0.5)')
    plot4 = plot(year, departement,1,  4,age1, age2, 'BLESSÉES LEGERÉES', 'rgba(0, 0, 0, 0.5)')
    plot5 = plot(year, departement,2,  1,age1, age2, 'INDEMNS', 'rgba(230, 36, 36, 0.5)')
    plot6 = plot(year, departement,2,  2,age1, age2, 'DÉCÉDES', 'rgba(4, 0, 247, 0.5)')
    plot7 = plot(year, departement,2,  3,age1, age2, 'BLESSÉES HOSPITALISÉES', 'rgba(54, 214, 71, 0.5)')
    plot8 = plot(year, departement,2,  4,age1, age2, 'BLESSÉES LEGERÉES', 'rgba(0, 0, 0, 0.5)')
    # plot1 = plot(year, departement, gender, gravity, age1, age2,)
    plot9 = plot_carte_nb_acc()
    plot10 = plot_carte_loc() 

    return plot1,plot2,plot3,plot4,plot5,plot6,plot7,plot8, plot9, plot10
    
def error_404(request):
    return render(request, 'Acc_route/404.html')

# def save_data():
#     data = DataForm()
#     data.save()


def dashboard(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        # check whether it's valid:
        if form is not None:
            
            year, departement, age1, age2, unhurt, dead, hospitalized, hurt_light, men, women = form_data(request)
            if  not year :
                return render(request,'Acc_route/404.html')
            else :
                year = int(year)
                departement = str(departement)
                age1 = int(age1)
                age2 = int(age2)
                # unhurt = int(unhurt)
                # dead = int(dead)
                # hospitalized = int(hospitalized)
                # hurt_light = int(hurt_light)
                # men = int(men)
                # women = int(women)
                # gender = int(gender)
                # gravity = int(gravity)
                plot1,plot2,plot3,plot4,plot5,plot6,plot7,plot8, plot9, plot10 = graphique(year, departement,age1, age2)
                
                context = {
                    'year': year, 'departement': departement, 'age1': age1, 
                    'age2': age2, 'unhurt': unhurt, 'dead': dead, 'hospitalized': hospitalized,
                    'hurt_light': hurt_light, 'men': men, 'women': women, 'plot1': plot1,
                    'plot2': plot2,'plot3': plot3, 'plot4': plot4, 'plot5': plot5,
                    'plot6': plot6, 'plot7': plot7, 'plot8': plot8,
                    'plot9': plot9, 'plot10': plot10
                
                }
                        
                return render(request, "Acc_route/dashboard.html", context)
        else:

            form = DataForm() 

        return render(request, "Acc_route/data.html", {"form": form})

def data_predict(request):
    departement = dep_data()
    context = {
        'departement': departement
    }
    return render(request, "Acc_route/data_pred.html", context)

def form_pred(request):
    year = request.POST.get('year')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    departement = request.POST.get('departement')
    location = request.POST.get('location')
    intersection = request.POST.get('intersection')
    light = request.POST.get('light')
    return year, departement, age, gender, location, intersection, light

def predict(request):
    if request.method == "POST":
        form = DataPred(request.POST)

        if form is not None:
            year, departement, age, gender, location, intersection, light = form_pred(request)
            if  not year :
                return render(request,'Acc_route/404.html')
            else :
                context = {
                    'year': year, 'departement': departement, 'age': age,
                    'gender': gender, 'location': location, 'intersection': intersection
                    , 'light': light
                    }
                return render(request, "Acc_route/prediction.html", context)
    else:

        form = DataPred() 

    return render(request, "Acc_route/data_pred.html", {"form": form})
        