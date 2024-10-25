import time
import requests

# URL de l'API OWASP ZAP
zap_url = "http://localhost:8080"
scan_url = "http://example.com"  # Remplace par le site cible autorisé pour le scan

# Démarrer un scan actif
scan_response = requests.get(f"{zap_url}/JSON/ascan/action/scan/?url={scan_url}")
scan_data = scan_response.json()

# Récupérer l'ID du scan
scan_id = scan_data.get('scan', None)

if scan_id:
    print(f"Scan ID : {scan_id}")

    # Vérifier l'état du scan
    scan_status = 0
    while int(scan_status) < 100:
        status_response = requests.get(f"{zap_url}/JSON/ascan/view/status/?scanId={scan_id}")
        scan_status = status_response.json().get('status')
        print(f"Scan en cours : {scan_status}%")
        
        # Attendre quelques secondes avant de vérifier à nouveau
        time.sleep(5)
    
    print("Scan terminé.")

    # Récupérer les résultats du scan (alertes)
    alerts = requests.get(f"{zap_url}/JSON/alert/view/alerts/?baseurl={scan_url}")
    alerts_data = alerts.json()

    # Afficher les alertes
    print(f"Résultats du scan pour {scan_url} :")
    for alert in alerts_data.get('alerts', []):
        print(f"Nom de l'alerte : {alert['alert']}")
        print(f"Description : {alert['desc']}")
        print(f"Solution : {alert['solution']}")
        print(f"Risque : {alert['risk']}")
        print("-" * 40)

else:
    print("Impossible de démarrer le scan.")
