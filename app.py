from flask import Flask, render_template, request, redirect, url_for

from analitic import detect_churn_risk, predict_client_loyalty_score
from database import load_data, save_data

app = Flask(__name__)

@app.route('/')
def index():
    data=load_data()
    return render_template('index.html',
                           clients_count=len(data['clients']),
                           services_count=len(data['services']),
                           appointments_count=len(data['appointments']),
                           churn_risk=detect_churn_risk(data['clients']))
@app.route('/clients')
def clients():
    data = load_data()
    clients_with_score=[]
    for client in data['clients']:
        client['loyalty_score']=predict_client_loyalty_score(client)
        clients_with_score.append(client)
    return render_template('clients.html', clients=clients_with_score)
@app.route('/clients/add', methods=['POST'])
def add_client():
    name = request.form['name']
    phone = request.form['phone']
    data=load_data()
    new_client={
        'id':len(data['clients'])+1,
        'name':name,
        'phone':phone
    }
    data['clients'].append(new_client)
    save_data(data)
    return redirect(url_for('clients'))

@app.route('/services')
def services():
    data = load_data()
    return render_template('services.html', services=data['services'])
@app.route('/services/add', methods=['POST'])
def add_service():
    data=load_data()
    data['services'].append({
        'id':len(data['services'])+1,
        'name':request.form['name'],
        'price':request.form['price']
    })
    save_data(data)
    return redirect(url_for('services'))
@app.route('/appointments')
def appointments():
    data = load_data()
    clients_by_id={c['id']:c['name'] for c in data['clients']}
    services_by_id = {s['id']: s['name'] for s in data['services']}
    appointments_view=[]
    for appointment in data['appointments']:
        appointments_view.append({
            'date':appointment['date'],
            'time':appointment['time'],
            'client_name':clients_by_id.get(appointment['client_id'], 'Клиента не существует'),
            'service_name':services_by_id.get(appointment['service_id'], 'Данной услуги не существует')
        })
    return render_template('appointments.html', appointments=appointments_view, clients=data['clients'], services=data['services'])
@app.route('/appointments/add', methods=['POST'])
def add_appointment():
    data=load_data()
    data['appointments'].append({
        'id':len(data['appointments'])+1,
        'date':request.form['date'],
        'time':request.form['time'],
        'client_id':int(request.form['client_id']),
        'service_id':int(request.form['service_id']),
    })
    save_data(data)
    return redirect(url_for('appointments'))


if __name__ == '__main__':
    app.run(debug=True)
