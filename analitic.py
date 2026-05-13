def detect_churn_risk(clients, threshold_days=90):
    visitors=[]
    for client in clients:
        date=client.get('last_visit_days')
        if date>threshold_days:
            visitors.append(client)
    return visitors

def predict_client_loyalty_score(client):
    visit=client.get('visits')
    avg_spent=client.get('avg_spent')
    last_visit_days=client.get('last_visit_days')
    score=0
    score+=min(visit,30)*0.3
    score+=min(avg_spent/100,30)*0.2
    score+=min(last_visit_days/30,20)*0.1
    return round(min(max(score*10,0),100))


if __name__=='__main__':
    test_clients=[{"id": 1, "name": "Oksana", "phone": "8913", "last_visit_days": 68, "visits": 3, "avg_spent": 2100 },
                    {"id": 2, "name": "Kris", "phone": "8929", "last_visit_days": 95, "visits": 2, "avg_spent": 1900},
                    {"id": 3, "name": "Sergey", "phone": "8934", "last_visit_days": 10, "visits": 10, "avg_spent": 3200}]
    for client in detect_churn_risk(test_clients, 20):
        print(client)
    for client in test_clients:
        print(predict_client_loyalty_score(client))