import firebase_admin
from firebase_admin import credentials, firestore
from graphviz import Digraph

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def build_diagram():
    diagram = Digraph(comment="Firestore Schema")
    for collection in db.collections():
        coll_name = collection.id
        diagram.node(coll_name, coll_name, shape='folder')
        docs = collection.stream()
        for doc in docs:
            doc_node = f"{coll_name}/{doc.id}"
            diagram.node(doc_node, doc.id, shape='note')
            diagram.edge(coll_name, doc_node)
            subcollections = db.collection(coll_name).document(doc.id).collections()
            for sub in subcollections:
                sub_node = f"{doc_node}/{sub.id}"
                diagram.node(sub_node, sub.id, shape='folder')
                diagram.edge(doc_node, sub_node)
    return diagram

if __name__ == "__main__":
    diagram = build_diagram()
    diagram.render('firestore_schema', format='png', cleanup=True)
    print("Το διάγραμμα αποθηκεύτηκε ως firestore_schema.png")
