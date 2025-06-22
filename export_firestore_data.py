import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# 1. Σύνδεση στο Firebase
# Εισαγωγή του αρχείου κλειδιού για πρόσβαση στη βάση Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Αντικατάστησε με το path του κλειδιού σου
firebase_admin.initialize_app(cred)
db = firestore.client()

print(f"Τρέχουσα διαδρομή: {os.getcwd()}")

# 2. Συνάρτηση για ανάκτηση δεδομένων από Firestore
def fetch_firestore_structure(collection_names):
    """
    Ανάκτηση δομής δεδομένων από Firestore.
    Περιλαμβάνει υπο-συλλογές και δεδομένα εγγράφων.
    """
    structure = {}

    def fetch_subcollections(document_path):
        """
        Ανάκτηση υπο-συλλογών για ένα συγκεκριμένο έγγραφο.
        """
        subcollections = db.document(document_path).collections()
        subcollection_data = {}
        for subcollection in subcollections:
            subcollection_name = subcollection.id
            docs = subcollection.stream()
            subcollection_data[subcollection_name] = {}
            for doc in docs:
                subcollection_data[subcollection_name][doc.id] = doc.to_dict()
        return subcollection_data

    for collection in collection_names:
        print(f"Ανάκτηση δεδομένων από τη συλλογή: {collection}...")
        structure[collection] = {}
        docs = db.collection(collection).stream()
        for doc in docs:
            document_path = f"{collection}/{doc.id}"
            structure[collection][doc.id] = {
                "fields": doc.to_dict(),
                "subcollections": fetch_subcollections(document_path),
            }

    return structure

# 3. Ανάκτηση και αποθήκευση δεδομένων σε πολλαπλά JSON αρχεία
def export_collections_to_json(collection_names):
    """
    Εξαγωγή κάθε συλλογής σε ξεχωριστό αρχείο JSON.
    """
    # Εκτύπωση του τρέχοντος καταλόγου
    current_directory = os.getcwd()
    print(f"Ο τρέχων κατάλογος εκτέλεσης είναι: {current_directory}")

    # Εναλλακτικός φάκελος αποθήκευσης
    downloads_folder = "C:\\temp"
     #downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    for collection in collection_names:
        try:
            # Ανάκτηση δεδομένων συλλογής
            collection_data = fetch_firestore_structure([collection])
            
            # Δημιουργία ονόματος αρχείου JSON
            output_file = os.path.join(downloads_folder, f"{collection}_data.json")
            print(f"Διαδρομή αρχείου: {output_file}")
            downloads_folder = "C:\\temp"

            
            # Αποθήκευση δεδομένων στο αρχείο JSON
            with open(output_file, "w", encoding="utf-8") as f:
             json.dump(collection_data, f, ensure_ascii=False, indent=4)
            print(f"Η εγγραφή ολοκληρώθηκε για το αρχείο: {output_file}")

            
            print(f"Η συλλογή '{collection}' αποθηκεύτηκε στο '{output_file}'.")
        except Exception as e:
            print(f"Σφάλμα κατά την εξαγωγή της συλλογής '{collection}': {e}")

# 4. Συλλογές προς ανάκτηση
collections_to_fetch = ["users", "admin_logs", "menu", "pois", "roles", "routes", "Authentication"]

# 5. Εκτέλεση εξαγωγής δεδομένων
print("Ξεκινά η εξαγωγή δεδομένων από Firestore...")
export_collections_to_json(collections_to_fetch)
print("Η εξαγωγή ολοκληρώθηκε!")
