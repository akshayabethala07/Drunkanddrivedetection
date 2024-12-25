from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ClientRegister_Model, Country, State, City, Gender
from .forms import RegistrationForm
from .data_handling import load_and_preprocess_data
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Home Page
def index(request):
    return render(request, 'users/index.html')

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)  # Session is created here
            return redirect('profile')  # Redirect to profile if login is successful
        else:
            return render(request, 'users/login.html', {'error_message': "Invalid email or password."})

    return render(request, 'users/login.html')

# Profile Page
@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'object': request.user})

def edit_profile_view(request):
    user = request.user
    countries = Country.objects.all()
    genders = Gender.objects.all()

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phoneno = request.POST.get('phoneno')
        user.country_id = request.POST.get('country')
        user.state_id = request.POST.get('state')
        user.city_id = request.POST.get('city')
        user.address = request.POST.get('address')
        user.gender_id = request.POST.get('gender')
        user.save()
        return redirect('profile')

    return render(request, 'users/edit_profile.html', {
        'object': user,
        'countries': countries,
        'genders': genders
    })

# Logout View
def logout_view(request):
    logout(request)  # This clears the session data and logs the user out
    return redirect('login')  # Redirect to login page after logout

def Register1(request):
    # If the request is POST, handle form submission
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        address = request.POST.get('address')
        gender_id = request.POST.get('gender')

        # Perform manual validation (e.g., check if password fields match)
        if password1 != password2:
            return render(request, 'users/Register1.html', {'error_message': "Passwords do not match."})
        
        try:
            # Manually create user without form validation
            user = ClientRegister_Model.objects.create(
                username=username,
                email=email,
                phoneno=phone_number,
                address=address,
                gender_id=gender_id,
                country_id=country_id,
                state_id=state_id,
                city_id=city_id,
            )
            user.set_password(password1)  # Set the password manually
            user.save()

            # Log the user in after saving
            login(request, user)
            return redirect('profile')

        except Exception as e:
            return render(request, 'users/Register1.html', {'error_message': str(e)})

    return render(request, 'users/Register1.html', {
        'countries': Country.objects.all(),
        'genders': Gender.objects.all(),
    })


# Get States by Country
def get_states(request, country_id):
    try:
        states = State.objects.filter(country_id=country_id)
        states_data = [{'id': state.id, 'name': state.name} for state in states]
        return JsonResponse(states_data, safe=False)
    except Country.DoesNotExist:
        return JsonResponse([], safe=False)

# Get Cities by State
def get_cities(request, state_id):
    try:
        cities = City.objects.filter(state_id=state_id)
        cities_data = [{'id': city.id, 'name': city.name} for city in cities]
        return JsonResponse(cities_data, safe=False)
    except State.DoesNotExist:
        return JsonResponse([], safe=False)

# Get Genders
def get_genders(request):
    genders = Gender.objects.all()
    genders_data = [{'id': gender.id, 'name': gender.name} for gender in genders]
    return JsonResponse({'genders': genders_data})

# # Predict Drink Driving Detection
# def Predict_Drink_Driving_Detection(request):
#     if request.method == "POST":
#         # Retrieving form data and processing...
#         pass
#     return render(request, 'users/predict_drink_driving.html')
def Predict_Drink_Driving_Detection(request):
    if request.method == "POST":
        # Retrieve data from POST request
        idnumber = request.POST.get('idnumber')
        City_Location = request.POST.get('City_Location')
        day = request.POST.get('day')
        Sex = request.POST.get('Sex')
        Age = request.POST.get('Age')
        Time = request.POST.get('Time')
        Day_of_week = request.POST.get('Day_of_week')
        Educational_level = request.POST.get('Educational_level')
        Vehicle_driver_relation = request.POST.get('Vehicle_driver_relation')
        Driving_experience = request.POST.get('Driving_experience')
        Type_of_vehicle = request.POST.get('Type_of_vehicle')
        Owner_of_vehicle = request.POST.get('Owner_of_vehicle')
        Service_year_of_vehicle = request.POST.get('Service_year_of_vehicle')
        Lanes_or_Medians = request.POST.get('Lanes_or_Medians')
        Road_allignment = request.POST.get('Road_allignment')
        Road_surface_type = request.POST.get('Road_surface_type')
        Vehicle_movement = request.POST.get('Vehicle_movement')
        # Path to the CSV file
        csv_file = 'data/Driving_Datasets.csv'

        # Load and preprocess the data
        X_train, X_test, y_train, y_test, label_encoders = load_and_preprocess_data(csv_file)

        # Logistic Regression
        print("Logistic Regression")
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred_logistic = reg.predict(X_test)
        logistic_acc = accuracy_score(y_test, y_pred_logistic) * 100
        logistic_class_report = classification_report(y_test, y_pred_logistic)
        logistic_confusion_matrix = confusion_matrix(y_test, y_pred_logistic)

        # SVM
        print("SVM")
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        svm_class_report = classification_report(y_test, predict_svm)
        svm_confusion_matrix = confusion_matrix(y_test, predict_svm)

        # Naive Bayes
        print("Naive Bayes")
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes_acc = accuracy_score(y_test, predict_nb) * 100
        naivebayes_class_report = classification_report(y_test, predict_nb)
        naivebayes_confusion_matrix = confusion_matrix(y_test, predict_nb)

        # Decision Tree Classifier
        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        decision_tree_acc = accuracy_score(y_test, dtcpredict) * 100
        decision_tree_class_report = classification_report(y_test, dtcpredict)
        decision_tree_confusion_matrix = confusion_matrix(y_test, dtcpredict)

        # Prepare data to pass to template
        context = {
            'idnumber': idnumber,
            'City_Location': City_Location,
            'logistic_accuracy': logistic_acc,
            'logistic_class_report': logistic_class_report,
            'logistic_confusion_matrix': logistic_confusion_matrix,
            'svm_accuracy': svm_acc,
            'svm_class_report': svm_class_report,
            'svm_confusion_matrix': svm_confusion_matrix,
            'naivebayes_accuracy': naivebayes_acc,
            'naivebayes_class_report': naivebayes_class_report,
            'naivebayes_confusion_matrix': naivebayes_confusion_matrix,
            'decision_tree_accuracy': decision_tree_acc,
            'decision_tree_class_report': decision_tree_class_report,
            'decision_tree_confusion_matrix': decision_tree_confusion_matrix,
        }

        return render(request, 'users/predict_result.html', context)
    else:
        return render(request, 'users/predict_drink_driving.html')